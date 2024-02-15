from pocketsphinx import LiveSpeech

def main():
    model_path = r"C:\Users\andok\Downloads\Whizzy\model\en-us"
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=16000,
        no_search=False,
        full_utt=False,
        hmm=model_path,
        lm=f"{model_path}/en-us.lm.bin",
        dic=f"{model_path}/cmudict-en-us.dict"
    )

    wake_word = "hey whizzy"

    print("Listening for the wake word...")

    for phrase in speech:
        print(f"You said: {phrase}")

        if wake_word in str(phrase).lower():
            print("Wake word detected! Recognized!")

if __name__ == "__main__":
    main()
