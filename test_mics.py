import pyaudio
import wave
import time

def record_mic(index, duration=5):
    p = pyaudio.PyAudio()
    
    try:
        info = p.get_device_info_by_index(index)
        name = info.get('name', 'Unknown')
    except Exception as e:
        print(f"Could not get info for index {index}: {e}")
        p.terminate()
        return

    print(f"\n=============================================")
    print(f"Testing Microphone Index: {index}")
    print(f"Name: {name}")
    print(f"=============================================")
    
    channels = 1
    # Check max input channels
    if info.get('maxInputChannels', 0) < 1:
        print(f"Device {index} has no input channels. Skipping.")
        p.terminate()
        return
        
    rate = int(info.get('defaultSampleRate', 44100))
    chunk = 1024
    audio_format = pyaudio.paInt16

    print(f"Recording for {duration} seconds... Please speak now!")
    
    try:
        stream = p.open(format=audio_format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        input_device_index=index,
                        frames_per_buffer=chunk)
        
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        print("Recording finished.")
        
        filename = f"mic_{index}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            
        print(f"Saved to {filename}")
        
    except Exception as e:
        print(f"Error recording from index {index}: {e}")
        
    finally:
        p.terminate()
        
def main():
    indexes_to_test = [1, 9, 13]
    for idx in indexes_to_test:
        record_mic(idx)
        print("Waiting 2 seconds before next test...\n")
        time.sleep(2)
        
    print("\nAll tests complete! Please check the output wav files.")

if __name__ == "__main__":
    main()
