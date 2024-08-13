import analysis

import os
import time
import threading
import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfilename
from PIL import Image, ImageTk

root = tk.Tk()
root.title('VI Analysis')
root.resizable(width=False,height=False)

input_folder = ''
output = ''

save_btn: tk.Button
empty_img: ImageTk
confirm_img: ImageTk

def get_folder(dir_entry: tk.Entry, output_entry: tk.Entry):
    global input_folder
    global output
    input_folder = askdirectory()
    dir_entry.delete(0, tk.END)
    dir_entry.insert(0, input_folder)
    date_str = analysis.get_date(input_folder)
    output = input_folder + '/' +  'vi_analysis_' + date_str + '.csv'
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output)
    reset_save_btn()

def get_save_file(file_name:str, file_entry: tk.Entry):
    global output
    file = asksaveasfilename(initialdir=input_folder, initialfile=file_name ,defaultextension='.csv', filetypes=[("Comma Separated Value files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file)
    output = file

def display_process_finished():
    global save_btn
    save_btn.config(
        image=confirm_img
    )
    t = threading.Thread(target=wait_and_reset_save_btn)
    t.start()

def reset_save_btn():
    global save_btn
    save_btn.config(
        image=empty_img
    )

def wait_and_reset_save_btn():
    time.sleep(5)
    reset_save_btn()

def run_ui() -> None:
    global root

    folder_select = tk.Frame(root)
    folder_select.grid(column=0, row=0)
    folder_select.grid_columnconfigure(1, weight=1)

    folder_lbl = tk.Label(folder_select, text='Data Folder')
    folder_lbl.grid(column=0, row=0)
    folder_entry = tk.Entry(folder_select, width=100)
    folder_entry.grid(column=1, row=0, sticky='we')
    browse_btn = tk.Button(folder_select, text='Browse...', command=lambda: get_folder(folder_entry, output_entry))
    browse_btn.grid(column=2, row=0)


    output_frame = tk.Frame(root)
    output_frame.grid(column=0, row=1)

    mouse_name = os.path.basename(input_folder)
    output_lbl = tk.Label(output_frame, text='Save to')
    output_lbl.grid(column=0, row=0)
    output_entry = tk.Entry(output_frame, width=100)
    output_entry.grid(column=1, row=0)
    output_browse_btn = tk.Button(output_frame, text='Browse...', command=lambda: get_save_file(mouse_name, output_entry))
    output_browse_btn.grid(column=2, row=0)

    mouse_thumbs_up_img = Image.open('img/mouse-thumbs-up.png')
    mouse_thumbs_up_img = mouse_thumbs_up_img.resize((50,50))
    mouse_thumbs_up_img = ImageTk.PhotoImage(mouse_thumbs_up_img)

    _empty_img = Image.open('img/empty.png')
    _empty_img = _empty_img.resize((50,50))
    _empty_img = ImageTk.PhotoImage(_empty_img)

    global empty_img
    empty_img = _empty_img
    global confirm_img
    confirm_img = mouse_thumbs_up_img

    _save_btn = tk.Button (
        root, 
        text='Analyse and Save', 
        command=lambda:analysis.run(folder_entry.get(), output_entry.get()),
        highlightthickness=2,
        image=empty_img,
        compound=tk.RIGHT
    )
    _save_btn.grid(column=0, row=2)
    global save_btn
    save_btn = _save_btn

    root.mainloop()