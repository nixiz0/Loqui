import csv
import pyttsx3
import speech_recognition as sr
import requests
import json
import os
import keyboard


def start_talk_chatbot(model, language="en-EN", mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    url = "http://localhost:11434/api/chat"
    headers = {'Content-Type': "application/json",}
    conversation_history = []
    working = True
        
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
        
    # Set the selected voice
    engine.setProperty('voice', voice_id)

    # Initialize the voice recognizer
    recognizer = sr.Recognizer()

    def beforeSay(response):
        return response

    def say(response):
        if len(response) == 0:
            return
        engine.say(beforeSay(response))
        engine.runAndWait()

    def generate_response(prompt, chat_history):
        if len(prompt) == 0:
            return "", chat_history

        full_prompt = []
        for i in chat_history:
            full_prompt.append({
                "role": "user",
                "content": i[0]
            })
            full_prompt.append({
                "role": "assistant",
                "content": i[1]
            })
        full_prompt.append({
            "role": "user",
            "content": prompt
        })

        data = {
            "model": model,
            "stream": True,
            "messages": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        if response.status_code == 200:
            print('\nAssistant:', end='')
            all_response = ''
            this_response = ''
            for line in response.iter_lines():
                if line:
                    jsonData = json.loads(line)
                    this_response += jsonData["message"]['content']
                    if '.' in this_response or '?' in this_response or '!' in this_response:
                        print(f'{this_response}', end='')
                        say(this_response)
                        all_response += this_response
                        this_response = ''
            if len(this_response) > 0:
                print(f'{this_response}', end='')
                say(this_response)
                all_response += this_response
                this_response = ''
            chat_history.append((prompt, all_response))

            return "", chat_history
        else:
            return "Error: Unable to fetch response", chat_history

    def save_conversation(conversation_history):
        filename = f"conversation_history.csv"
        with open(os.path.join(os.path.expanduser('~'), 'Downloads', filename), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Assistant"])
            for chat in conversation_history:
                writer.writerow([chat[0], chat[1]])
                
    if language=='fr-FR':
        print("Apuuyez sur * sur votre clavier pour mettre en pause la conversation")
    else: 
        print("Press * on your keyboard to pause the conversation")
        
    def toggle_program(e):
        nonlocal working
        working = not working

    keyboard.on_press_key('*', toggle_program)
    while True:
        if working:
            with sr.Microphone(device_index=mic_index) as source:
                print("\nListening (precision LLM mode)...")
                audio = recognizer.listen(source)

                try:
                    # Recognize user voice
                    user_input = recognizer.recognize_google(audio, language=language)
                    user_input = user_input.lower()
                    print("\nUser: " + user_input)
                    
                    # Check if the user wants to save the conversation
                    detect_save_keyords = ['sauvegarde notre discussion', 'sauvegarde notre conversation', 'sauvegarde la discussion', 'sauvegarde la conversation',
                                            'save our discussion', 'save our conversation', 'save the discussion', 'save the conversation',
                                            ]
                    if any(keyword in user_input for keyword in detect_save_keyords):
                        if language=='fr-FR':
                            engine.say("La conversation a été sauvegardé")
                        else: 
                            engine.say("The conversation has been saved")
                        print("Conversation saved.")
                        save_conversation(conversation_history)
                        continue

                    # Check if the user wants to stop the LLM conversation for return to basic voice detection
                    detect_stop_llm_keyords = ['désactive llm', 'passe en mode classique', 'passage en mode classique',
                                            'disable llm', 'switch to classic mode', 'switch classic mode']
                    if any(keyword in user_input for keyword in detect_stop_llm_keyords):
                        if language=='fr-FR':
                            engine.say("Passage en mode exécution de commandes")
                        else: 
                            engine.say("Switching to commands execution mode")
                        engine.runAndWait()
                        print("Stopping the conversation with the LLM.")
                        break

                    # Generate a response
                    user_input_str = str(user_input)
                    _, chat_history = generate_response(user_input_str, conversation_history)

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))