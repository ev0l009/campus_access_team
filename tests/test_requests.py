"""Unit tests for the requests handling module."""

import unittest
from unittest.mock import patch
from io import StringIO
 
from services.requests import (
    generate_request_ids,
    create_request,
    get_request,
    view_request,
    list_requests,
)


class TestRequestsModule(unittest.TestCase):
    """Test suite targeting unique ID generation and request management CRUD actions."""

    def test_generate_request_ids_empty(self):
        """Verifies generation defaults to A001 when database is empty."""
        requests = {}
        req_id = generate_request_ids(requests)
        self.assertEqual(req_id, "A001")

    def test_generate_request_ids_sequential(self):
        """Verifies generation increments sequentially based on existing entries."""
        requests = {"A001": {}, "A002": {}}
        req_id = generate_request_ids(requests)
        self.assertEqual(req_id, "A003")

    def test_generate_request_ids_limit_reached(self):
        """Verifies ValueError raises if system reaches total capacity (999)."""
        requests = {f"A{i:03d}": {} for i in range(1, 1000)}
        with self.assertRaises(ValueError) as ctx:
            generate_request_ids(requests)
        self.assertIn("Requests creation limit reached", str(ctx.exception))

    @patch("services.requests.get_card_type")
    @patch("builtins.input", side_effect=["FELLOW123"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_request_success(self, mock_stdout, mock_input, mock_get_card):
        """Verifies a fully valid request correctly saves into storage."""
        mock_get_card.return_value = "student"
        requests = {}
        
        result = create_request(requests)
        
        self.assertIn("A001", requests)
        self.assertEqual(requests["A001"]["fellow_id"], "FELLOW123")
        self.assertEqual(requests["A001"]["card_type"], "student")
        self.assertEqual(requests["A001"]["status"], "requested")
        self.assertEqual(requests["A001"]["approved_by"], "None")
        self.assertIsNotNone(result)

    @patch("builtins.input", side_effect=["   "])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_request_empty_fellow_id(self, mock_stdout, mock_input):
        """Verifies request fails gracefully when whitespace fellow ID is entered."""
        requests = {}
        result = create_request(requests)
        
        self.assertEqual(requests, {})
        self.assertIsNone(result)
        self.assertIn("Err: Fellow ID cannot be empty", mock_stdout.getvalue())

    @patch("services.requests.get_card_type", side_effect=ValueError("Invalid card type"))
    @patch("builtins.input", side_effect=["FELLOW123"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_request_card_type_error(self, mock_stdout, mock_input, mock_get_card):
        """Verifies request drops if user submits an incorrect card option."""
        requests = {}
        result = create_request(requests)
        
        self.assertEqual(requests, {})
        self.assertIsNone(result)
        self.assertIn("Err: Invalid card type", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["A001"])
    def test_get_request_valid(self, mock_input):
        """Verifies successful payload lookup using a known ID index."""
        requests = {"A001": {"id": "A001", "fellow_id": "F1"}}
        result = get_request(requests)
        self.assertEqual(result, requests["A001"])

    @patch("builtins.input", side_effect=["A999"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_get_request_invalid(self, mock_stdout, mock_input):
        """Verifies get_request returns None if searched ID does not exist."""
        requests = {"A001": {"id": "A001", "fellow_id": "F1"}}
        result = get_request(requests)
        self.assertIsNone(result)
        self.assertIn("Invalid request ID", mock_stdout.getvalue())

    @patch("services.requests.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_view_request_success(self, mock_stdout, mock_validate):
        """Verifies view interface cleanly displays ticket details in terminal."""
        req_data = {
            "id": "A001",
            "fellow_id": "FELLOW123",
            "card_type": "visitor",
            "status": "requested",
            "approved_by": "None"
        }
        mock_validate.return_value = req_data
        
        view_request({})
        output = mock_stdout.getvalue()
        
        self.assertIn("Ticket Details", output)
        self.assertIn("A001", output)
        self.assertIn("FELLOW123", output)

    @patch("services.requests.get_request", return_value=None)
    def test_view_request_not_found(self, mock_validate):
        """Verifies application safely exits view operations if request target is empty."""
        try:
            view_request({})
        except Exception as e:
            self.fail(f"view_request raised an unexpected exception: {e}")

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_requests_empty(self, mock_stdout):
        """Verifies list summary informs user clearly when no request files exist."""
        list_requests({})
        self.assertIn("There are no requests right now.", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_requests_non_empty(self, mock_stdout):
        """Verifies entire dataset structure prints out accurately into a tabular view."""
        requests = {
            "A001": {
                "id": "A001",
                "card_type": "staff",
                "status": "approved",
                "approved_by": "Admin"
            }
        }
        list_requests(requests)
        output = mock_stdout.getvalue()
        
        self.assertIn("ALL CARD REQUESTS", output)
        self.assertIn("A001", output)
        self.assertIn("Staff", output)
        self.assertIn("Approved", output)
        self.assertIn("Admin", output)