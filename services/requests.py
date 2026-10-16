from string import digits

from services.ui import get_card_type

VALID_CARD_TYPES = {"visitor", "student", "staff"}
REQUEST_ID_PREFIX = "A"
REQUEST_ID_LENGTH = 4

def generate_request_ids(requests):

    number = 1

    while number <= 999:
        request_id = f"{REQUEST_ID_PREFIX}{number:03d}"

        if request_id not in requests:
            return request_id

        number += 1

    raise ValueError("\nRequests creation limit reached.\n")

def create_request(requests):

    fellow_id = input("\nEnter your fellow ID: ")

    if not fellow_id.strip():
        print("\nErr: Fellow ID cannot be empty\n")
        return 
        
    try:
        card_type = get_card_type()
    except ValueError as err:
        print(f"Err: {err}")
        return 

    request_id = generate_request_ids(requests)

    requests[request_id] = {
        "id": request_id,
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": None
    }

    print(
        "\n┌────────────────────────────────────────┐\n"
        "│      Request created successfully      │\n"
        "├────────────────────────────────────────┤\n"
        f"│ Request ID:     {request_id:<22} │\n"
        f"│ Fellow ID:      {fellow_id:<22} │\n"
        f"│ Card Type:      {card_type.capitalize():<22} │\n"
        "│ Status:         Requested              │\n"
        "│ Approved by:    None                   │\n"
        "└────────────────────────────────────────┘\n"
    )
    return requests

def validate_request_id(requests):
    request_id = input("\nEnter request ID: ")
    
    if request_id not in requests:
        print(f"\nInvalid request ID: {request_id}\n")
        return

    return requests[request_id]


def view_request(requests):

    request = validate_request_id(requests)

    if request is None:
        return

    print(
        "\n┌────────────────────────────────────────┐\n"
        "│             Ticket Details             │\n"
        "├────────────────────────────────────────┤\n"
        f"│ Request ID:     {request["id"]:<22} │\n"
        f"│ Fellow ID:      {request["fellow_id"]:<22} │\n"
        f"│ Card Type:      {request["card_type"].capitalize():<22} │\n"
        f"│ Status:         {request["status"].capitalize():<22} │\n"
        f"│ Approved by:    {request["approved_by"]:<22} │\n"
        f"└────────────────────────────────────────┘\n"
    )

def list_requests(requests):
    if not requests:
        print("\nThere are no requests right now.\n")
        return

    requests_list_str = (
        "\n{'=' * 50}\n"
        "             ALL CARD REQUESTS\n"
        "{'=' * 50}\n"
        f"{'ID':<8}{'CARD TYPE':<15}{'STATUS':<15}{'APPROVED BY':<12}\n"
        f"{'-' * 50}\n"
    )

    for req in requests.values():
        requests_list_str += (
            f"{req['id']:<8}"
            f"{req['card_type'].capitalize():<15}"
            f"{req['status'].capitalize():<15}"
            f"{str(req['approved_by']):<15}\n"
        )

    print(requests_list_str)