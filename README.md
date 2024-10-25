# Toney The Tiger Resonant Frequency Scanner/Detector

## Disclaimer

Testing resonant frequencies can pose potential risks like damage to nearby objects, structures, equipment, and even possibly your own body. Extreme caution should be taken to ensure the safety of your environment before running scans, especially in the presence of fragile or complex equipment. The creator of this tool is not responsible for any damages, injuries, or consequences resulting from its use. Please ensure responsible experimentation in controlled environments. Do NOT run this without knowing what you are doing. By using this software you agree to accept all responsibility for the outcomes.

---

## Overview

**Toney The Tiger Resonant Frequency Scanner** is a Python tool designed to detect resonant frequencies in objects within a specified range. 

### Microphone and Speaker Usage
The scanner works by:
1. **Speaker Output**: Playing sine wave tones through the system's audio output, such as external speakers, to project sound at different frequencies.
2. **Microphone Input**: Recording the system's response to these tones using a microphone, which detects any resonant frequencies created by the object being tested.

### Microphone and Speaker Placement
To maximize the accuracy of frequency detection, you should consider the following when placing the microphone and speakers:
- **Environment**: Conduct the tests in a quiet environment to minimize noise interference that could affect the analysis.
- **Object Testing**: Position the microphone and speaker close to the object, ensuring the microphone can pick up any reflected sound waves caused by resonant frequencies. Make the microphone face the object at an angle away from the direct path of the speaker to avoid overwhelming the reading. You want to capture the sound of the object vibrating. (A sound shield between the microphone and speaker can help, as long as it does not shield the path from speaker to object and object to microphone.) 
  
Proper placement is essential for accurate resonant frequency detection. A poorly placed microphone or speaker could lead to misreadings or insufficient data capture. 
The quality and choice of equipment is also a huge factor.

## Parameters
- **Start Frequency**: Starting frequency of the scan (in Hz).
- **End Frequency**: Ending frequency of the scan (in Hz).
- **Duration**: Tone duration (in seconds).
- **Sample Rate**: Audio sampling rate (in Hz).

## How It Works
1. **Setup**: Provide the start and end frequencies.
2. **Scan**: The program generates and plays tones for each frequency in the range.
3. **Record and Analyze**: The system response is recorded via the microphone, and peaks in the signal are identified.
4. **Refinement**: If resonance is detected, the scan can be refined with smaller frequency steps (10 Hz or 1 Hz).

To be clear: It will narrow down the resonant frequency of the tested object to an accuracy of +/- 1 Hz.

## Requirements
Ensure the following Python libraries are installed:
- `numpy`: For generating sine waves and handling data.
- `pyaudio`: For audio playback and recording.
- `scipy`: For peak detection in the recorded data.

Install the required packages with:
```
pip install numpy pyaudio scipy
```
Recommendation: Use a Python Virtual Environment (venv)
Note: If default devices are not being detected, make sure pulse audio is running (linux)


Thanks for your interest in my work! 
ionnoim@proton.me
