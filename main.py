"""Entry point of application."""

from services.ui import get_dashboard_menu_opt

from services.storage import load_campus_access, save_session   # We import functions that we'll use

from services.requests import create_request, view_request, list_requests
from services.workflow import approve_request, issue_card, return_card

def campus_access_runner():
    """Controls app flow."""

    current_state = "dashboard" # defines where you are in the program

    data = load_campus_access() # loads data from database and stores it in data variable

    while current_state != "exit":

        if current_state == "dashboard":
            current_state = get_dashboard_menu_opt()

        elif current_state == "create_request":
            result = create_request(data) # Run create requests and store the returned value in result.

            if result: # checks whether result has a value aside None. If the value is None, do nothing otherwise update or data. 
                data = result

            current_state = "dashboard" # reset back to the dashboard

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

    save_session(data)

    print("Exiting application.")

campus_access_runner()