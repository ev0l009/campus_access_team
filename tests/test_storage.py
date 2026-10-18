"""Unit tests for the storage persistence layer module."""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from pathlib import Path
from io import StringIO

from services.storage import load_campus_access, save_session


class TestStorageModule(unittest.TestCase):
    """Test suite verifying database creation, directory structural safety, and JSON state persistence."""

    @patch("services.storage.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open, read_data='{"A001": {"id": "A001"}}')
    @patch("sys.stdout", new_callable=StringIO if 'StringIO' in globals() else None)
    def test_load_campus_access_success(self, mock_stdout, mock_file, mock_mkdir):
        """Verifies clean JSON profiles load correctly when the storage file exists."""
        data = load_campus_access()
        
        mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
        mock_file.assert_called_once()
        self.assertEqual(data, {"A001": {"id": "A001"}})

    @patch("services.storage.Path.mkdir")
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("sys.stdout", new_callable=StringIO)
    def test_load_campus_access_file_not_found(self, mock_stdout, mock_file, mock_mkdir):
        """Verifies missing database files fall back to an empty tracking dictionary."""
        data = load_campus_access()
        self.assertEqual(data, {})
        self.assertIn("Couldn't load requests", mock_stdout.getvalue())

    @patch("services.storage.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("sys.stdout", new_callable=None)
    def test_load_campus_access_json_decode_error(self, mock_stdout, mock_file, mock_mkdir):
        """Verifies corrupted file structures are caught safely to return an empty layout."""
        data = load_campus_access()
        self.assertEqual(data, {})

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_session_success(self, mock_json_dump, mock_file):
        """Verifies application workspace states dump successfully to storage paths with clear indent formatting."""
        test_data = {"A001": {"status": "approved"}}
        save_session(test_data)
        
        mock_file.assert_called_once()
        mock_json_dump.assert_called_once_with(test_data, mock_file.return_value.__enter__(), indent=4)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_save_session_file_not_found(self, mock_file):
        """Verifies operational save execution catches system path access faults cleanly."""
        test_data = {"A001": {"status": "approved"}}
        try:
            save_session(test_data)
        except Exception as e:
            self.fail(f"save_session raised unexpected exception: {e}")