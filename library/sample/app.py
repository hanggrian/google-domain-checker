from tkinter import Tk, Label

from library_extension.label_ext_impl import LabelExtImpl

tk: Tk = Tk()
tk.geometry('400x300')

label: Label = Label(tk, text='Hello, World!')
label.place(relx=0.5, rely=0.5, anchor='center')

impl: LabelExtImpl = LabelExtImpl(label)
label.config(text=f'{impl.get_size()} pixels')
label.config(text=f'{label['text']} at {impl.get_position()}')

tk.mainloop()
