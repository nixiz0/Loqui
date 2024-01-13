import os
import subprocess
import speech_recognition as sr 
import pyttsx3 
import pywhatkit
import datetime
import keyboard
import json
import webbrowser

from functions.volume import set_volume, change_volume
from functions.llm_model import start_talk_chatbot


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
        for filename in os.listdir('json_files'):
            if filename.endswith('.json'):
                with open(f'json_files/{filename}', 'r', encoding='utf-8') as f:
                    app_paths.update(json.load(f))
        return app_paths
    
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

    keyboard.on_press_key('*', toggle_program)
    while True:
        if working:
            sentences = load_sentences()
            app_paths = load_app_paths()
            command = listen()
            command = command.lower()
            print(command)
            for key in sentences.keys():
                # Split the key and command into words
                key_words = key.split()
                command_words = command.split()
                
                # Check if all words in the key are in the command and in the correct order
                if all(word in command_words[i:] for i, word in enumerate(key_words)):
                    talk(sentences[key])
                    
            for path_key in app_paths.keys():
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
                    url = "https://www.google.com/search?q=" + search
                    webbrowser.open(url)
                    break

            # Wikipedia
            wikipedia_keywords = ['cherche sur wikipédia', 'recherche sur wikipédia', 'find on wikipedia', 'find in wikipedia']
            for keyword in wikipedia_keywords:
                if keyword in command:
                    search = command.replace(keyword, '').strip()
                    url = "https://fr.wikipedia.org/wiki/" + search
                    webbrowser.open(url)
                    break
                    
            # Bing
            bing_keywords = ['cherche sur bing', 'recherche sur bing', 'find on bing', 'find in bing']
            for keyword in bing_keywords:
                if keyword in command:
                    search = command.replace(keyword, '').strip()
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