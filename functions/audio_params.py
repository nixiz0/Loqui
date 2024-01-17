import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pyaudio
import pyttsx3
import webbrowser


def callback(url):
    webbrowser.open_new(url)
    
def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return {voice.name: voice.id for voice in voices}

def audio_ai_params():
    mic_index = tk.IntVar()
    mic_index.set(0)
    voice_id = tk.StringVar()
    voice_id.set('')
    voice_dict = get_voices()
    llm_model = tk.StringVar()
    llm_vision_model = tk.StringVar()
    def on_ok_audio_click():
        selected_language = language.get()
        if mic_index and voice_id and selected_language:
            start_web_sep_shell(selected_language, mic_index.get(), voice_id.get())
            messagebox.showinfo("Start", f"Starting the Assistant with Micro : {mic_index.get()}, Language : {selected_language}, Voice : {voice_id.get()}")
            dialog.destroy()
        elif not mic_index:
            messagebox.showwarning("No microphone selected", "Please select a microphone before continuing.")
        elif not voice_id:
            messagebox.showwarning("No voice selected", "Please select a voice before continuing.")
        elif not selected_language:
            messagebox.showwarning("No language selected", "Please select a language before continuing.")
        else:
            messagebox.showwarning("No microphone and voice selected", "Please select a microphone and a voice before continuing.")
            
        if llm_model:
            with open('params.txt', 'a') as f:
                f.write(f'{llm_model.get()}\n')
                
        if llm_vision_model: 
            with open('params.txt', 'a') as f:
                f.write(f'{llm_vision_model.get()}\n')

    def start_web_sep_shell(language, mic_index, voice_id):
        with open('params.txt', 'w') as f:
            f.write(f'{language}\n{mic_index}\n{voice_id}\n')
        command = f'python -c "from functions.model import voice_model; voice_model(\'{language}\', {int(mic_index)}, \'{voice_id}\')"'
        subprocess.Popen(command, shell=True)

    def show_mic_list():
        p = pyaudio.PyAudio()
        mic_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                # Check if the device is available and active
                if device_info['hostApi'] == p.get_default_host_api_info()['index'] and device_info['maxInputChannels'] > 0:
                    mic_list.append(device_info['name'])
        p.terminate()

        mic_list_dialog = tk.Toplevel()
        mic_list_dialog.title("Microphone List")

        # Create a canvas inside the dialog
        canvas = tk.Canvas(mic_list_dialog, width=290, height=200, background='#ffffff')
        scrollbar = ttk.Scrollbar(mic_list_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Bind the canvas's height to the scrollable frame's height
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, mic_name in enumerate(mic_list):
            mic_button = tk.Button(scrollable_frame, text=mic_name, command=lambda idx=idx: select_mic(idx), font=("Inter", 12))
            mic_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_mic(index):
        # Selected mic_index
        mic_index.set(index)
        print(f"Selected Microphone Index: {index}")
        
    def show_voice_list():
        voice_list_dialog = tk.Toplevel()
        voice_list_dialog.title("Voice List")

        # Create a canvas inside the dialog
        canvas = tk.Canvas(voice_list_dialog, width=360, height=360, background='#ffffff')
        scrollbar = ttk.Scrollbar(voice_list_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Bind the canvas's height to the scrollable frame's height
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for voice_name in voice_dict.keys():
            voice_button = tk.Button(scrollable_frame, text=voice_name, command=lambda voice_name=voice_name: select_voice(voice_name), font=("Inter", 12))
            voice_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_voice(voice_name):
        # Selected voice_id
        voice_id.set(voice_dict[voice_name])
        print(f"Selected Voice ID: {voice_dict[voice_name]}")

    dialog = tk.Toplevel()
    dialog.geometry("400x470")
    dialog.minsize(350, 460)
    dialog.maxsize(420, 480)

    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'+{x}+{y}')
    
    font_style = ("Helvetica", 15)
    
    dialog.title("Loqui Start")

    dialog.option_add("*Font", font_style)

    dialog.configure(background="#333333")
    dialog.tk_setPalette(background="#333333", foreground="white")

    languages = ["fr-FR", "en-EN"]
    language = tk.StringVar()

    languages_label = ttk.Label(dialog, text="Select Language:", foreground="white", background="#333333")
    languages_label.pack(pady=(15, 1))
    languages_dropdown = ttk.Combobox(dialog, textvariable=language, values=languages, state="readonly")
    languages_dropdown.pack()

    mic_list_button = ttk.Button(dialog, text="Microphone List", command=show_mic_list)
    mic_list_button.pack(pady=5)
    
    voice_list_button = ttk.Button(dialog, text="Voice List", command=show_voice_list)
    voice_list_button.pack(pady=5)
    
    tk.Frame(dialog, height=3, bg="white").pack(fill=tk.X, padx=5, pady=5)
    
    llm_label = ttk.Label(dialog, text="Enter LLM model (optional) :", foreground="white", background="#333333")
    llm_label.pack()
    model_link = tk.Label(dialog, text="List of models", fg="blue", cursor="hand2", foreground="cyan", background="#333333")
    model_link.pack(pady=5)
    model_link.bind("<Button-1>", lambda e: callback("https://ollama.ai/library"))
    
    model_entry = ttk.Entry(dialog, textvariable=llm_model)
    model_entry.pack()
    
    tk.Frame(dialog, height=1, bg="white").pack(fill=tk.X, padx=5, pady=5)
    
    llm_vision_label = ttk.Label(dialog, text="Enter Vision LLM model (optional) :", foreground="white", background="#333333")
    llm_vision_label.pack()
    model_vision_link = tk.Label(dialog, text="Vision models", fg="blue", cursor="hand2", foreground="cyan", background="#333333")
    model_vision_link.pack(pady=5)
    model_vision_link.bind("<Button-1>", lambda e: callback("https://ollama.ai/library?q=llava"))
    
    model_vision_entry = ttk.Entry(dialog, textvariable=llm_vision_model)
    model_vision_entry.pack()

    ok_button = ttk.Button(dialog, text="OK", command=on_ok_audio_click)
    ok_button.pack(pady=5)
    dialog.bind('<Return>', lambda event: on_ok_audio_click())
    dialog.mainloop()