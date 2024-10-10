#include <Arduino.h>
#include "PinDefinitionsAndMore.h"
#include <IRremote.hpp>

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(115200);
    while (!Serial); // Wait for Serial to become available.

#if defined(__AVR_ATmega32U4__) || defined(SERIAL_PORT_USBVIRTUAL) || defined(SERIAL_USB) /*stm32duino*/|| defined(USBCON) /*STM32_stm32*/ \
    || defined(SERIALUSB_PID)  || defined(ARDUINO_ARCH_RP2040) || defined(ARDUINO_attiny3217)
    delay(4000); // To connect Serial monitor after reset or power up and before first print out.
#endif

    IrSender.begin(); // Start IR sending
    Serial.println(F("[INIT] IR Send Program Initialized"));
}

bool isValidHexString(String str) {
    if (str.length() < 3 || str.substring(0, 2) != "0x") {
        return false; // Must start with "0x"
    }
    for (int i = 2; i < str.length(); i++) {
        char c = str.charAt(i);
        if (!isHexadecimalDigit(c)) {
            return false;
        }
    }
    return true;
}

bool isValidUintString(String str) {
    if (str.length() > 9) {
        return false; 
    }
    for (int i = 0; i < str.length(); i++) {
        char c = str.charAt(i);
        if (!isDigit(c)) {
            return false;
        }
    }
    return true;
}

unsigned long hexToULong(String hexStr) {
    return strtoul(hexStr.c_str(), NULL, 16);
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim(); 
        
        Serial.print(F("[INFO] Received input: "));
        Serial.println(input);

        // separate input string with spaces
        int spaceIndex = input.indexOf(' '); 
        if (spaceIndex == -1) {
            Serial.println(F("[ERROR] Invalid input format. Expected space separator."));
            return;
        }
        String addressStr = input.substring(0, spaceIndex);
        String commandStr = input.substring(spaceIndex + 1);
        String repeatsStr = "1";
        spaceIndex = commandStr.indexOf(' ');
        if (spaceIndex != -1){
          repeatsStr  = commandStr.substring(spaceIndex + 1);
          commandStr = commandStr.substring(0, spaceIndex);
        }

        Serial.print(F("[INFO] Address string: "));
        Serial.println(addressStr);
        Serial.print(F("[INFO] Command string: "));
        Serial.println(commandStr);
        Serial.print(F("[INFO] Repeats string: "));
        Serial.println(repeatsStr);

        if (!isValidHexString(addressStr)) {
            Serial.println(F("[ERROR] Invalid address format."));
            return;
        }
        if (!isValidHexString(commandStr)) {
            Serial.println(F("[ERROR] Invalid command format."));
            return;
        }
        if (!isValidUintString(repeatsStr)) {
            Serial.println(F("[ERROR] Invalid repeats format."));
            return;
        }

        // Convert to unsigned long hex values
        unsigned long address = hexToULong(addressStr);
        unsigned long command = hexToULong(commandStr);
        unsigned long repeats = repeatsStr.toInt();

        Serial.print(F("[INFO] Sending "));
        Serial.print(repeats);
        Serial.print(F(" repeats of IR command with address: 0x"));
        Serial.print(address, HEX);
        Serial.print(F(" and command: 0x"));
        Serial.println(command, HEX);

        // send
        IrSender.sendNEC(address, command, repeats);
        Serial.println(F("[OK] IR command sent successfully."));
    }
}
