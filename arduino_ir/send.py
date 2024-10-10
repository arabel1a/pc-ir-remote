import argparse
import serial
import time
import logging
import sys


def recieve(device, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = device.readline()
        decoded_response = response.decode("utf-8").strip()
        if decoded_response == "":
            # logging.warning(f"Got empty response.")
            continue
        return decoded_response
    else:
        logging.error(f"Timeout waiting for the response.")
        sys.exit(1)


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="Send command to a device via a serial port."
    )
    parser.add_argument("address", type=str, help="Target device address")
    parser.add_argument("command", type=str, help="Command to send")
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Number of command repats",
    )

    parser.add_argument(
        "--serial_port",
        type=str,
        default="/dev/ttyUSB0",
        help="Serial port to use (default: /dev/ttyUSB0)",
    )

    args = parser.parse_args()
    address = args.address
    command = args.command
    repeats = args.repeats
    serial_port = args.serial_port

    full_command = f"{address} {command} {repeats}"
    logging.info(f"Preparing to send command: >{full_command}< to {serial_port}")

    # check if the serial port is busy and wait for it to become available
    start_time = time.time()
    while time.time() - start_time < 10:  # 10-second timeout
        try:
            with serial.Serial(serial_port, timeout=1) as ser:
                logging.info(f"Port {serial_port} is available.")
                break
        except serial.SerialException as e:
            logging.warning(f"Port {serial_port} is busy. Retrying...")
            time.sleep(1)
    else:
        logging.error(
            f"Port {serial_port} did not become available within 10 seconds. Aborting."
        )
        sys.exit(1)

    # Start the communication. WARNING: the arduino resets when it receive DTR.
    try:
        with serial.Serial(
            serial_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            write_timeout=1,
        ) as ser:
            msg = recieve(ser)
            if "[INIT]" in msg:
                logging.info("Device initialization sucesfull.")
            else:
                logging.error(f"Inadequate init message: {msg}.")
                sys.exit(1)

            # send the command to the device
            ser.write(full_command.encode())
            logging.info(f"Sent command: >{full_command}< to {serial_port}")

            while True:  # if no messages in 10s, recieve will throw an error
                msg = recieve(ser)
                if "[OK]" in msg:
                    logging.info("Received 'OK' from the device. Exiting successfully.")
                    sys.exit(0)
                elif "[ERROR]" in msg:
                    logging.error(f"Device error: {msg.replace('[ERROR]', '')}")
                    sys.exit(1)
                elif "[INFO]" in msg:
                    logging.info(f"Device info: {msg.replace('[INFO]', '')}")
                else:
                    logging.error(f"Unexpected response: >{msg}<.")
                    sys.exit(1)

    except serial.SerialException as e:
        logging.error(f"Error occurred while communicating with {serial_port}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
