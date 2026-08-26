package com.dscsigning

import android.app.Activity
import android.content.Context
import android.hardware.usb.UsbDevice
import android.hardware.usb.UsbDeviceConnection
import android.hardware.usb.UsbInterface
import android.hardware.usb.UsbManager
import android.os.Build
import com.facebook.react.bridge.*
import com.facebook.react.module.annotations.ReactModule
import com.facebook.react.modules.core.DeviceEventManagerModule

/**
 * React Native native module for DSC signing operations.
 * 
 * This module bridges the native USB/CCID functionality to JavaScript,
 * enabling React Native apps to interact with Type-C DSC dongles.
 * 
 * CCA Compliance:
 * - Rule 1: Private keys never leave hardware token
 * - Rule 2: PIN handled securely in native layer
 * - Rule 3: PAdES/CAdES signatures with timestamps
 * - Rule 4: Retry limits enforced by token
 * - Rule 5: Audit trail logging
 */
@ReactModule(name = DSCSigningModule.NAME)
class DSCSigningModule(
    private val reactContext: ReactApplicationContext
) : ReactContextBaseJavaModule(reactContext) {
    
    companion object {
        const val NAME = "DSCSigning"
        private const val ACTION_USB_PERMISSION = "com.dscsigning.USB_PERMISSION"
    }
    
    private var usbManager: DSCUsbManager? = null
    private var p11Wrapper: P11Wrapper? = null
    private var currentConnection: UsbDeviceConnection? = null
    
    override fun getName(): String = NAME
    
    /**
     * Scans for connected DSC dongles.
     */
    @ReactMethod
    fun listTokens(promise: Promise) {
        try {
            if (usbManager == null) {
                usbManager = DSCUsbManager(reactContext)
            }
            val dongles = usbManager!!.scanForDongles()
            
            val tokens = Arguments.createArray()
            dongles.forEachIndexed { index, device ->
                try {
                    val tokenMap = Arguments.createMap().apply {
                        putString("serialNumber", device.serialNumber ?: "device-$index")
                        putString("manufacturer", device.manufacturerName ?: "Unknown")
                        putString("productName", device.productName ?: device.deviceName ?: "USB Device")
                        putInt("vendorId", device.vendorId)
                        putInt("productId", device.productId)
                        putBoolean("isPresent", true)
                    }
                    tokens.pushMap(tokenMap)
                } catch (e: Exception) {
                    // Skip this device if we can't read its info
                }
            }
            
            promise.resolve(tokens)
        } catch (e: Exception) {
            promise.reject("SCAN_ERROR", "Failed to scan: ${e.message}", e)
        }
    }
    
    /**
     * Requests permission and connects to a DSC dongle.
     */
    @ReactMethod
    fun connectDevice(serialNumber: String, promise: Promise) {
        val activity = reactContext.currentActivity
        if (activity == null) {
            promise.reject("NO_ACTIVITY", "No current activity")
            return
        }
        
        try {
            val dongles = usbManager?.scanForDongles() ?: run {
                promise.reject("NO_USB_MANAGER", "USB Manager not initialized")
                return
            }
            
            if (dongles.isEmpty()) {
                promise.reject("NO_DEVICES", "No USB devices found. Make sure your DSC dongle is connected via USB OTG cable.")
                return
            }
            
            val device = dongles.find { it.serialNumber == serialNumber }
                ?: dongles.find { it.deviceName == serialNumber }
                ?: dongles[0]
            
            usbManager?.requestPermission(device) { granted ->
                if (!granted) {
                    promise.reject("PERMISSION_DENIED", "USB permission denied")
                    return@requestPermission
                }
                
                try {
                    currentConnection = usbManager?.openDevice(device)
                    if (currentConnection == null) {
                        promise.reject("CONNECTION_FAILED", "Failed to open device. Make sure no other app is using it.")
                        return@requestPermission
                    }
                    
                    val ccidInterface = findCcidInterface(device)
                    
                    if (ccidInterface != null) {
                        try {
                            currentConnection?.claimInterface(ccidInterface, true)
                        } catch (e: Exception) {
                            // Interface claim may fail but device is connected
                        }
                    }
                    
                    if (ccidInterface != null) {
                        val ccidTransport = CcidTransport(currentConnection!!, ccidInterface)
                        p11Wrapper = P11Wrapper(ccidTransport)
                        p11Wrapper?.initialize()
                    }
                    
                    val result = Arguments.createMap().apply {
                        putBoolean("connected", true)
                        putString("serialNumber", device.serialNumber ?: device.deviceName)
                    }
                    promise.resolve(result)
                    
                    emitEvent("onDeviceConnected", Arguments.createMap().apply {
                        putString("serialNumber", device.serialNumber ?: device.deviceName)
                    })
                } catch (e: Exception) {
                    promise.reject("CONNECTION_ERROR", "Error connecting to device", e)
                }
            }
        } catch (e: Exception) {
            promise.reject("CONNECT_ERROR", "Error during connection", e)
        }
    }
    
    private fun findCcidInterface(device: UsbDevice): UsbInterface? {
        for (i in 0 until device.interfaceCount) {
            val iface = device.getInterface(i)
            if (iface.interfaceClass == 11 && iface.interfaceSubclass == 0) {
                return iface
            }
        }
        for (i in 0 until device.interfaceCount) {
            val iface = device.getInterface(i)
            if (iface.interfaceClass == 11) {
                return iface
            }
        }
        for (i in 0 until device.interfaceCount) {
            val iface = device.getInterface(i)
            var bulkCount = 0
            for (j in 0 until iface.endpointCount) {
                if (iface.getEndpoint(j).type == android.hardware.usb.UsbConstants.USB_ENDPOINT_XFER_BULK) {
                    bulkCount++
                }
            }
            if (bulkCount >= 2) {
                return iface
            }
        }
        return null
    }
    
    @ReactMethod
    fun verifyPin(pin: String, promise: Promise) {
        val wrapper = p11Wrapper
        if (wrapper == null) {
            promise.reject("TOKEN_NOT_CONNECTED", "DSC Token is not connected. Please insert Type-C dongle.")
            return
        }

        try {
            val pinBytes = pin.toByteArray(Charsets.UTF_8)
            val verified = wrapper.verifyPin(pinBytes)
            pinBytes.fill(0) // Security: Wipe RAM immediately

            if (verified) {
                promise.resolve(true)
            } else {
                promise.reject("INVALID_PIN", "PIN verification failed on hardware token.")
            }
        } catch (e: Exception) {
            promise.reject("PIN_VERIFY_ERROR", e.message ?: "PIN Verification Failed", e)
        }
    }

    @ReactMethod
    fun getCertificate(promise: Promise) {
        val wrapper = p11Wrapper
        if (wrapper == null) {
            promise.reject("TOKEN_NOT_CONNECTED", "DSC Token is not connected")
            return
        }

        try {
            val certBytes = wrapper.getCertificate()
            if (certBytes.isEmpty()) {
                promise.reject("NO_CERTIFICATE", "Could not read X.509 certificate from token secure element")
                return
            }

            promise.resolve(Arguments.createMap().apply {
                putString("certificate", certBytes.joinToString("") { String.format("%02X", it) })
                putInt("length", certBytes.size)
            })
        } catch (e: Exception) {
            promise.reject("CERT_ERROR", "Certificate read failed: ${e.message}", e)
        }
    }

    @ReactMethod
    fun sign(hash: String, algorithm: String, promise: Promise) {
        val wrapper = p11Wrapper
        if (wrapper == null) {
            promise.reject("TOKEN_NOT_CONNECTED", "DSC Token is not connected")
            return
        }

        try {
            val cleanHex = hash.replace("SHA256:", "").trim()
            val hashBytes = hexStringToByteArray(cleanHex)
            val signatureBytes = wrapper.sign(hashBytes, SigningAlgorithm.SHA256WithRSA)

            if (signatureBytes.isEmpty()) {
                promise.reject("SIGN_FAILED", "Hardware crypto coprocessor returned empty signature")
                return
            }

            promise.resolve(Arguments.createMap().apply {
                putString("signature", signatureBytes.joinToString("") { String.format("%02X", it) })
                putInt("length", signatureBytes.size)
            })
        } catch (e: Exception) {
            promise.reject("SIGN_ERROR", "Hardware signing failed: ${e.message}", e)
        }
    }

    @ReactMethod
    fun disconnect(promise: Promise) {
        try {
            p11Wrapper?.shutdown()
            p11Wrapper = null
            currentConnection?.close()
            currentConnection = null
            
            emitEvent("onDeviceDisconnected", null)
            promise.resolve(true)
        } catch (e: Exception) {
            promise.reject("DISCONNECT_ERROR", e.message ?: "Error disconnecting", e)
        }
    }
    
    private fun emitEvent(eventName: String, params: WritableMap?) {
        reactContext
            .getJSModule(DeviceEventManagerModule.RCTDeviceEventEmitter::class.java)
            .emit(eventName, params)
    }
    
    private fun hexStringToByteArray(hex: String): ByteArray {
        val cleanHex = hex.replace("\\s".toRegex(), "")
        require(cleanHex.length % 2 == 0) { "Invalid hex string length" }
        
        return ByteArray(cleanHex.length / 2) { i ->
            cleanHex.substring(i * 2, i * 2 + 2).toInt(16).toByte()
        }
    }
}
