import tkinter as tk
from tkinter.filedialog import askopenfile

m = tk.Tk()
m.title('This is the title')



label = tk.Label(m, text='label text :0')
label.pack()

button = tk.Button(m, text='Button Text', width=100)
button.pack()

filename = askopenfile()

m.mainloop()