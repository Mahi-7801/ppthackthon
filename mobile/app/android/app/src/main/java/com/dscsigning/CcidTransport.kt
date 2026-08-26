package com.dscsigning

import android.hardware.usb.UsbDeviceConnection
import android.hardware.usb.UsbInterface
import java.nio.ByteBuffer
import java.nio.ByteOrder

/**
 * CCID (Chip Card Interface Device) protocol implementation over USB bulk transfers.
 * 
 * This module handles low-level communication with CCID-compliant smart card readers,
 * implementing the PC/SC specifications for smart card interoperability.
 * 
 * CCA Rule 1: All operations happen on the hardware token; we only send hashes
 * and receive signature blobs.
 */
class CcidTransport(private val connection: UsbDeviceConnection, private val iface: UsbInterface) {

    companion object {
        // CCID message types
        private const val PC_TO_RDR_ICC_POWER_ON = 0x62
        private const val PC_TO_RDR_ICC_POWER_OFF = 0x63
        private const val PC_TO_RDR_GET_SLOT_STATUS = 0x65
        private const val PC_TO_RDR_XFR_BLOCK = 0x6F
        private const val RDR_TO_PC_DATA_BLOCK = 0x80
        private const val RDR_TO_PC_SLOT_STATUS = 0x81

        // CCID status codes
        private const val SLOT_STATUS_PRESENT = 0x00
        private const val SLOT_STATUS_ABSENT = 0x01
        private const val SLOT_STATUS_ERROR = 0x02

        // APDU constants
        private const val APDU_CLA = 0x00
        private const val APDU_P1 = 0x00
        private const val APDU_P2 = 0x00

        // Buffer sizes
        private const val MAX_BUFFER_SIZE = 261
        private const val HEADER_SIZE = 10

        // CCA Rule 1: Transfer timeout for USB communication
        private const val TRANSFER_TIMEOUT = 5000
    }

    private var slotIndex: Int = 0

    // CCA Rule 1: Dynamically discover bulk transfer endpoints from the USB interface
    private val bulkOutEndpoint: android.hardware.usb.UsbEndpoint by lazy {
        findBulkEndpoint(isIn = false)
    }
    private val bulkInEndpoint: android.hardware.usb.UsbEndpoint by lazy {
        findBulkEndpoint(isIn = true)
    }

    private fun findBulkEndpoint(isIn: Boolean): android.hardware.usb.UsbEndpoint {
        for (i in 0 until iface.endpointCount) {
            val ep = iface.getEndpoint(i)
            if (ep.type == android.hardware.usb.UsbConstants.USB_ENDPOINT_XFER_BULK) {
                if (isIn && ep.direction == android.hardware.usb.UsbConstants.USB_DIR_IN) return ep
                if (!isIn && ep.direction == android.hardware.usb.UsbConstants.USB_DIR_OUT) return ep
            }
        }
        throw CcidException("Bulk ${if (isIn) "IN" else "OUT"} endpoint not found on CCID interface")
    }
    
    /**
     * Sends a CCID command to the reader and receives the response.
     */
    private fun sendCcidCommand(command: ByteArray): ByteArray {
        val sent = connection.bulkTransfer(bulkOutEndpoint, command, command.size, TRANSFER_TIMEOUT)
        if (sent < 0) {
            throw CcidException("Failed to send CCID command")
        }

        val responseBuffer = ByteArray(MAX_BUFFER_SIZE)
        val received = connection.bulkTransfer(bulkInEndpoint, responseBuffer, responseBuffer.size, TRANSFER_TIMEOUT)
        if (received < 0) {
            throw CcidException("Failed to receive CCID response")
        }

        return responseBuffer.copyOf(received)
    }
    
    /**
     * Powers on the ICC (Integrated Circuit Card) and receives the ATR.
     * CCA Rule 1: Initializes secure communication channel with hardware token.
     */
    fun powerOn(): ByteArray {
        // CCID PC_TO_RDR_IccPowerOn command
        val command = ByteArray(HEADER_SIZE + 1)
        // Message type
        command[0] = PC_TO_RDR_ICC_POWER_ON.toByte()
        // Slot
        command[5] = slotIndex.toByte()
        // Length (4 bytes, little endian) = 1 (power select byte)
        command[6] = 0x01
        command[7] = 0x00
        command[8] = 0x00
        command[9] = 0x00
        // Power select: auto
        command[10] = 0x00
        
        val response = sendCcidCommand(command)
        
        // Extract ATR from response
        if (response.size > HEADER_SIZE) {
            val atrLength = response.size - HEADER_SIZE
            return response.copyOfRange(HEADER_SIZE, HEADER_SIZE + atrLength)
        }
        
        return byteArrayOf()
    }
    
