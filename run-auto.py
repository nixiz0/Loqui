from functions.model import voice_model


def main():
    with open('params.txt', 'r') as f:
        lines = f.readlines()
        language = lines[0].strip()
        mic_index = int(lines[1].strip())
        voice_id = lines[2].strip()

    voice_model(language, mic_index, voice_id)

if __name__ == "__main__":
    main()