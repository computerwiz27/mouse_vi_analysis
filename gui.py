import analysis

import tkinter as tk
from tkinter.filedialog import askopenfilename

root = tk.Tk()
root.title('VI Analysis')

file = ''

def get_file(file_entry: tk.Entry):
    global file
    file = askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file)
    analysis.file = file
    analysis.init()

def print_to_field(field, handle):
    field.delete(1.0, tk.END)
    result = str(handle())
    field.insert(tk.END, result)

def analyse(wrong_pokes, impulsive_pokes, retrieval_t):
    print_to_field(wrong_pokes, analysis.get_wrong_pokes)
    print_to_field(impulsive_pokes, analysis.get_impulsive_pokes)
    print_to_field(retrieval_t, analysis.get_avg_retrieval_t)



def run_ui() -> None:
    global root

    file_select = tk.Frame(root)
    file_select.grid(column=0, row=0)

    file_lbl = tk.Label(file_select, text='File')
    file_lbl.grid(column=0, row=0)
    file_entry = tk.Entry(file_select)
    file_entry.grid(column=1, row=0)
    browse_btn = tk.Button(file_select, text='Browse...', command=lambda: get_file(file_entry))
    browse_btn.grid(column=2, row=0)

    analysis_frame = tk.Frame(root)
    analysis_frame.grid(column=0, row=1)

    wrong_pokes_lbl = tk.Label(analysis_frame, text='Wrong Pokes')
    wrong_pokes_lbl.grid(column=0, row=1)
    wrong_pokes_txt = tk.Text(analysis_frame, height=1)
    wrong_pokes_txt.grid(column=1, row=1)
    impulsive_pokes_lbl = tk.Label(analysis_frame, text='Impulsive Pokes')
    impulsive_pokes_lbl.grid(column=0, row=2)
    impulsive_pokes_txt = tk.Text(analysis_frame, height=1)
    impulsive_pokes_txt.grid(column=1, row=2)
    retrieval_t_lbl = tk.Label(analysis_frame, text='Average Retrieval Time (s)')
    retrieval_t_lbl.grid(column=0, row=3)
    retrieval_t_txt = tk.Text(analysis_frame, height=1)
    retrieval_t_txt.grid(column=1, row=3)
    analyse_btn = tk.Button(analysis_frame, text='Analyse', command=lambda: analyse(wrong_pokes_txt, impulsive_pokes_txt, retrieval_t_txt))
    analyse_btn.grid(column=0, row=0)





    root.mainloop()