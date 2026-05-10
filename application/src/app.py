from tkinter import Tk, Label

from src.label_impl import LabelImpl

tk: Tk = Tk()
tk.geometry('400x300')

label: Label = Label(tk, text='Hello, World!')
label.place(relx=0.5, rely=0.5, anchor='center')

impl: LabelImpl = LabelImpl(label)
label.config(text=f'{impl.get_size()} pixels')

tk.mainloop()
