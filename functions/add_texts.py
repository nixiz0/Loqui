import tkinter as tk
from tkinter import filedialog
import os
import json
import string


def add_texts():
    master = tk.Toplevel()
    master.title("Loqui Add Data")
    master.configure(bg='#333333')
    font = ('Helvetica', 15)
    
    # Set the window size and limits
    master.geometry("350x410")
    master.minsize(330, 400)
    master.maxsize(370, 430)

    # Center the window
    window_width = master.winfo_reqwidth()
    window_height = master.winfo_reqheight()
    position_right = int(master.winfo_screenwidth()/2 - window_width/2)
    position_down = int(master.winfo_screenheight()/2 - window_height/2)
    master.geometry("+{}+{}".format(position_right, position_down))

    def save_to_file(trigger, response, file_path='json_texts/texts.json'):
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({}, file, ensure_ascii=False, indent=4)
        with open(file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[trigger] = response
            file.seek(0)
            file.truncate()
            json.dump(data, file, ensure_ascii=False, indent=4)

    def submit_fields():
        trigger = e1.get()
        response = e2.get()
        if trigger and response:
            save_to_file(trigger, response)
            e1.delete(0, tk.END)
            e2.delete(0, tk.END)

    def open_file_dialog():
        filename = filedialog.askopenfilename()
        if filename:
            base = os.path.basename(filename)
            name_without_ext = os.path.splitext(base)[0].lower()
            name_without_ext = name_without_ext.translate(str.maketrans('', '', string.punctuation))
            save_to_file(name_without_ext, filename, 'json_files/file_path.json')
            e3.config(state='normal')
            e3.delete(0, tk.END)
            e3.insert(0, name_without_ext)
            e3.config(state='disabled')

    def rename_key():
        old_key = e3.get()
        new_key = e4.get()
        if old_key and new_key:
            with open('json_files/file_path.json', 'r+', encoding='utf-8') as file:
                data = json.load(file)
                if old_key in data:
                    data[new_key] = data.pop(old_key)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, ensure_ascii=False, indent=4)
                else:
                    print(f"The key '{old_key}' does not exist in the JSON file.")
        e4.delete(0, tk.END)

    e1 = tk.Entry(master, font=font)
    tk.Label(master, text="Trigger Phrase", bg='#333333', fg='white', font=font).pack()
    e1.pack()

    e2 = tk.Entry(master, font=font)
    tk.Label(master, text="Response", bg='#333333', fg='white', font=font).pack()
    e2.pack()

    tk.Button(master, text='Submit', command=submit_fields, font=font).pack(pady=7)
    tk.Frame(master, height=3, bg="white").pack(fill=tk.X, padx=5, pady=5)
    tk.Button(master, text='Add Application', command=open_file_dialog, font=font).pack(pady=5)

    e3 = tk.Entry(master, font=font)
    tk.Label(master, text="Application Key", bg='#333333', fg='white', font=font).pack()
    e3.pack()

    e4 = tk.Entry(master, font=font)
    tk.Label(master, text="New Key Name", bg='#333333', fg='white', font=font).pack()
    e4.pack()

    tk.Button(master, text='Rename', command=rename_key, font=font).pack(pady=5)

    master.mainloop()