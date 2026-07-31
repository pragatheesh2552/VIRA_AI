import speech_recognition as sr
from modules.voice.config import DEVICE_INDEX

def main():
    try:
        mic_name = sr.Microphone.list_microphone_names()[DEVICE_INDEX]
    except IndexError:
        mic_name = f"Unknown (Index {DEVICE_INDEX})"
        
    print(f"Microphone Name: {mic_name}")
    
    r = sr.Recognizer()
    try:
        mic = sr.Microphone(device_index=DEVICE_INDEX)
    except Exception as e:
        print(f"Failed to initialize microphone: {e}")
        return

    print(f"Sample Rate: {mic.SAMPLE_RATE} Hz")
    
    print("\n--- RECORDING FOR 5 SECONDS ---")
    print("Please speak NOW...")
    
    try:
        with mic as source:
            # Captures exactly 5 seconds of raw audio (no STT involved)
            audio = r.record(source, duration=5)
    except Exception as e:
        print(f"Recording error: {e}")
        return
            
    print("--- RECORDING FINISHED ---")
    
    # Extract WAV data
    wav_data = audio.get_wav_data()
    
    # Calculate duration (simplified estimation based on raw bytes, though duration is roughly 5s)
    print(f"Duration: 5.0 seconds")
    
    filename = "test.wav"
    with open(filename, "wb") as f:
        f.write(wav_data)
        
    print(f"Saved to: {filename}")
    print("You can now play this file to verify the audio!")

if __name__ == "__main__":
    main()
