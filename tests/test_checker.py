from contextlib import redirect_stdout
from io import StringIO
from tempfile import NamedTemporaryFile
from unittest import main, TestCase
from unittest.mock import patch

from src import main as cli
from src.checker import _is_google_domain_domain, is_google_domain


class TestChecker(TestCase):
    def test_is_google_domain(self):
        self.assertTrue(is_google_domain('definitely@gmail.com'))
        self.assertTrue(is_google_domain('support-id@google.co.id'))
        self.assertFalse(is_google_domain('support@protonmail.zendesk.com'))

    def test_is_google_domain_caches_domain_lookups(self):
        class FakeRdata:
            def __init__(self, exchange):
                self.exchange = exchange

        _is_google_domain_domain.cache_clear()
        with patch(
            'src.checker.resolve',
            return_value=[FakeRdata('aspmx.l.google.com.')],
        ) as resolve_mock:
            self.assertTrue(is_google_domain('admin@google.co.id'))
            self.assertTrue(is_google_domain('support@google.co.id'))
        self.assertEqual(resolve_mock.call_count, 1)

    def test_convert_adds_google_column(self):
        with NamedTemporaryFile(
            'w+',
            newline='',
            encoding='UTF-8',
            suffix='.csv',
            delete=False,
        ) as input_file:
            input_file.write('email,name\n')
            input_file.write('admin@gmail.com,Alice\n')
            input_file.write('support@gmail.com,Bob\n')
            input_file.write('user@example.com,Carol\n')
            input_file.flush()
            output = StringIO()
            with patch('src.main.argv', ['convert', input_file.name]), \
                patch(
                    'src.main.is_google_domain',
                    side_effect=lambda domain: domain == 'gmail.com',
                ), \
                redirect_stdout(output):
                cli.convert()
            input_file.seek(0)
            contents = input_file.read().splitlines()
            progress = output.getvalue().splitlines()
        self.assertEqual(contents[0], 'EMAIL,NAME,GOOGLE')
        self.assertEqual(contents[1], 'admin@gmail.com,Alice,Yes')
        self.assertEqual(contents[2], 'support@gmail.com,Bob,Yes')
        self.assertEqual(contents[3], 'user@example.com,Carol,No')
        self.assertTrue(progress[0].startswith('Loading '))
        self.assertTrue(progress[0].endswith('.csv.'))
        self.assertEqual(progress[1], 'Processing 3 row(s) across 2 worker(s).')
        self.assertTrue(progress[2].startswith('Resolved 1/'))
        self.assertTrue(progress[2].endswith('unique domain(s).'))
        self.assertTrue(progress[3].startswith('Resolved 2/'))
        self.assertTrue(progress[3].endswith('unique domain(s).'))
        self.assertEqual(progress[4], 'Processed 1/3 row(s).')
        self.assertEqual(progress[5], 'Processed 2/3 row(s).')
        self.assertEqual(progress[6], 'Processed 3/3 row(s).')
        self.assertTrue(progress[7].endswith('Done.\x1b[0m'))

    def test_convert_uses_unique_domain_lookups(self):
        with NamedTemporaryFile(
            'w+',
            newline='',
            encoding='UTF-8',
            suffix='.csv',
            delete=False,
        ) as input_file:
            input_file.write('email,name\n')
            input_file.write('admin@gmail.com,Alice\n')
            input_file.write('support@gmail.com,Bob\n')
            input_file.write('user@example.com,Carol\n')
            input_file.flush()
            with patch('src.main.argv', ['convert', input_file.name]), \
                patch('src.main.cpu_count', return_value=8), \
                patch('src.main.is_google_domain', side_effect=[True, False]) as is_google_mock, \
                redirect_stdout(StringIO()):
                cli.convert()
        self.assertEqual(is_google_mock.call_count, 2)


if __name__ == '__main__':
    main()
