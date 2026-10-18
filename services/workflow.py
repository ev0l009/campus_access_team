"""Manages the state lifecycle (approval, issuance, return) of card access requests."""

from services.requests import get_request


def approve_request(requests):
    """Approves a pending card access request with a validated staff ID.

    Args:
        requests (dict): The global requests dataset.
    """
    request = get_request(requests)

    if request is None:
        return

    if request["status"] != "requested":
        print("\nOnly requests with status 'requested' can be approved.\n")
        return

    staff_id = input("\nEnter staff ID: ")

    if not staff_id.strip():
        print("\nErr: Fellow ID cannot be empty\n")
        return "dashboard"

    request["approved_by"] = staff_id
    request["status"] = "approved"

    print(f"\nCard access request approved by {staff_id}.\n")


def issue_card(requests):
    """Changes the status of an approved request to issued.

    Args:
        requests (dict): The global requests dataset.
    """
    request = get_request(requests)

    if request is None:
        return

    if request["status"] != "approved":
        print("\nOnly approved requests can be issued.\n")
        return

    if (
        not isinstance(request["approved_by"], str)
        or not request["approved_by"].strip()
    ):
        print("\nCannot issue a card without a recorded approver.\n")
        return

    request["status"] = "issued"
    print(f"\nCard issued to fellow ID: {request['fellow_id']}\n")


def return_card(requests):
    """Marks an issued card as successfully returned.

    Args:
        requests (dict): The global requests dataset.
    """
    request = get_request(requests)

    if request is None:
        return

    if request["status"] != "issued":
        print("\nOnly issued cards can be returned.\n")
        return

    request["status"] = "returned"
    print(f"\nCard returned by fellow ID: {request['fellow_id']}\n")
