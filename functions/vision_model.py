import os
import re
import cv2
import keyboard
import pyautogui
import pyttsx3
import speech_recognition as sr
from word2number import w2n 
import requests 
import base64 
import json 
import time


def start_vision_chatbot(model, language="en-EN", mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': "application/json",}
    vision_history = []
    working = True
        
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
        
    # Set the selected voice
    engine.setProperty('voice', voice_id)

    # Initialize the voice recognizer
    recognizer = sr.Recognizer()

    def encode_image_to_base64(image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(image_path, custom_prompt):
        vision_history.append(custom_prompt)
        image_base64 = encode_image_to_base64(image_path)
        
        payload = {
            "model": model,
            "prompt": custom_prompt,
            "images": [image_base64]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        try: 
            response_lines = response.text.strip().split('\n')
            full_response = ''.join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))
            
            # Read response to user
            engine.say(full_response)
            engine.runAndWait()
            
            return full_response
        except Exception as e: 
            return f"Error: {e}"

    def capture_screenshot():
        if not os.path.exists('photos'):
            os.makedirs('photos')
        screenshot = pyautogui.screenshot()
        screenshot.save(r'photos/screenshot.png')

    def capture_camera(camera_index):
        if not os.path.exists('photos'):
            os.makedirs('photos')
        cap = cv2.VideoCapture(int(camera_index))
        ret, frame = cap.read()
        time.sleep(1)
        cv2.imwrite('photos/camera.png', frame)
        cap.release()

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
                print("Listening (vision LLM mode)...")
                audio = recognizer.listen(source)
                try:
                    user_input = recognizer.recognize_google(audio, language=language)
                    user_input = user_input.lower()
                    print("User: " + user_input)
                        
                     # Check if the user wants to stop the LLM Vision for return to basic voice detection
                    detect_stop_llm_keyords = ['désactive llm', 'passe en mode classique', 'passage en mode classique',
                                            'disable llm', 'switch to classic mode', 'switch classic mode']
                    if any(keyword in user_input for keyword in detect_stop_llm_keyords):
                        if language=='fr-FR':
                            engine.say("Passage en mode exécution de commandes")
                        else: 
                            engine.say("Switching to commands execution mode")
                        engine.runAndWait()
                        print("Stopping the vision with the model.")
                        break
                        
                    if "screenshot" in user_input or "screen" in user_input:
                        capture_screenshot()
                        if language == 'fr-FR':
                            engine.say("Screenshot effectué.")
                        else:
                            engine.say("Screenshot taken.")
                        engine.runAndWait()
                        image_path = 'photos/screenshot.png'
                    elif "camera" in user_input or "caméra" in user_input or "cam" in user_input:
                        camera_index = None
                        while camera_index is None:
                            if language == 'fr-FR':
                                engine.say("Veuillez indiquer le numéro de la caméra.")
                            else:
                                engine.say("Please indicate the camera number.")
                            engine.runAndWait()
                            print("Listening Num Cam...")
                            audio = recognizer.listen(source)
                            user_input = recognizer.recognize_google(audio, language=language)
                            match = re.search(r'\d+', user_input)
                            if match:
                                camera_index = int(match.group())
                            else:
                                try:
                                    camera_index = w2n.word_to_num(user_input)
                                except ValueError:
                                    continue
                            capture_camera(camera_index)
                            if language == 'fr-FR':
                                engine.say("Photo prise.")
                            else:
                                engine.say("Photo taken.")
                            engine.runAndWait()
                            image_path = 'photos/camera.png'
                    else:
                        continue

                    if language == 'fr-FR':
                        engine.say("Dites moi ce que je dois faire avec cette image ?")
                    else:
                        engine.say("Tell me what I should do with this image ?")
                    engine.runAndWait()
                    try:
                        print("Listening Do With Image...")
                        audio = recognizer.listen(source)
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    custom_prompt = recognizer.recognize_google(audio, language=language)
                    analyze_image(image_path, custom_prompt)
                    
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))