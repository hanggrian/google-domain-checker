from unittest import main, TestCase
from unittest.mock import Mock

from library_extension.label_ext_impl import LabelExtImpl


class TestLabelImpl(TestCase):
    def test(self):
        label = Mock()
        label.winfo_pointerx.return_value = 0
        label.winfo_pointery.return_value = 1
        impl = LabelExtImpl(label)
        self.assertEqual(impl.get_position(), '(0,1)')
        self.assertTrue(label.winfo_pointerx.called)
        self.assertTrue(label.winfo_pointery.called)


if __name__ == '__main__':
    main()
