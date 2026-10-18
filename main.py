"""Entry point of application."""

from services.ui import get_dashboard_menu_opt
from services.storage import load_campus_access, save_session
from services.requests import create_request, view_request, list_requests
from services.workflow import approve_request, issue_card, return_card


def campus_access_runner():
    """Controls the runtime application lifecycle and primary execution loop.

    Coordinates loading saved states, routing terminal menu options, and auto-saving sessions.
    """
    current_state = "dashboard"
    data = load_campus_access()

    # Core state machine loop
    while current_state != "exit":

        if current_state == "dashboard":
            current_state = get_dashboard_menu_opt()

        elif current_state == "create_request":
            result = create_request(data)
            if result:
                data = result
            current_state = "dashboard"

        elif current_state == "view_request":
            view_request(data)
            current_state = "dashboard"

        elif current_state == "approve_request":
            approve_request(data)
            current_state = "dashboard"

        elif current_state == "issue_card":
            issue_card(data)
            current_state = "dashboard"

        elif current_state == "return_card":
            return_card(data)
            current_state = "dashboard"

        elif current_state == "list_requests":
            list_requests(data)
            current_state = "dashboard"

    # Persist data state before close
    save_session(data)
    print("Exiting application.")


if __name__ == "__main__":
    campus_access_runner()