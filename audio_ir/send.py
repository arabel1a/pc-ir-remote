import time
import argparse
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import matplotlib.pyplot as plt


def nec_waveform(
    address: int, command: int, sample_rate: int = 44100, carrier_freq: int = 10000
):
    # Calculate the number of samples per segment
    meander_on_samples = int(sample_rate * 560e-6)
    meander_off_samples_1 = int(sample_rate * (2250e-6 - 560e-6))
    meander_off_samples_0 = int(sample_rate * (1120e-6 - 560e-6))

    # Calculate the number of samples for preamble and pauses
    preamble_meander_samples = int(sample_rate * 9000e-6)
    long_pause_samples = int(sample_rate * 4500e-6)

    # Carrier wave for 38kHz
    t = np.arange(0, meander_on_samples) / sample_rate
    carrier = np.sin(2 * np.pi * carrier_freq * t)  # / 2

    # Build waveform
    waveform = np.zeros(0)

    # Preamble and long pause
    waveform = np.concatenate(
        [
            waveform,
            np.tile(carrier, int(preamble_meander_samples / meander_on_samples)),
            np.zeros(long_pause_samples),
        ]
    )

    # Construct the bit string
    address_bits = f"{address:08b}"[::-1]
    address_inv_bits = "".join("1" if x == "0" else "0" for x in address_bits)
    command_bits = f"{command:08b}"[::-1]
    command_inv_bits = "".join("1" if x == "0" else "0" for x in command_bits)

    bitstring = address_bits + address_inv_bits + command_bits + command_inv_bits
    print(f"Bitstring: {bitstring}")

    # Convert the bitstring to waveform
    for bit in bitstring:
        waveform = np.concatenate(
            [
                waveform,
                carrier,  # 560µs meander
                np.zeros(
                    meander_off_samples_1 if bit == "1" else meander_off_samples_0
                ),
            ]
        )

    # Add stop bit
    waveform = np.concatenate([waveform, carrier])

    # Normalize the waveform to between -1 and 1 (for WAV file compatibility)
    waveform = waveform / np.max(np.abs(waveform))

    return waveform


def plot_wav(filename):
    # Read the WAV file
    sample_rate, data = wav.read(filename)

    # Generate time axis in seconds
    duration = len(data) / sample_rate

    # Convert to milliseconds
    time = np.linspace(0, duration * 1000, num=len(data))

    plt.figure(figsize=(12, 6))
    plt.plot(time, data, label="Audio Signal")
    plt.title("WAV File Audio Signal")
    plt.xlabel("Time [ms]")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.legend()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Send command to a device via a serial port."
    )
    parser.add_argument("address", type=str, help="Target device address")
    parser.add_argument("command", type=str, help="Command to send")
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=192000,
        help="Maximal sample rate",
    )

    args = parser.parse_args()
    waveform = nec_waveform(args.address, args.command, args.sample_rate)
    wav.write("nec_signal.wav", sample_rate, waveform.astype(np.float32))
    sd.play(waveform, samplerate=sample_rate)
    sd.wait()
    # plot_wav("nec_signal.wav")


if __name__ == "__main__":
    main()
