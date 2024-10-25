import numpy as np
import pyaudio
from scipy.signal import find_peaks


def main():
    ...


# Parameters
start_freq = 0  # Start frequency in Hz
end_freq = 0  # End frequency in Hz
duration = 2  # Duration of each tone in seconds
sample_rate = 44100  # Sample rate in Hz

# Initialize PyAudio
pa = pyaudio.PyAudio()

print("\n \n*** Toney The Tiger resonant frequency scanner created by ionnoim *** \n        This is an open source project. Consult the README file.")
tiger = r'''
                     __,,,,_
          _ __..-;''`--/'/ /.',-`-.
      (`/' ` |  \ \ \\ / / / / .-'/`,_
     /'`\ \   |  \ | \| // // / -.,/_,'-,
    /<7' ;  \ \  | ; ||/ /| | \/    |`-/,/-.,_,/')
   /  _.-, `,-\,__|  _-| / \ \/|_/  |    '-/.;.\'
   `-`  f/ ;      / __/ \__ `/ |__/ |
        `-'      |  -| =|\_  \  |-' |
              __/   /_..-' `  ),'  //
          fL ((__.-'((___..-'' \__.'
'''  

print(tiger)
# Function to generate a tone
def generate_tone(freq, duration, sample_rate):
    """
    Generate a sine wave for a given frequency and duration.
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave.astype(np.float32)

# Function to play a tone and record a response
def play_and_record(freq, duration, sample_rate, input_device_index=None, output_device_index=None):
    """
    Play the generated tone and record the response.
    """
    # Generate the tone
    tone = generate_tone(freq, duration, sample_rate)

    # Attempt to open streams with error handling
    try:
        # Open stream for playing sound
        play_stream = pa.open(format=pyaudio.paFloat32,
                              channels=1,
                              rate=sample_rate,
                              output=True,
                              output_device_index=output_device_index)

        # Play the tone
        play_stream.write(tone.tobytes())
        play_stream.stop_stream()
        play_stream.close()

        # Open stream for recording
        record_stream = pa.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=sample_rate,
                                input=True,
                                input_device_index=input_device_index,
                                frames_per_buffer=1024)

        # Record the response
        frames = []
        for _ in range(0, int(sample_rate / 1024 * duration)):
            data = record_stream.read(1024)
            frames.append(data)

        record_stream.stop_stream()
        record_stream.close()

        return b''.join(frames)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to analyze the response
def analyze_response(recorded_data, sample_rate):
    """
    Analyze the recorded data to find resonant frequencies.
    Returns the peaks and their respective amplitudes.
    """
    # Convert recorded data to a numpy array
    audio_data = np.frombuffer(recorded_data, dtype=np.int16)
    peaks, properties = find_peaks(audio_data, height=0.5)
    return peaks, properties['peak_heights']

# Function to refine the scan and determine the exact frequency
def refine_scan(start, end, step):
    print(f"\n Refining scan from {start} Hz to {end} Hz.\n")
    
    max_resonance = 0
    exact_frequency = None
    
    for freq in range(start, end + 1, step):
        print(f"Testing Frequency: {freq} Hz")
        recorded_data = play_and_record(freq, duration, sample_rate)
        if recorded_data is not None:
            resonant_freqs, amplitudes = analyze_response(recorded_data, sample_rate)
            if amplitudes.size > 0:
                current_max = np.max(amplitudes)
                if current_max > max_resonance:
                    max_resonance = current_max
                    exact_frequency = freq
            print(f"Resonant Frequencies: {resonant_freqs}")

    if exact_frequency is not None:
        print(f"\nBest frequency detected: {exact_frequency} Hz with maximum resonance amplitude.\n")
        return exact_frequency
    else:
        print("\nNo significant resonance detected within the specified range.\n")
        return None

# User input for the initial scan range
start_freq = int(input("Enter starting frequency for the first scan (in Hz): "))
end_freq = int(input("Enter ending frequency for the first scan (in Hz): "))

# Initialize max_resonance before the initial scan loop
max_resonance = 0
max_resonance_iteration = None  # Initialize this variable

# Main loop for the initial scan
for i, freq in enumerate(range(start_freq, end_freq, 100)):  # Use enumerate for iteration count
    print(f"Initial Scan - Testing Frequency {freq} Hz")
    recorded_data = play_and_record(freq, duration, sample_rate)
    if recorded_data is not None:
        resonant_freqs, amplitudes = analyze_response(recorded_data, sample_rate)
        if amplitudes.size > 0:
            current_max = np.max(amplitudes)
            if current_max > max_resonance:
                max_resonance = current_max
                max_resonance_iteration = i
        print(f"Resonant Frequencies: {resonant_freqs}")

# Check for resonance and offer user option to continue or exit
if max_resonance_iteration is not None:
    print(f"\n Most resonance at iteration: {max_resonance_iteration} with frequency: {start_freq + 100 * max_resonance_iteration} Hz")
    user_choice = input("\n Continue the scan to tighten range @ 10hz? (y/n): ").lower()
    
    if user_choice == 'y':
        # Narrow the scan range for the second scan based on user input
        refined_start_freq = max(start_freq, start_freq + 100 * (max_resonance_iteration - 1))
        refined_end_freq = min(end_freq, start_freq + 100 * (max_resonance_iteration + 1))
        
        # Second scan with a step of 10 Hz
        second_scan_exact_freq = refine_scan(refined_start_freq, refined_end_freq, 10)
        
        user_choice = input("\n Continue the scan to zero in @ 1hz precision? (y/n): ").lower()
        
        if user_choice == 'y' and second_scan_exact_freq is not None:
            # Third scan based on the best iteration of the second scan
            refined_start_freq = max(refined_start_freq, second_scan_exact_freq - 10)
            refined_end_freq = min(refined_end_freq, second_scan_exact_freq + 10)
            refine_scan(refined_start_freq, refined_end_freq, 1)

else:
    print("No significant resonance detected in the initial scan.")

# Terminate PyAudio
pa.terminate()
