"""Handles user interface menus and input selections for the system."""


def get_dashboard_menu_opt():
    """Displays the main control panel and returns the selected action.

    Returns:
        str: The string action key corresponding to the choice, or 'dashboard' if invalid.
    """
    options = {
        "1": "create_request",
        "2": "view_request",
        "3": "approve_request",
        "4": "issue_card",
        "5": "return_card",
        "6": "list_requests",
        "7": "exit"
    }

    choice = input(
        "===== CAMPUS ACCESS =====\n"
        "1. Create request\n"
        "2. View request\n"
        "3. Approve request\n"
        "4. Issue card\n"
        "5. Return card\n"
        "6. List requests\n"
        "7. Exit\n"
        "_________________________\n"
        "Select an option(1-7): "
    )

    if choice not in options:
        print("\nInvalid selection. Try again\n")
        return "dashboard"

    return options[choice]


def get_card_type():
    """Prompts the user to select an access group classification.

    Raises:
        ValueError: If the user selection is outside the valid 1-3 range.

    Returns:
        str: The chosen card type string ('visitor', 'student', or 'staff').
    """
    card_types = {
        "1": "visitor",
        "2": "student",
        "3": "staff"
    }

    choice = input(
        "\nSelect a card type:\n"
        "1. Visitor\n"
        "2. Student\n"
        "3. Staff\n"
        "_________________________\n"
        "Select an option(1-3): "
    )

    if choice not in card_types:
        raise ValueError("\nInvalid card type selection.\n")

    return card_types[choice]
