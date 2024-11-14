import pyaudio

audio = pyaudio.PyAudio()
# List available devices to get the correct input device index
for i in range(audio.get_device_count()):
    dev = audio.get_device_info_by_index(i)
    print(f"Index: {i}, Name: {dev['name']}, Max Input Channels: {dev['maxInputChannels']}")

# Replace X with the correct device index found above
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096, input_device_index=X)
