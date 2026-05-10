from library.label_impl import LabelImpl


class LabelExtImpl(LabelImpl):
    def get_position(self) -> str:
        return f'({self.label.winfo_pointerx()},{self.label.winfo_pointery()})'
