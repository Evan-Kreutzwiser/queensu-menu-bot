import json
from datetime import datetime
import requests

LEONARD_HALL = 14627
BAN_RIGH_HALL = 14628
JEAN_ROYCE_HALL = 14629


class HallClosedError(Exception):
    pass


class MenuApiError(Exception):
    pass


async def get_menu_json(building_id, meal, date):
    """
    Retrieves unfiltered menu data in json format for
    a specific dining hall, meal, and day.

    Parameters
        building_id : int
            The numeric ID representing the building.
            Valid IDs are provided as class constants.

        meal : str
            The meal to request the menu for.
            Valid values are "Breakfast", "Lunch", and "Dinner".

        date : str
            The date to request the menu for in "MM-DD-YYYY" format.
    """
    data = requests.get("https://dining.queensu.ca/wp-content/themes/housing/campusDishAPI.php",
                        params={"locationId": building_id, "mealPeriod": meal, "selDate": date})
    return json.loads(data.content)


async def get_todays_menu(building_id, meal):
    """
    Get the menu for the current date and extract
    only the stations and item names.

    Parameters
      building_id : int
        The numeric ID representing the building.
        Valid IDs are provided as class constants.

      meal : str
        The meal to request the menu for.
        Valid values are "Breakfast", "Lunch", and "Dinner".
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
