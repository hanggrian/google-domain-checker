from tkinter import Label


class LabelImpl:
    def __init__(self, label: Label):
        self.label = label

    def get_size(self) -> int:
        return self.label.winfo_width() * self.label.winfo_height()