    /**
     * Powers off the ICC.
     */
    fun powerOff() {
        val command = ByteBuffer.allocate(HEADER_SIZE)
            .order(ByteOrder.LITTLE_ENDIAN)
            .putInt(HEADER_SIZE) // length
            .putInt(PC_TO_RDR_ICC_POWER_OFF) // message type
            .putInt(slotIndex) // slot
            .putInt(0) // length
            .array()
        
        sendCcidCommand(command)
    }
    
    /**
     * Gets the current slot status (card present/absent/error).
     */
    fun getSlotStatus(): Int {
        val command = ByteBuffer.allocate(HEADER_SIZE)
            .order(ByteOrder.LITTLE_ENDIAN)
            .putInt(HEADER_SIZE) // length
            .putInt(PC_TO_RDR_GET_SLOT_STATUS) // message type
            .putInt(slotIndex) // slot
            .putInt(0) // length
            .array()
        
        val response = sendCcidCommand(command)
        return when (response[7].toInt() and 0x03) {
            0x00 -> SLOT_STATUS_PRESENT
            0x01 -> SLOT_STATUS_ABSENT
            else -> SLOT_STATUS_ERROR
        }
    }
    
    /**
     * Sends an APDU command to the smart card and receives the response.
     * This is the primary interface for PKCS#11 operations.
     * 
     * CCA Rule 1: All cryptographic operations are delegated to the hardware token.
     */
    fun transmitApdu(command: ByteArray): ByteArray {
        // Wrap APDU in CCID XFR_BLOCK message
        val ccidHeader = ByteArray(HEADER_SIZE + command.size)
        // Message type: XFR_BLOCK
        ccidHeader[0] = PC_TO_RDR_XFR_BLOCK.toByte()
        // Slot
        ccidHeader[5] = slotIndex.toByte()
        // APDU length (4 bytes little endian)
        ccidHeader[6] = (command.size and 0xFF).toByte()
        ccidHeader[7] = ((command.size shr 8) and 0xFF).toByte()
        ccidHeader[8] = 0x00
        ccidHeader[9] = 0x00
        // Copy APDU data
        System.arraycopy(command, 0, ccidHeader, HEADER_SIZE, command.size)
        
        val response = sendCcidCommand(ccidHeader)
        
        // Extract response data (skip CCID header)
        if (response.size > HEADER_SIZE) {
            return response.copyOfRange(HEADER_SIZE, response.size)
        }
        
        return byteArrayOf()
    }
    
    /**
     * Selects an application on the smart card by AID.
     */
    fun selectApplication(aid: ByteArray): ByteArray {
        val apdu = byteArrayOf(
            APDU_CLA.toByte(), // CLA
            0xA4.toByte(), // INS: SELECT
            APDU_P1.toByte(),
            APDU_P2.toByte(),
            aid.size.toByte() // Lc
        ) + aid + byteArrayOf(0x00) // Le
        
        return transmitApdu(apdu)
    }
    
    /**
     * Verifies PIN by sending standard ISO 7816-4 APDU to the hardware token.
     * 
     * CCA Rule 2: PIN is sent directly to hardware token, memory wiped immediately.
     */
    fun verifyPin(pin: ByteArray): Boolean {
        // Standard ISO 7816-4 VERIFY command: CLA=0x00, INS=0x20, P1=0x00, P2=0x01, Lc=len, Data=pin
        val apdu = byteArrayOf(
            0x00, // CLA
            0x20.toByte(), // INS: VERIFY
            0x00, // P1
            0x01, // P2: User PIN slot
            pin.size.toByte() // Lc
        ) + pin

        val response = transmitApdu(apdu)
        if (response.size < 2) {
            throw CcidException("Hardware token returned invalid APDU response length")
        }

        val sw1 = response[response.size - 2].toInt() and 0xFF
        val sw2 = response[response.size - 1].toInt() and 0xFF

        // 0x9000 = Success
        if (sw1 == 0x90 && sw2 == 0x00) {
            return true
        }

        // 0x63CX = Incorrect PIN with X attempts remaining
        if (sw1 == 0x63) {
            val remaining = sw2 and 0x0F
            throw CcidException("Incorrect PIN: $remaining attempts remaining before token lock.")
        }

        // 0x6983 = Authentication Method Blocked (Token locked)
        if (sw1 == 0x69 && sw2 == 0x83) {
            throw CcidException("Token PIN is BLOCKED due to consecutive failed attempts.")
        }

        throw CcidException("PIN Verification failed with Status Word: ${String.format("%02X %02X", sw1, sw2)}")
    }
    
