import av

print("PyAV version:", av.__version__)

with av.open("farmer_hindi_test.wav") as container:
    print("Audio opened successfully!")