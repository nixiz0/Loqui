import csv
import pyttsx3
import speech_recognition as sr
import requests
import json
import os
import keyboard


def start_talk_chatbot(model, language="en-EN", mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': "application/json",}
    conversation_history = []
    working = True
        
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
        
    # Set the selected voice
    engine.setProperty('voice', voice_id)

    # Initialize the voice recognizer
    recognizer = sr.Recognizer()

    def generate_response(prompt, chat_history):
        conversation_history.append(prompt)
        full_prompt = "\n".join(map(str, conversation_history))

        data = {
            "model": model,
            "stream": False,
            "prompt": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            chat_history.append((prompt, actual_response))

            # Read response to user
            engine.say(actual_response)
            engine.runAndWait()

            return "", chat_history
        else:
            return "Error: Unable to fetch response", chat_history

    def save_conversation(conversation_history):
        filename = f"conversation_history.csv"
        with open(os.path.join(os.path.expanduser('~'), 'Downloads', filename), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Model"])
            for index in range(0, len(conversation_history), 2):
                user = conversation_history[index]
                model = conversation_history[index + 1] if index + 1 < len(conversation_history) else ""
                writer.writerow([user, model])
                
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
                print("Listening...")
                audio = recognizer.listen(source)

                try:
                    # Recognize user voice
                    user_input = recognizer.recognize_google(audio, language=language)
                    user_input = user_input.lower()
                    print("User: " + user_input)
                    
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