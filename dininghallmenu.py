import json
from datetime import datetime
import requests

LEONARD_HALL = 14627
BAN_RIGH_HALL = 14628
JEAN_ROYCE_HALL = 14629


class HallClosedError(Exception):
    """
    Raised when a menu is requested for a time the dining hall is closed.
    """
    pass


class MenuApiError(Exception):
    """
    Raised when invalid arguments cause an issue retrieving the menu data.
    """
    pass


async def get_menu_json(building_id: int, meal: str, date: str):
    """
    Retrieves unfiltered menu data in json format for a specific dining hall, meal, and day.

    :param building_id: The numeric ID representing the building
    :param meal: The meal to request a menu for ("Breakfast", "Lunch", or "Dinner")
    :param date: The date to request the menu for in "MM-DD-YYYY" format.
    :return: The received json data as a python object
    """
    data = requests.get("https://dining.queensu.ca/wp-content/themes/housing/campusDishAPI.php",
                        params={"locationId": building_id, "mealPeriod": meal, "selDate": date})
    return json.loads(data.content)


async def get_todays_menu(building_id: int, meal: str) -> dict:
    """
    Get the menu for the current date and extract just the station and item names.

    :param building_id: The numeric ID representing the building
    :param meal: The meal to request a menu for ("Breakfast", "Lunch", or "Dinner")
    :return: A dictionary of each station with a list of the items served there
    :raises HallClosedError: The dining hall is closed for this meal
    :raises MenuApiError: Request arguments may be invalid
    """
    # Get today's menu from the api
    date_string = datetime.now().strftime("%m-%d-%Y")
    json_data = await get_menu_json(building_id, meal, date_string)

    # Check that the menu was properly received
    if "MealPeriods" not in json_data:
        # The parameters might have been invalid
        raise MenuApiError
    elif len(json_data["MealPeriods"]) == 0:
        # Building is closed at this time
        raise HallClosedError

    # Organize the complex json data into a clean set of stations and item names
    menu = {}
    for station in json_data["MealPeriods"][0]["Stations"]:
        menu_items = []
        # Make a list of everything served at the station
        # Items are organized into sub-categories
        for category in station["SubCategories"]:
            # We only need the names, not any of the nutritional data
            menu_items += [item["ProductName"] for item in category["Items"]]

        # Add a list of all of this station's food to the menu
        menu[station["Name"]] = menu_items

    return menu


def hall_id_from_name(name: str) -> int:
    """ Translate a dining hall's name to the building ID used to retrieve the menu """
    if name.lower() in ["leonard", "leonard hall", "lenny", "shu's house"]:
        return LEONARD_HALL
    elif name.lower() in ["ban righ", "ban righ hall", "ban"]:
        return BAN_RIGH_HALL
    elif name.lower() in ["jean royce", "jean royce hall", "jean", "west"]:
        return JEAN_ROYCE_HALL
    else:
        return -1


def hall_name_from_id(hall_id: int) -> str:
    """ Get the human-readable name for a dinning hall"""
    if hall_id == LEONARD_HALL:
        return "Leonard Hall"
    elif hall_id == BAN_RIGH_HALL:
        return "Ban Righ Hall"
    elif hall_id == JEAN_ROYCE_HALL:
        return "Jean Royce Hall"
    else:
        return ""
