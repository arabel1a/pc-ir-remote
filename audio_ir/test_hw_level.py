import numpy as np
import sounddevice as sd


def play_50hz(duration=3, sample_rate=192000, frequency=50):
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Generate a 38 kHz sine wave
    sound = 5 * np.cos(np.pi * frequency * t)  # 0.5 for volume control

    print(sound[:100])
    # Play the sound
    sd.play(sound, samplerate=sample_rate)

    # Wait until sound has finished playing
    sd.wait()


# Example usage
play_50hz(duration=100)  # Plays a 38 kHz sine wave for 10 seconds
