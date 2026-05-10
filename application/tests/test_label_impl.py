from unittest import main, TestCase
from unittest.mock import Mock

from src.label_impl import LabelImpl


class TestLabelImpl(TestCase):
    def test(self):
        label = Mock()
        label.winfo_width.return_value = 2
        label.winfo_height.return_value = 4
        impl = LabelImpl(label)
        self.assertEqual(impl.get_size(), 8)
        self.assertTrue(label.winfo_width.called)
        self.assertTrue(label.winfo_height.called)


if __name__ == '__main__':
    main()
