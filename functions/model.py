import os
import time
import subprocess
import speech_recognition as sr 
import pyttsx3 
import pywhatkit
import datetime
import keyboard
import json
import webbrowser
import sympy
import cv2

from functions.volume import set_volume, change_volume
from functions.llm_model import start_talk_chatbot
from functions.vision_model import start_vision_chatbot


def voice_model(language='en-EN', mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    working = True
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    
    if language=='fr-FR':
        print("Apuuyez sur * sur votre clavier pour mettre en pause la conversation")
    else: 
        print("Press * on your keyboard to pause the conversation")

    def talk(text):
        engine.say(text)
        engine.runAndWait()

    def listen():
        command = ''
        try:
            with sr.Microphone(device_index=mic_index) as source:
                print('Assistant :')
                voice = listener.listen(source)
                command = listener.recognize_google(voice, language=language)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return command
    
    def load_sentences():
        sentences = {}
        for filename in os.listdir('json_texts'):
            if filename.endswith('.json'):
                with open(f'json_texts/{filename}', 'r', encoding='utf-8') as f:
                    sentences.update(json.load(f))
        return sentences
    
    def load_app_paths():
        app_paths = {}
        if not os.path.exists('json_files'):
            os.makedirs('json_files')
        for filename in os.listdir('json_files'):
            if filename.endswith('.json'):
                with open(f'json_files/{filename}', 'r', encoding='utf-8') as f:
                    app_paths.update(json.load(f))
        return app_paths
    
    def video_capture():
        if language == 'fr-FR':
            talk("Voulez-vous changer les paramètres par défaut pour la vidéo ?")
        else:
            talk("Do you want to change the default settings for video? (Yes or no)")
        while True:
            user_response = listen().lower()
            if 'oui' in user_response or 'yes' in user_response:
                user_response = 'yes'
                break
            elif 'non' in user_response or 'no' in user_response:
                user_response = 'no'
                break
            else:
                if language == 'fr-FR':
                    talk("Veuillez répondre Oui je veux ou Non je ne veux pas.")
                else:
                    talk("Please answer yes i want or no i don't want.")

        if user_response == 'yes':
            if language == 'fr-FR':
                talk("Veuillez indiquer le numéro de la caméra.")
            else:
                talk("Please indicate the camera number.")
            num_cam_input = listen()
            while not num_cam_input.isdigit():
                if language == 'fr-FR':
                    talk("Veuillez entrer un numéro de caméra valide.")
                else:
                    talk("Please enter a valid camera number.")
                num_cam_input = listen()

            num_cam_command = int(num_cam_input)

            if language == 'fr-FR':
                talk("Veuillez indiquer le FPS.")
            else:
                talk("Please indicate the FPS.")
            fps_input = listen()
            fps_command = int(next((int(s) for s in fps_input.split() if s.isdigit()), 60))

            if language == 'fr-FR':
                talk("Veuillez indiquer le titre de la vidéo.")
            else:
                talk("Please indicate the title of the video.")
            title_video_input = listen()
            title_video_command = title_video_input.strip() or "video_save.mp4"

            num_cam = num_cam_command
            fps = fps_command
            title_video = title_video_command if title_video_command.endswith(".mp4") else title_video_command + ".mp4"
        else:
            num_cam = 0
            fps = 60
            title_video = "video_save.mp4"

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        video_path = os.path.join(desktop_path, title_video)
        cap = cv2.VideoCapture(num_cam)
        if not cap.isOpened():
            if language == 'fr-FR':
                talk("Erreur : Impossible d'ouvrir la caméra.")
            else:
                talk("Error: Unable to open the camera.")
            return

        width = int(cap.get(3))
        height = int(cap.get(4))

        # Set video codec and creator
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        print(f"FPS: {fps}")
        print(f"Video title: {title_video}")
        if language == 'fr-FR':
            talk("Lancement de la vidéo")
        else:
            talk("Video launch")
        while True:
            ret, frame = cap.read()
            if not ret:
                if language == 'fr-FR':
                    print("Erreur lecture de la caméra.")
                else:
                    print("Error reading camera.")
                break

            cv2.imshow("Live video (press 'space' to exit)", frame)
            video_writer.write(frame)
            # Stop video capture when 'space' key is pressed
            if cv2.waitKey(1) == 32:
                break
        cap.release()
        video_writer.release()
        cv2.destroyAllWindows()
        
    def toggle_program(e):
        nonlocal working
        working = not working
        if not working: 
            if language=='fr-FR':
                print("La conversation a été interrompue")
            else: 
                print("The conversation was paused")
        else: 
            if language=='fr-FR':
                print("La conversation reprend")
            else: 
                print("The conversation starts again")
                
    sentences = load_sentences()
    app_paths = load_app_paths()  
    # Sort the keys once at the beginning of the program
    sorted_keys_sentences = sorted(sentences.keys(), key=len, reverse=True)
    sorted_keys_app_paths = sorted(app_paths.keys(), key=len, reverse=True)
    
    chronometer_start_time = None
    keyboard.on_press_key('*', toggle_program)
    while True:
        if working:
            command = listen()
            command = command.lower()
            print(command)
            for key in sorted_keys_sentences:
                # Split the key and command into words
                key_words = key.split()
                command_words = command.split()

                # Check if all words in the key are in the command and in the correct order
                if all(word in command_words[i:] for i, word in enumerate(key_words)):
                    talk(sentences[key])
                    break 

            for path_key in sorted_keys_app_paths:
                # Split the path_key and command into words
                path_key_words = path_key.split()
                command_words = command.split()

                # Check if all words in the path_key are in the command and in the correct order
                if all(word in command_words[i:] for i, word in enumerate(path_key_words)):
                    if language == 'fr-FR':
                        talk("Lancement de l'application " + path_key)
                    else: 
                        talk("Starting the application " + path_key)
                    subprocess.Popen(app_paths[path_key], shell=True)
                    break
                    
            # Launch Local LLM (use Ollama) 
            llm_start_keywords = ['passe en mode précision', 'passe en précision', 'passage en mode précision',
                                  'switch to precision mode', 'switch to precision'
                                 ]
            if any(keyword in command for keyword in llm_start_keywords):
                with open('params.txt', 'r') as f:
                    lines = f.readlines()
                    language = lines[0].strip()
                    mic_index = int(lines[1].strip())
                    voice_id = lines[2].strip()
                    llm_model = lines[3].strip()
                if language == 'fr-FR':
                    talk("Passage en mode LLM Local sur seveur Ollama")
                else: 
                    talk("Switching to LLM Local mode on Ollama server")
                start_talk_chatbot(llm_model, language, mic_index, voice_id)
                continue
            
            # Launch Local Vision LLM (use Ollama) 
            llm_vision_start_keywords = ['passe en mode analyse', 'passe en analyse', 'passage en mode analyse', 'passage en mode vision',
                                  'passage en vision', 'passe en vision', 'passe en mode vision', 'switch to analysis mode', 
                                  'switch to analyse', 'switch to vision', 'switch to vision mode', 'switch to analysis', 'switch to analyse mode', 
                                 ]
            if any(keyword in command for keyword in llm_vision_start_keywords):
                with open('params.txt', 'r') as f:
                    lines = f.readlines()
                    language = lines[0].strip()
                    mic_index = int(lines[1].strip())
                    voice_id = lines[2].strip()
                    llm_vision_model = lines[4].strip()
                if language == 'fr-FR':
                    talk("Passage en mode LLM Vision sur seveur Ollama")
                else: 
                    talk("Switching to Vision LLM on Ollama server")
                start_vision_chatbot(llm_vision_model, language, mic_index, voice_id)
                continue
            
            # Open Text Edit and take note
            text_note_keywords = ['prends note', 'take note']
            for keyword in text_note_keywords:
                if keyword in command:
                    if language == 'fr-FR':
                        talk("C'est noté")
                    else: 
                        talk("Noted")
                    command = command.replace(keyword, '').strip()
                    desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
                    file_path = os.path.join(desktop, 'vocal_note.txt')
                    # Check if file is empty or not
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        with open(file_path, 'a', encoding="utf-8") as f:
                            f.write('\n' + command)
                    else:
                        with open(file_path, 'a', encoding="utf-8") as f:
                            f.write(command)
                    
            # Calcul
            calc_keywords = ['calcule', 'calcul', 'compute', 'calculate']
            if any(keyword in command for keyword in calc_keywords):
                calc_command = command.replace('calcule', '').replace('calcul', '').replace('compute', '').replace('calculate', '')
                calc_command = calc_command.replace('x', '*').replace(',', '.')
                try:
                    result = sympy.sympify(calc_command)
                    result = round(result, 2)
                    if language == 'fr-FR':
                        talk(f"Cela fait {result}")
                    else: 
                        talk(f"This makes {result}")
                except Exception as e:
                    if language == 'fr-FR':
                        talk("Désolé, je n'ai pas pu effectuer le calcul.")
                    else:
                        talk("Sorry, I couldn't do the calculation.")
                continue
            
            # Start Chronometer
            start_chronometer_keywords = ['démarre le chronomètre', 'start the chronometer']
            stop_chronometer_keywords = ['arrête le chronomètre', 'stop the chronometer']
            if any(keyword in command for keyword in start_chronometer_keywords):
                if language == 'fr-FR':
                    chronometer_start_time = time.time()
                    talk("Chronomètre démarré.")
                else:
                    chronometer_start_time = time.time()
                    talk("Chronometer started.")
            elif any(keyword in command for keyword in stop_chronometer_keywords) and chronometer_start_time is not None:
                elapsed_time = time.time() - chronometer_start_time
                if language == 'fr-FR':
                    talk(f"Chronomètre arrêté, temps écoulé : {round(elapsed_time, 2)} secondes")
                    print(f"Chronomètre arrêté, temps écoulé : {round(elapsed_time, 2)} secondes")
                else:
                    talk(f"Chronometer stopped, time elapsed: {round(elapsed_time, 2)} seconds")
                    print(f"Chronometer stopped, time elapsed: {round(elapsed_time, 2)} seconds")
                chronometer_start_time = None
                
            # Start Video
            start_video_keywords = ['je veux que tu filmes', 'commence une vidéo',
                                    'i want you to film', 'start video', 'start a video']             
            if any(keyword in command for keyword in start_video_keywords):
                video_capture()
                continue
                            
            # YouTube
            youtube_keywords = ['cherche sur youtube', 'recherche sur youtube', 'find on youtube', 'find in youtube']
            if any(keyword in command for keyword in youtube_keywords):
                ytb_command = command.replace('Open YouTube and find', '')
                talk(ytb_command)
                pywhatkit.playonyt(ytb_command)
                continue
                
            # Google
            google_keywords = ['cherche sur google', 'recherche sur google', 'find on google', 'find in google']
            for keyword in google_keywords:
                if keyword in command:
                    search = command.replace(keyword, '').strip()
                    if search.startswith('re '):
                        search = search[3:]
                    url = "https://www.google.com/search?q=" + search
                    webbrowser.open(url)
                    break

            # Wikipedia
            wikipedia_keywords = ['cherche sur wikipédia', 'recherche sur wikipédia', 'find on wikipedia', 'find in wikipedia']
            for keyword in wikipedia_keywords:
                if keyword in command:
                    search = command.replace(keyword, '').strip()
                    if search.startswith('re '):
                        search = search[3:]
                    url = "https://fr.wikipedia.org/wiki/" + search
                    webbrowser.open(url)
                    break
                    
            # Bing
            bing_keywords = ['cherche sur bing', 'recherche sur bing', 'find on bing', 'find in bing']
            for keyword in bing_keywords:
                if keyword in command:
                    search = command.replace(keyword, '').strip()
                    if search.startswith('re '):
                        search = search[3:]
                    url = "https://www.bing.com/search?q=" + search
                    webbrowser.open(url)
                    break
                
            # Chat GPT
            openai_keywords = ['ouvre chat ia', 'recherche sur chat ia', 'search on ai chat', 
                               'cherche sur chat ia', 'search in ai chat', 'start ai chat']
            if any(keyword in command for keyword in openai_keywords):
                url = "https://chat.openai.com/"
                webbrowser.open(url)
                continue
                
            # Current Time
            detect_time_keywords = ['quelle heure est-il', 'l\'heure actuelle', 'what time is it']
            if any(keyword in command for keyword in detect_time_keywords):
                talk(datetime.datetime.now().strftime('%H:%M:%S'))
                continue
            
            # Current Date
            detect_datetime_keywords = ['date actuelle', 'date d\'aujourd\'hui',
                                        'current date', 'today\'s date', 'date of today'
                                        ]
            if any(keyword in command for keyword in detect_datetime_keywords):
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime('%A %d %B %Y - %H:%M')
                talk(formatted_datetime)
                continue
            
            # IP Config
            ip_keywords = ['quel est mon ip', 'mon ip', 'my ip', 'what is my ip', 'what\'s my ip']
            if any(keyword in command for keyword in ip_keywords):
                subprocess.Popen('cmd /k "ipconfig"')
                continue

            # System Info
            sys_info_keywords = ['informations sur mon système', 'informations système', 
                                'informations of my system', 'informations system']
            if any(keyword in command for keyword in sys_info_keywords):
                subprocess.Popen('cmd /k "systeminfo"')
                continue
            
            # Volume Mute
            mute_keywords = ['mute', 'silence']
            if any(keyword in command for keyword in mute_keywords):
                talk('Mute')
                set_volume(0.0)
                continue
            
            # Volume deMute
            demute_keywords = ['des mute', 'remets le volume', 'demute', 'de mute']
            if any(keyword in command for keyword in demute_keywords):
                if language == 'fr-FR':
                    talk('Volume remis')
                else: 
                    talk('Volume restarted')
                set_volume(0.5)
                continue
            
            # Volume Increase
            volume_increase_keywords = ['augmente le volume', 'monte le volume', 'increase the volume']
            if any(keyword in command for keyword in volume_increase_keywords):
                if language == 'fr-FR':
                    talk('Volume augmenté')
                else: 
                    talk('Volume increased')
                change_volume(0.2)
                continue
                            
            # Volume Decreases
            volume_decrease_keywords = ['diminue le volume', 'descend le volume', 'decreases the volume']
            if any(keyword in command for keyword in volume_decrease_keywords):
                if language == 'fr-FR':
                    talk('Volume diminué')
                else: 
                    talk('Volume decreased')
                change_volume(-0.2)
                continue    
            
            # Pause Conversation
            pause_keywords = ['pause']
            if any(keyword in command for keyword in pause_keywords):
                if language == 'fr-FR':
                    talk('La conversation a été interrompue')
                else: 
                    talk('The conversation was paused')
                toggle_program(working)
                continue
                                
            # Stop Conversation
            stop_keywords = ['stoppe notre discussion', 'stoppe notre conversation', 'stoppe la discussion', 'stoppe la conversation',
                            'stop our discussion', 'stop our conversation', 'stop the discussion', 'stop the conversation',
                            ]
            if any(keyword in command for keyword in stop_keywords):
                working = False
                break