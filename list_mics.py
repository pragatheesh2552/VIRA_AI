import speech_recognition as sr

print("\n=====================================")
print("Available Microphones and their Index")
print("=====================================")

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"[{index}] -> {name}")

print("=====================================\n")
