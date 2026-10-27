from voice.whisper_recognizer import WhisperSpeechRecognizer


recognizer = WhisperSpeechRecognizer(
    model_size="tiny",
    device="cpu",
    compute_type="int8",
)

text = recognizer.listen(duration=4)

print()
print("Recognized:", text)