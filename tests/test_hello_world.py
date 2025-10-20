#!/usr/bin/env python3
"""
Comprehensive unit tests for hello_world.py

This test suite covers:
- Main functionality (output verification)
- Function behavior and side effects
- Edge cases and boundary conditions
- Module execution scenarios
"""

import unittest
import sys
from io import StringIO
from unittest.mock import patch, call
import importlib.util


class TestHelloWorldMain(unittest.TestCase):
    """Test cases for the main() function in hello_world module."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import the module dynamically to test it
        spec = importlib.util.spec_from_file_location(
            "hello_world",
            "/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py"
        )
        self.hello_world = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.hello_world)

    def test_main_prints_hello_world(self):
        """Test that main() prints 'Hello, World!' to stdout."""
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            self.hello_world.main()

        # Verify the output
        self.assertEqual(captured_output.getvalue(), "Hello, World!\n")

    def test_main_prints_exactly_once(self):
        """Test that main() prints exactly one line of output."""
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            self.hello_world.main()

        # Count the number of lines printed
        lines = captured_output.getvalue().split('\n')
        # Filter out empty strings from split
        non_empty_lines = [line for line in lines if line]
        self.assertEqual(len(non_empty_lines), 1)

    def test_main_output_format(self):
        """Test that the output has correct capitalization and punctuation."""
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            self.hello_world.main()

        output = captured_output.getvalue().strip()

        # Verify capitalization
        self.assertTrue(output.startswith('Hello'))
        # Verify comma placement
        self.assertIn(', ', output)
        # Verify exclamation mark
        self.assertTrue(output.endswith('!'))

    def test_main_no_return_value(self):
        """Test that main() returns None (no explicit return)."""
        result = self.hello_world.main()
        self.assertIsNone(result)

    @patch('builtins.print')
    def test_main_uses_print_function(self, mock_print):
        """Test that main() uses the print() function."""
        self.hello_world.main()

        # Verify print was called
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_main_print_arguments(self, mock_print):
        """Test the exact arguments passed to print()."""
        self.hello_world.main()

        # Verify print was called with correct argument
        mock_print.assert_called_once_with("Hello, World!")

    def test_main_callable(self):
        """Test that main is a callable function."""
        self.assertTrue(callable(self.hello_world.main))

    def test_main_has_docstring(self):
        """Test that main() has a docstring."""
        self.assertIsNotNone(self.hello_world.main.__doc__)
        self.assertTrue(len(self.hello_world.main.__doc__) > 0)


class TestHelloWorldModule(unittest.TestCase):
    """Test cases for module-level behavior."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        spec = importlib.util.spec_from_file_location(
            "hello_world",
            "/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py"
        )
        self.hello_world = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.hello_world)

    def test_module_has_main_function(self):
        """Test that the module defines a main() function."""
        self.assertTrue(hasattr(self.hello_world, 'main'))

    def test_module_docstring_exists(self):
        """Test that the module has a docstring."""
        self.assertIsNotNone(self.hello_world.__doc__)
        self.assertTrue(len(self.hello_world.__doc__) > 0)

    def test_module_docstring_content(self):
        """Test that module docstring describes the program."""
        docstring = self.hello_world.__doc__.lower()
        # Check for relevant keywords
        self.assertTrue(
            'hello' in docstring or 'world' in docstring or 'simple' in docstring,
            "Module docstring should describe the program"
        )


class TestHelloWorldIntegration(unittest.TestCase):
    """Integration tests for the hello_world module."""

    def test_module_execution_as_script(self):
        """Test that module can be executed as a script."""
        # This tests the if __name__ == "__main__": block
        captured_output = StringIO()

        with patch('sys.stdout', captured_output):
            with patch.object(sys, 'argv', ['/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py']):
                # Simulate running as main module
                spec = importlib.util.spec_from_file_location(
                    "__main__",
                    "/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py"
                )
                module = importlib.util.module_from_spec(spec)
                module.__name__ = "__main__"
                spec.loader.exec_module(module)

        # Verify output when run as script
        self.assertEqual(captured_output.getvalue(), "Hello, World!\n")

    def test_multiple_calls_produce_identical_output(self):
        """Test that calling main() multiple times produces consistent output."""
        outputs = []

        for _ in range(5):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                spec = importlib.util.spec_from_file_location(
                    "hello_world",
                    "/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py"
                )
                hello_world = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(hello_world)
                hello_world.main()
            outputs.append(captured_output.getvalue())

        # All outputs should be identical
        self.assertEqual(len(set(outputs)), 1)
        self.assertEqual(outputs[0], "Hello, World!\n")


class TestHelloWorldEdgeCases(unittest.TestCase):
    """Edge case and boundary condition tests."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        spec = importlib.util.spec_from_file_location(
            "hello_world",
            "/Users/hudanqi/claude-demo/claude-git-demo/hello_world.py"
        )
        self.hello_world = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.hello_world)

    def test_main_with_different_stdout(self):
        """Test that main() works with different stdout redirections."""
        # Test with StringIO
        string_output = StringIO()
        with patch('sys.stdout', string_output):
            self.hello_world.main()
        self.assertEqual(string_output.getvalue(), "Hello, World!\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_encoding(self, mock_stdout):
        """Test that output is properly encoded as a string."""
        self.hello_world.main()
        output = mock_stdout.getvalue()

        # Verify output is a string
        self.assertIsInstance(output, str)
        # Verify it can be encoded to UTF-8
        self.assertIsInstance(output.encode('utf-8'), bytes)

    def test_main_no_exceptions(self):
        """Test that main() doesn't raise any exceptions."""
        try:
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                self.hello_world.main()
        except Exception as e:
            self.fail(f"main() raised an unexpected exception: {e}")

    def test_main_thread_safety(self):
        """Test that main() can be called from multiple contexts safely."""
        import threading

        outputs = []
        lock = threading.Lock()

        def run_main():
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                self.hello_world.main()
            with lock:
                outputs.append(captured_output.getvalue())

        threads = [threading.Thread(target=run_main) for _ in range(10)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All outputs should be identical
        self.assertEqual(len(outputs), 10)
        for output in outputs:
            self.assertEqual(output, "Hello, World!\n")


if __name__ == '__main__':
    unittest.main()