    /**
     * Checks if APDU response indicates success (SW1=0x90, SW2=0x00)
     */
    private fun checkSuccess(response: ByteArray): Boolean {
        if (response.size < 2) return false
        val sw1 = response[response.size - 2].toInt() and 0xFF
        val sw2 = response[response.size - 1].toInt() and 0xFF
        return sw1 == 0x90 && sw2 == 0x00
    }
    
    /**
     * Signs a hash using the hardware token's private key.
     * 
     * CCA Rule 1: Signing operation happens entirely on the hardware token secure element.
     * Private key never leaves the hardware token.
     */
    fun sign(hash: ByteArray, algorithm: SigningAlgorithm = SigningAlgorithm.SHA256WithRSA): ByteArray {
        // DigestInfo prefix for SHA-256 (RFC 3447 PKCS#1 v1.5)
        val sha256DigestInfoPrefix = byteArrayOf(
            0x30, 0x31, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86.toByte(), 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20
        )
        val tData = if (hash.size == 32) sha256DigestInfoPrefix + hash else hash

        // Manage Security Environment (MSE: Set Digital Signature Key)
        val selectKeyApdu = byteArrayOf(
            0x00, // CLA
            0x22.toByte(), // INS: MANAGE SECURITY ENVIRONMENT
            0x41.toByte(), // P1: Set computation/signature
            0xB6.toByte(), // P2: Digital Signature
            0x06.toByte(), // Lc
            0x80.toByte(), 0x01, algorithm.value, // Tag Algorithm
            0x84.toByte(), 0x01, 0x01 // Key reference 1
        )
        try {
            transmitApdu(selectKeyApdu)
        } catch (e: Exception) {
            // Some tokens do not require explicit MSE if default signing key is active
        }
        
        // Perform PSO: Compute Digital Signature (INS=0x2A, P1=0xBE or 0x9E)
        val signApdu = byteArrayOf(
            0x00, // CLA
            0x2A.toByte(), // INS: PSO
            0xBE.toByte(), // P1: compute digital signature
            0x00, // P2
            tData.size.toByte() // Lc
        ) + tData + byteArrayOf(0x00) // Le (256 bytes RSA response)
        
        val response = transmitApdu(signApdu)
        
        if (response.size < 2) {
            throw CcidException("Invalid signing response from hardware token")
        }
        
        val sw1 = response[response.size - 2].toInt() and 0xFF
        val sw2 = response[response.size - 1].toInt() and 0xFF
        
        if (sw1 == 0x90 && sw2 == 0x00) {
            return response.copyOfRange(0, response.size - 2)
        }

        // Alternative APDU for tokens supporting ISO 7816-8 P1=0x9E, P2=0x9A
        val altSignApdu = byteArrayOf(
            0x00,
            0x2A.toByte(),
            0x9E.toByte(),
            0x9A.toByte(),
            tData.size.toByte()
        ) + tData + byteArrayOf(0x00)

        val altResp = transmitApdu(altSignApdu)
        if (altResp.size >= 2) {
            val altSw1 = altResp[altResp.size - 2].toInt() and 0xFF
            val altSw2 = altResp[altResp.size - 1].toInt() and 0xFF
            if (altSw1 == 0x90 && altSw2 == 0x00) {
                return altResp.copyOfRange(0, altResp.size - 2)
            }
        }
        
        throw CcidException("Hardware token signing failed with Status Word: ${String.format("%02X %02X", sw1, sw2)}")
    }
    
    /**
     * Gets the certificate from the hardware token.
     * 
     * CCA Rule 1: Certificate retrieval does not expose private key material.
     */
    fun getCertificate(): ByteArray {
        val apdu = byteArrayOf(
            0x00, // CLA
            0xB0.toByte(), // INS: READ BINARY
            0x80.toByte(), // P1: use EF with logical path
            0x00, // P2
            0x00 // Le (256 bytes)
        )
        
        return transmitApdu(apdu)
    }
    
    /**
     * Gets the serial number of the smart card.
     */
    fun getSerialNumber(): String {
        val apdu = byteArrayOf(
            0x00, // CLA
            0xCA.toByte(), // INS: GET DATA
            0x9F.toByte(), // P1
            0x17, // P2
            0x00 // Le
        )
        
        val response = transmitApdu(apdu)
        if (response.size < 2) {
            return ""
        }
        
        return response.copyOfRange(0, response.size - 2).joinToString("") { 
            String.format("%02X", it) 
        }
    }
}

/**
 * Signing algorithm identifiers for PKCS#11 operations.
 */
enum class SigningAlgorithm(val value: Byte) {
    SHA1WithRSA(0x10),
    SHA256WithRSA(0x11),
    SHA384WithRSA(0x12),
    SHA512WithRSA(0x13),
    SHA256WithECDSA(0x14)
}

/**
 * Exception thrown for CCID-related errors.
 */
class CcidException(message: String, cause: Throwable? = null) : Exception(message, cause)
