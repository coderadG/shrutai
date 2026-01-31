import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    
    print("\n--- Available Audio Input Devices ---")
    print(f"{'Index':<7} | {'Device Name'}")
    print("-" * 40)
    
    # Iterate through all available audio devices
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        
        # We only care about devices that have 'input' channels (microphones)
        if info.get('maxInputChannels') > 0:
            name = info.get('name')
            print(f"{i:<7} | {name}")
            
    p.terminate()
    print("-" * 40)
    print("Look for 'iPhone Microphone' and note the Index number.\n")

if __name__ == "__main__":
    try:
        list_audio_devices()
    except Exception as e:
        print(f"Error: {e}")