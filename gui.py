import analysis

import os
import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfilename

root = tk.Tk()
root.title('VI Analysis')
root.resizable()

input_folder = ''
output = ''

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

def get_save_file(file_name:str, file_entry: tk.Entry):
    global output
    file = asksaveasfilename(initialdir=input_folder, initialfile=file_name ,defaultextension='.csv', filetypes=[("Comma Separated Value files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file)
    output = file

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

    save_btn = tk.Button(root, text='Analyse and Save', command=lambda:analysis.run(folder_entry.get(), output_entry.get()))
    save_btn.grid(column=0, row=2)

    root.mainloop()