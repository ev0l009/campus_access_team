"""Unit tests for the workflow lifecycle management module."""

import unittest
from unittest.mock import patch
from io import StringIO

from services.workflow import approve_request, issue_card, return_card


class TestWorkflowModule(unittest.TestCase):
    """Test suite targeting sequential state changes (Requested -> Approved -> Issued -> Returned)."""

    @patch("services.workflow.get_request", return_value=None)
    def test_approve_request_not_found(self, mock_get_request):
        """Verifies approval aborts gracefully if the requested ticket ID does not exist."""
        result = approve_request({})
        self.assertIsNone(result)

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_approve_request_invalid_status(self, mock_stdout, mock_get_request):
        """Verifies tickets already processed cannot be approved a second time."""
        req = {"id": "A001", "status": "approved", "approved_by": "Staff1"}
        mock_get_request.return_value = req
        
        approve_request({})
        self.assertIn("Only requests with status 'requested' can be approved.", mock_stdout.getvalue())

    @patch("services.workflow.get_request")
    @patch("builtins.input", side_effect=["   "])
    @patch("sys.stdout", new_callable=StringIO)
    def test_approve_request_empty_staff_id(self, mock_stdout, mock_input, mock_get_request):
        """Verifies approval routes back to dashboard if staff signature input is left blank."""
        req = {"id": "A001", "status": "requested", "approved_by": "None"}
        mock_get_request.return_value = req
        
        result = approve_request({})
        self.assertEqual(result, "dashboard")
        self.assertIn("Err: Fellow ID cannot be empty", mock_stdout.getvalue())

    @patch("services.workflow.get_request")
    @patch("builtins.input", side_effect=["STAFF001"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_approve_request_success(self, mock_stdout, mock_input, mock_get_request):
        """Verifies ticket updates status to 'approved' and binds the staff ID upon valid submission."""
        req = {"id": "A001", "status": "requested", "approved_by": "None"}
        mock_get_request.return_value = req
        
        approve_request({})
        
        self.assertEqual(req["status"], "approved")
        self.assertEqual(req["approved_by"], "STAFF001")
        self.assertIn("Card access request approved by STAFF001", mock_stdout.getvalue())

    @patch("services.workflow.get_request", return_value=None)
    def test_issue_card_not_found(self, mock_get_request):
        """Verifies card physical printing/issuance aborts if target ID does not exist."""
        result = issue_card({})
        self.assertIsNone(result)

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_issue_card_invalid_status(self, mock_stdout, mock_get_request):
        """Verifies unapproved tickets block card collection attempts."""
        req = {"id": "A001", "status": "requested", "approved_by": "None"}
        mock_get_request.return_value = req
        
        issue_card({})
        self.assertIn("Only approved requests can be issued.", mock_stdout.getvalue())

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_issue_card_invalid_approver(self, mock_stdout, mock_get_request):
        """Verifies cards cannot clear validation boundaries with missing structural metadata signatures."""
        req = {"id": "A001", "fellow_id": "F1", "status": "approved", "approved_by": "   "}
        mock_get_request.return_value = req
        
        issue_card({})
        self.assertIn("Cannot issue a card without a recorded approver.", mock_stdout.getvalue())

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_issue_card_success(self, mock_stdout, mock_get_request):
        """Verifies ticket sets status to 'issued' on safe processing authorization."""
        req = {"id": "A001", "fellow_id": "F1", "status": "approved", "approved_by": "STAFF001"}
        mock_get_request.return_value = req
        
        issue_card({})
        
        self.assertEqual(req["status"], "issued")
        self.assertIn("Card issued to fellow ID: F1", mock_stdout.getvalue())

    @patch("services.workflow.get_request", return_value=None)
    def test_return_card_not_found(self, mock_get_request):
        """Verifies return workflows cancel early if targeting missing profile records."""
        result = return_card({})
        self.assertIsNone(result)

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_return_card_invalid_status(self, mock_stdout, mock_get_request):
        """Verifies tickets cannot change to 'returned' unless their previous verified state was 'issued'."""
        req = {"id": "A001", "fellow_id": "F1", "status": "approved"}
        mock_get_request.return_value = req
        
        return_card({})
        self.assertIn("Only issued cards can be returned.", mock_stdout.getvalue())

    @patch("services.workflow.get_request")
    @patch("sys.stdout", new_callable=StringIO)
    def test_return_card_success(self, mock_stdout, mock_get_request):
        """Verifies final state change to 'returned' resolves the active profile lifecycle tracker safely."""
        req = {"id": "A001", "fellow_id": "F1", "status": "issued"}
        mock_get_request.return_value = req
        
        return_card({})
        
        self.assertEqual(req["status"], "returned")
        self.assertIn("Card returned by fellow ID: F1", mock_stdout.getvalue())