import os
import traceback

import pytest
from pyfakefs import fake_filesystem_unittest

from github_forcepush_tracker.utils import setup_logging

class LoggerTests(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()  # Fake file system
        self.test_log_path = os.path.join(
            os.getcwd(), 'Test_log_dir' 'TEST_LOG_FILE.TEST')

        setup_logging(self.test_log_path)

    def tearDown(self):
        self.capsys = None

    def test_path_to_log_file(self):
        # make sure log file is created where we expect it
        pass

    @pytest.fixture(autouse=True)
    def expose_capsys(self, capsys):
        self.capsys = capsys

    def test_print_method_logs(self):
        # make sure logger and print statements log to file
        txt = '123 test line'
        print txt
        with open(self.test_log_path) as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 1)
        self.assertIn(txt, lines[0])
        self.assertIn('STDOUT', lines[0])
        out, err = self.capsys.readouterr()
        # make sure console matches log file
        self.assertEqual(lines[0], out)

        # printing everything to std out so err should be blank
        self.assertEqual(len(err), 0)

    def test_traceback_print_method_logs(self):
        # make sure logger and print statements log to file
        txt = 'test error line'
        try:
            raise Exception(txt)
        except:
            traceback.print_exc()

        with open(self.test_log_path) as f:
            lines = f.readlines()

        # 3 lines, traceback message, traceback line, exception line
        self.assertEqual(len(lines), 3)

        self.assertIn('Traceback (most recent call last)', lines[0])
        self.assertIn('STDERR', lines[0])

        self.assertIn('in test_traceback_print_method_logs', lines[1])
        self.assertIn('STDERR', lines[1])

        self.assertIn(txt, lines[2])
        self.assertIn('STDERR', lines[2])

        out, err = self.capsys.readouterr()
        out_lines = out.splitlines()
        # make sure console matches log file
        self.assertEqual(lines[0].strip(), out_lines[0].strip())
        self.assertEqual(lines[1].strip(), out_lines[1].strip())
        self.assertEqual(lines[2].strip(), out_lines[2].strip())
        # printing everything to std out so err should be blank
        self.assertEqual(len(err), 0)
