
# Loqui

![Loqui Logo](ressources/logo_loqui.png)

Application allowing you to configure a text and a voice response, also allows you to open your applications with a chosen text trigger.
## Installation

=> You need to install **Python 3.11**

1-/ Clone this repository ```git clone https://github.com/nixiz0/DrawItium.git```

2-/ Create your environment ```python -m venv .env```

3-/ Download required libraries ```pip install -r requirements.txt```

4-/ Run the menu.py ```python main.py```
## Loqui Add Data
![Add Data Illustration](ressources/add_data.png)

To add the text trigger and response for this text you want to the model you must :
- Put in **'Trigger Phrase'** the sentence that you want for trigger the model.
- Put in **'Response'** the response you want the pattern to say after saying the trigger phrase.
- Don't forget to **'Submit'** to put the data on the model.

To add an Application you must :
- Click on the **Add Application** button then in the file explorer you must search for the application or file you want to launch.
- In the **'Application Key'** input you will have the name of this application which will serve as a trigger phrase.
- If you want to change this name with a phrase or word that you want to use to trigger the opening of the application by saying this word orally, you just have to mark the new name you want in **'New Key Name'** and click on the **'Rename'** button to save the modification.

## Loqui Start the Model
![Start Model Illustration](ressources/start_model.png)

To launch the model you must :
- Select a Language, it's important because if you select the wrong language the voice recognition algorithm will not recognize the words well.
- By default the main microphone used by Windows will be used but you can choose from all your microphones (if you have several) the one you want to use to speak with.
- You can choose from the list of your synthetic voices that are in your operating system the voice you want to use.
## To have more Synthetic Voices Available (on Windows)

![Synthetic Voices Illustration](ressources/list_example_voices.png)

If you want to have more synthetic voices available, on Windows you have to go to the narrator settings and you can download the voices you want.

If this doesn't work and doesn't recognize the voices you have installed on the narrator settings, follow this steps :
1. Open the **Registry Editor** by pressing the **“Windows” and “R”** keys simultaneously, then type **“regedit”** and press Enter.

2. Navigate to the registry key : **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens**.

3. Export this key to a **REG file** (with a right click on the file).

4. Open this file with a text editor and replace all occurrences of **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens** 
with **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens**.

5. Save the modified file and double-click it to import the changes to the registry.


## Vocal Commands

The application integrates several features allowing you to execute commands with voice recognition, here are all the commands and their trigger phrases that you can use :

**Launch and search on YouTube if you say:**  
['recherche sur youtube', 'find on youtube', 'find in youtube']

**on Google:**  
['recherche sur google', 'find on google', 'find in google']

**on Wikipedia:**  
['recherche sur wikipédia', 'find on wikipedia', 'find in wikipedia']

**on Bing:**  
['recherche sur bing', 'find on bing', 'find in bing']

**Launch Chat-GPT:**  
['ouvre chat ia', 'recherche sur chat ia', 'search on ai chat', 'search in ai chat', 'start ai chat']

**Gives you the current Time:**
['quelle heure est-il', 'l\'heure actuelle', 'what time is it']

**Gives you the current Date:**
['date actuelle', 'date d\'aujourd\'hui', 'current date', 'today\'s date', 'date of today']

**Gives you info on your IP Address:**
['quel est mon ip', 'mon ip', 'my ip', 'what is my ip', 'what\'s my ip']

**Gives you info on your system:**
['informations sur mon système', 'informations système', 'informations of my system', 'informations system']

**Mute Volume in your computer:**
['mute', 'silence']

**DeMute Volume:**
['des mute', 'remets le volume', 'demute', 'de mute']

**Increases Volume:**
['augmente le volume', 'monte le volume', 'increase the volume']

**Decreases Volume:**
['diminue le volume', 'descend le volume', 'decreases the volume']

**Stop the Conversation:**
['stoppe notre discussion', 'stoppe notre conversation', 'stoppe la discussion', 'stoppe la conversation', 'stop our discussion', 'stop our conversation', 'stop the discussion', 'stop the conversation']
## Tech Stack

**Voice Recognition:** speech_recognition

**Audio Device Scanning:** pyaudio

**Synthetic Voices:** pyttsx3

**Interface:** Tkinter

**Computer Commands:** webbrowser (search on web) / pywhatkit (search on youtube) / pycaw (change volume computer)
## Author

- [@nixiz0](https://github.com/nixiz0)

