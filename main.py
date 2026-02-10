import sys # for exit()
import os # file handling
import time # time.sleep()



""" Initialization """
###

plant_counter = 0
fertilizer_counter = 0
log_counter = 0
plants_details = {}  # store plant details
fertilizer_details = {}  # store fertilizer details
valid_types = [
    "plant",
    "fertilizer",
    "logbook",
    "all",
    "exit",
    "p",
    "f",
    "l",
    "a",
    "e"
]  # valid choices
transactions_path = "transactions.dat"  # transactions file path
records_path = "records.dat"  # records file path
counters_path = "counters.dat" # counters_path

###

""" Main Menu Function """
def mainMenu(a_type):
    global plants_details
    global fertilizer_details
    # Step 1: Display initial menu and get user action type.
    if a_type == "start":
        entity_type = get_entity_type()  # get the list of options the user gave
    elif a_type in valid_types:
        entity_type = a_type

    # Step 2 : Validate and display relevant options
    available_choices = displayOptions(
        entity_type
    )  # display and retrieve the available choices

    # Step 3 : Ask User to select an Option
    choice = getValidChoice(available_choices)
    # Step 4 : execute the selected function
    executeFunctions(choice)

###

""" Utility Functions """
def get_entity_type():
    """
    This function retrieves valid choices from the user

    """

    while True:
        entity_choice = (
            input(
                "What would you like to see? (Plant/Fertilizer/Logbook/All/Exit)\nYou can choose one or more options separated by comma (,): "
            )
            .lower()
            .strip()
            .split(",")
        )
        if all(
            choice not in valid_types for choice in entity_choice
        ):  # checks if user enters non-valid either
            print(
                f"You have entered options not in the following options: {' || '.join(valid_types)} "  # prints into a single string separated by " || "
            )
            continue  # prompt again

        return entity_choice
def standardizeChoices(user_input):
    """
    This function standardize the choices from the user, meaning to say
    """
    # Define a mapping of shorthand to full forms
    synonyms = {
        "plant": "p",
        "fertilizer": "f",
        "logbook": "l",
        "all": "a",
        "exit": "e",
    }
    # Standardize the input choices
    standardized_choices = set()  # set, to avoid duplicates
    for choice in user_input:
        # Replace full form with short hand if it exists in the mapping
        standardized_choices.add(synonyms.get(choice, choice))

    # Step 3: Return the unique, standardized choices
    return list(standardized_choices)

def all_options():
    """
    This function is solely for mapping the options

    """

    allOptions = {
        "p": {
            0: "Exit",
            1: "Previous",
            2: "Add Plant",
            3: "Delete Plant",
            4: "View Plant",
            5: "Edit Plant",
            6: "Update Nourishment",
            7: "Nourish Plant",
        },
        "f": {
            0: "Exit",
            1: "Previous",
            8: "Purchase Fertilizer",
            9: "View Fertilizer",
            10: "View All Fertilizers",
            11: "View Affected Plants",
        },
        "l": {
            0: "Exit",
            1: "Previous",
            12: "View All Entries",
            13: "View Transactions per action",
            14: "Data Reset",
        },
        "a": {},
        "e": {0: "Exit"},
    }

    allOptions["a"].update(allOptions["p"])  # insert plant's options in "all" key
    allOptions["a"].update(allOptions["f"])  # insert fertilizer's options in "all" key
    allOptions["a"].update(allOptions["l"])  # insert logbook's options in "all" key

    return allOptions

def sortingKey(n):
    """
    Custom sorting key to prioritize specific characters:
    'a' > 'p' > 'l' > 'f' > other characters (sorted by their ASCII value)
    """
    priority = {"a": 0, "p": 1, "f": 2, "l": 3}  # highest priority

    # Check if the character is in the priority dictionary, if not assign it a value greater than 3
    return priority.get(n, 4)  # Return 4 for all other characters

def displayOptions(entity_types):
    options = all_options()  # retrieve the options
    selected_modes = standardizeChoices(
        entity_types
    )  # standardize the input of the user first to eliminate duplicates and replace shorthands
    available_choices = []  # store the possible choices here

    # loop over the selected entity types
    for entity in sorted(selected_modes, key=sortingKey):  # sort by priority
        try:
            # unpack the corresponding dictionary items
            for number, action in options[entity].items():
                if number not in available_choices:
                    print(f"[{number}] {action}")
                    available_choices.append(
                        number
                    )  # add the key to the available choices
        except KeyError:
            print(
                f"\nUnfortunately, we don't have the system to operate for that entity/es: {entity}"
            )

    return available_choices

def getValidChoice(options):
    while True:
        try:
            option_choice = int(input("Which one would you like to proceed with? "))
            if option_choice not in options:
                print("Please select among the allowed choices only.")
                continue  # prompt again

            return option_choice

        except ValueError:
            print("Invalid input. Please enter a number corresponding to the options.")

def getID(to_check, iterable, name_type):
    # if user enters the name, check if it exists in the records
    if any(to_check == details[name_type] for details in iterable.values()):
        for (
                the_id,
                the_details,
        ) in (
                iterable.items()
        ):  # if the name is found, the current id where that name is found is the id.
            if the_details[name_type] == to_check:
                return the_id
    # users enters id instead
    elif to_check in iterable:
        return to_check

    else:
        return None


## UTILITY FUNCTIONS
def programExit():
    """Function that gets called before the program exits"""
    global plant_counter,fertilizer_counter,log_counter
    save_counters = input("Do you want to save the counters?: (y/n) " ).lower().strip()
    if save_counters in ['y', 'yes']:
        # Save the ids before exiting
        saveCounters({
            "plant_counter": plant_counter,
            "fertilizer_counter": fertilizer_counter,
            "log_counter": log_counter
        })

    print("Thank you for using our program!")
    # encrypt both file before quitting
    encrypt(transactions_path)
    encrypt(records_path)
    sys.exit()

def previous():
    print("\nProceeding to previous action...\n")
    mainMenu("start")


def checkIfEmpty(details):
    return details is None or not details


# store functions for readability
def executeFunctions(option):

    listOfFunctions = {
        0: programExit,
        1: previous,
        2: addPlant,
        3: deletePlant,
        4: viewPlant,
        5: editPlant,
        6: updateNourishment,
        7: nourishPlant,
        8: purchaseFertilizer,
        9: viewFertilizer,
        10: viewAllFertilizer,
        11: viewAffectedPlants,
        12: viewAllEntries,
        13: viewTransactionsPerAction,
        14: dataReset,
    }
    # get the function and call it; handle invalid key input and stuff as well
    try:
        executeThisFunction = listOfFunctions[option]
        executeThisFunction()
    except KeyError:
        print("Invalid Input. Key does not Exist!")  # invalid key input
    except Exception as e:
        print(f"An error occurred: {e}")  # broader cases, unexpected errors


def askToContinue():
    continue_choice = input("Would you like to continue?: (y/n) ").lower().strip()
    while continue_choice not in ["y", "n", "yes", "no"]:
        print("Invalid Choice!")
        continue_choice = input("Would you like to continue?: (y/n) ")

    return continue_choice == "y" or continue_choice == "yes"


def generateID(entity_name):
    global plant_counter, fertilizer_counter, log_counter
    if entity_name == "plant":
        plant_counter += 1
        return f"P{plant_counter}"
    elif entity_name == "fertilizer":
        fertilizer_counter += 1
        return f"F{fertilizer_counter}"
    elif entity_name == "logbook":
        log_counter += 1
        return f"L{log_counter}"
    else:
        raise ValueError("Invalid counter name provided")


def checkDuplicates(name, to_check_dictionary, entity_type):
    # check for plant type
    if entity_type == "plant":
        if any(
                details["Plant Name"] == name for details in to_check_dictionary.values()
        ):  # check if there exists a plant name that is already in the dictionary
            print("Plant already exists! Please enter a new plant.")
            return True

    # check for fertilizer type
    elif entity_type == "fertilizer":
        return any(
            name == details["Fertilizer Name"]
            for details in to_check_dictionary.values()
        )

    return False  # default if not duplicates found


def validName(entity_type):
    """This function is to check if the input is valid for plant name"""
    validName = True
    if not all((word.replace("'","") or word.replace("-","")).isalpha() for word in entity_type.split()
    ):  # allows spaces and apostrophes but ensures words are alphabetic characters only
        validName = False

    return validName


def validatePlantStorage(value):
    """This function is to check if the input is valid for plant storage"""
    valid_storages = ["Outdoor", "Indoor"]
    shorthands = {"out": "Outside", "in": "Inside"}
    standardized_value = shorthands.get(value, value)  # standardize
    return standardized_value in valid_storages




""" Plants Functions """
###

def addPlant():
    """
    This function allows the user to add plants to the records.
    """
    global plants_details
    plantNourishment = {}  # Placeholder for nourishment details || resets every call

    while True:  # Loop until valid input is received
        plantName = input("Enter Plant's Name: ").strip().capitalize()

        # Check if plant name is valid and not a duplicate
        if checkDuplicates(plantName, plants_details, "plant") or not validName(
            plantName
        ):
            print("Invalid plant name or duplicate found. Please try again.")
            continue  # Ask for a new name if invalid
        break  # Exit the loop if the name is valid

    # Get plant storage input
    while True:
        plantStorage = input("Plant's Storage (Outdoor/Indoor): ").strip().capitalize()
        if validatePlantStorage(plantStorage):  # Check if input is valid
            break
        else:
            print("Invalid input. Please enter 'Outdoor' or 'Indoor'.")

    # Add the plant details
    plant_id = generateID("plant")
    generatePlantDetails(plant_id, plantName, plantStorage, plantNourishment)
    print(f"Plant added with ID: {plant_id}")

    # Log the addition of the plant
    addLogEntry(plant_id, "N/A", plantName, "N/A", "Add Plant")

    # Add plant to records
    addToRecords(plants_details, fertilizer_details, "p")

    # Ask if the user wants to add another plant
    if askToContinue():
        print("Great! Let's add another plant!")
        addPlant()
    else:
        print("Returning to main menu....")
        mainMenu("p")


def deletePlant():
    """

    This function allows user to delete plants


    """

    global plants_details
    # check if empty first
    if checkIfEmpty(plants_details):
        print("Unfortunately, there are no plants to delete!")
        mainMenu("p")  # return to main menu

    plants_copy = (
        plants_details.copy()
    )  # copy the plants details first to ensure no errors in looping later

    print("Here are the plants you may want to remove:\n")
    viewAll(plants_details, "plant")  # show all available plants to delete

    plant_to_delete = (
        input("Which plant do you want to remove?: (Enter its plant id or name) ")
        .strip()
        .capitalize()
    )

    plant_id = getID(
        plant_to_delete, plants_copy, "Plant Name"
    )  # get the id whether the user input name or id
    if plant_id is None:
        print("No plant found with that name or ID.")
        print("Returning to previous action")
        time.sleep(0.5)
        print("." * 5)
        deletePlant()  # call the function to prompt the user again

    # remove the delete plant if the user entered a valid id or name

    deleted_details = plants_details.pop(plant_id)  # remove the plant
    deleted_name = deleted_details.get("Plant Name", "N/A")  # store the deleted name
    print(f"Plant with plant ID: {plant_id} - (Name: {deleted_name}) has been removed.")
    addLogEntry(
        plant_id, "N/A", deleted_name, "N/A", "Delete Plant"
    )  # add to transaction records

    # ask if user wants to edit more plants
    if askToContinue():
        print("Great! Let's delete another plant!")
        deletePlant()  # call the function again
    else:
        print("Returning to main menu....")
        mainMenu("p")  # returns to main menu with options for plants


def viewPlant():
    """
    This function allows user to view plants they want

    """
    global plants_details

    if checkIfEmpty(plants_details):
        print("Unfortunately, there are no plants to view!")
        mainMenu("p")  # return to main menu

    to_view = (
        input("Which plant to do you want to view?: (Enter its plant name) ")
        .strip()
        .capitalize()
    )
    plant_id = getID(
        to_view, plants_details, "Plant Name"
    )  # find the plant id by matching the name

    if plant_id is None:
        print("Plant not found")
        print("Returning to previous action")
        time.sleep(0.5)
        print("." * 5)
        viewPlant()

    # plant id actually exist so view it
    plants_entry = {
        plant_id: plants_details[plant_id]
    }  # isolate the key value pair as a
    print("\nViewing Plants!")
    print("." * 5)
    time.sleep(0.5)
    view(plants_entry, "plant")
    # Ask if the user wants to view more plants
    if askToContinue():
        print("Great! Let's view another plant!")
        viewPlant()  # call the function again
    else:
        print("Returning to main menu....")
        mainMenu("p")


def editPlant():
    """
    This function allows user to edit plant they want

    """
    global plants_details
    if checkIfEmpty(plants_details):
        print("There are no plants to edit!")
        mainMenu("p")  # return to main menu
    plant_copy = plants_details.copy()  # copy again to avoid errors
    plant_to_edit = (
        input("Which plant do you want to edit?: (Enter its plant id or name) ")
        .strip()
        .capitalize()
    )
    plant_id = getID(plant_to_edit, plant_copy, "Plant Name")  # get the id

    if plant_id is None:
        # ask if user wants to edit more plants
        print("Plant not found!")
        print("Returning to previous action")
        time.sleep(0.5)
        print("." * 5)
        editPlant()

    # edit the details if user enters a valid plant id or name
    details = plant_copy[plant_id]  # get details of the plants
    removed_plant = details["Plant Name"]  # get the name
    removed_storage = details["Storage"]  # get the storage
    new_name = input("Enter a new plant's name: ").strip().capitalize()
    new_storage = (
        input("Enter a new storage ('Outdoor'/'Indoor') ").strip().capitalize()
    )
    plants_details[plant_to_edit]["Plant Name"] = new_name
    plants_details[plant_to_edit]["Storage"] = new_storage

    print(
        f"Plant name and storage with plant ID: {plant_id} (Previous Name: {removed_plant} || Previous Storage: {removed_storage}) has been edited."
    )

    # ask if user wants to edit more plants
    if askToContinue():
        print("Great! Let's edit another plant!")
        editPlant()  # call the function again
    else:
        print("Returning to main menu....")
        mainMenu("p")
        return


def updateNourishment():
    """
    This function allows user to add fertilizer or nourishment in their plants
    """
    global plants_details
    if checkIfEmpty(plants_details):
        print("No plants' records yet.")
        mainMenu("p")  # return to main menu

    viewAll(plants_details, "plant")  # view first

    fertilizer_name = (
        input("What is the name of the fertilizer you want to edit/add? ")
        .strip()
        .capitalize()
    )  # get fertilizer name

    # check if the fertilizer exists in any plant's records

    # this will be a flag
    fertilizer_found = any(
        fertilizer_name in details["Nourishment"] for details in plants_details.values()
    )

    # if the fertilizer does not exist, prompt to add either selected or all

    if not fertilizer_found:
        print(
            f"Fertilizer '{fertilizer_name}' does not exist in any plant's records yet."
        )
        add_new = (
            input(
                "Would you like to add it to a specific plant or all plants? (enter 'selected' or 'all'): "
            )
            .strip()
            .lower()
        )
        while add_new not in ["selected", "s", "all", "a"]:
            add_new = (
                input(
                    "Would you like to add it to a specific plant or all plants? (enter 'selected' or 'all'): "
                )
                .strip()
                .lower()
            )

        addToPlants(
            fertilizer_name, add_new
        )  # add to plants depending on the mode selected

    # Update fertilizer amount
    updateFertilizerAmount(fertilizer_name)

    # Option to update more
    if askToContinue():
        print("Let's update more!")
        updateNourishment()
    else:
        print("Returning to main menu...")
        mainMenu("p")


def nourishPlant():
    """
    This function allows user to use fertilizer to nourish their plant
    """
    global plants_details
    global fertilizer_details
    if checkIfEmpty(plants_details):
        print("No plants' records yet.")
        mainMenu("p")  # return to main menu

    """
        a. ask for the plant's name they want to nourish
        b. check if amount needed in the plant nourishment can be serviced by the fertilizer dictionary
        c. subtract amount if enough from the stock amount in fertilizer dictionary
        d. if not enough, error message
        f. log entry
        
    """

    to_nourish = (
        input("Enter the plant's name you want to nourish: ")
        .strip()
        .capitalize()
        .split(",")
    )

    for p_name in to_nourish:
        p_id = getID(p_name, plants_details, "Plant Name")  # check if the input exists
        if p_id is None:
            print(f"Plant: {p_name} is not found in the records!")
            continue  # go to the next item in the input

        useFertilizer(p_name, p_id, plants_details)
        fertilizer_name = next(iter(plants_details[p_id]["Nourishment"]))
        f_id = getID(fertilizer_name, fertilizer_details, "Fertilizer Name")
        addLogEntry(p_id, f_id, p_name, fertilizer_name, "Nourish")

    if askToContinue():
        print("Great! Let's nourish more plants!")
        nourishPlant()
    else:
        print("Returning to Main Menu...")
        mainMenu("p")



""" Fertilizer Functions """


def purchaseFertilizer():
    """
    A function that allows user to buy fertilizers
    """
    global fertilizer_details

    fertilizerName = input("Enter Fertilizer's Name: ").strip().capitalize()
    amountPurchased = float(input("Enter amount purchased: "))
    supplierName = input("Enter supplier's name: ").strip().capitalize()

    if checkDuplicates(
        fertilizerName, fertilizer_details, "fertilizer"
    ):  # update details if input exist already
        updateExisting(fertilizerName, amountPurchased, supplierName)
        print(
            f"Fertilizer ({fertilizerName}) already exists. Previous entry has been updated."
        )

    # add new details

    fertilizer_id = generateID("fertilizer")
    generateFertilizerDetails(
        fertilizer_id, fertilizerName, amountPurchased, supplierName
    )
    print(f"Fertilizer added with ID: {fertilizer_id}")

    addLogEntry("N/A", fertilizer_id, "N/A", fertilizerName, "Purchase")
    addToRecords(plants_details, fertilizer_details, "f")

    # ask if user wants to add more plants
    if not askToContinue():
        print("Returning to main menu....")
        mainMenu("f")
        return
    else:
        print("Great! Let's add another fertilizer!")
        purchaseFertilizer()  # call the function again


def viewFertilizer():
    """
    View Selected Fertilizers
    """
    global fertilizer_details
    if checkIfEmpty(fertilizer_details):
        print("Unfortunately, there are no fertilizers to view!")
        mainMenu("f")
    to_view = (
        input("Which fertilizer to do you want to view?: (Enter its fertilizer name) ")
        .strip()
        .capitalize()
    )
    fertilizer_id = getID(to_view, fertilizer_details, "Fertilizer Name")
    if fertilizer_id is None:
        print(f"Fertilizer ID not found!")
        viewFertilizer()  # call the function again

    fertilizer_entry = {
        fertilizer_id: fertilizer_details[fertilizer_id]
    }  # store what you need to view
    view(fertilizer_entry, "fertilizer")
    print("Viewing fertilizer!\n")

    if askToContinue():
        print("Great! Let's view another fertilizer!")
        viewFertilizer()  # call the function again

    else:
        print("Returning to main menu....")
        mainMenu("f")
        return


def viewAllFertilizer():
    global fertilizer_details
    if checkIfEmpty(fertilizer_details):
        print("Unfortunately, there are no fertilizers to view!")
        mainMenu("f")  # return to main menu
    print("\nViewing all fertilizers!")
    viewAll(fertilizer_details, "fertilizer")
    mainMenu("f")


def viewAffectedPlants():
    global plants_details
    global fertilizer_details

    # Check if fertilizer records are empty
    if checkIfEmpty(fertilizer_details):
        print("Fertilizer records are empty!")
        mainMenu("f")  # return to main menu

    # Input fertilizer IDs from user (allow multiple entries)
    to_compare = (
        input("Enter fertilizer ID(s): (Separate multiple IDs with commas ',')  ")
        .strip()
        .capitalize()
        .split(",")
    )

    # Initialize an empty dictionary to hold all affected plants for all fertilizers
    all_affected_plants = {}

    for f_id in to_compare:
        # Ensure that the fertilizer ID is valid
        if f_id not in fertilizer_details:
            print(f"Fertilizer ID {f_id} not found in records.")
            continue  # Skip this fertilizer ID if it's not valid

        # Get and add affected plants for the current fertilizer
        affected_plants = addAffected(f_id)

        # If affected plants exist, merge with the global affected plants dictionary
        if affected_plants:
            all_affected_plants.update(affected_plants)

    # Display results
    if all_affected_plants:
        viewAll(all_affected_plants, "affected")
        print("Viewing affected plants!")
    else:
        print("No plants are affected by the fertilizers provided.")

    mainMenu("f")


""" Logbook Functions """


def viewAllEntries():

    to_pass = "o"

    readFile(to_pass)
    mainMenu("l")


def viewTransactionsPerAction():
    synonyms = {
        "o": "ordinary",
        "a": "Add Plant",
        "d": "Delete Plant",
        "p": "Purchase",
        "n": "Nourish",
    }

    to_filter = (
        input(
            f"What do you want to filer or view? (enter 'o' for default)\nThe choices are: {list(synonyms.items())} "
        )
        .lower()
        .strip()
    )
    while to_filter not in ["o", "a", "d", "p", "n"]:
        to_filter = input("What do you want to filer or view? (enter 'o' for default) ")

    readFile(to_filter)
    mainMenu("l")


def dataReset():
    global plants_details, fertilizer_details
    confirmed = False
    confirmation = input("Are you certain with your choice?: ").strip().lower()
    while confirmation not in ["y", "n", "no", "yes"]:
        confirmation = input("Are you certain with your choice?: ").strip().lower()
    if confirmation in ["y", "yes"]:
        plants_details.clear() # remove the content of the current plant entries
        fertilizer_details.clear() # remove the content of the current fertilizer entries
        
        """ Remove from records """

        with open(records_path, "w"):
            pass  # overwrite, just open then close the file

        with open(transactions_path, "w"):
            pass  # overwrite, just open then close the file

        with open(counters_path,"w") as counter_file:
            counter_file.write(str({"plant_counter": 0, "fertilizer_counter": 0, "log_counter": 0}))



        confirmed = True

    if confirmed:
        print("Data reset! All records have been erased!")
    else:
        print("Returning back to main menu")
        time.sleep(0.5)
        print(". . .")

    mainMenu("l")






""" Other Functions """

def askForPassword():
    return int(input("Enter the password to decrypt the records. "))

def readFile(filter_details):
    synonyms = {
        "o": "Ordinary",
        "a": "Add Plant",
        "d": "Delete Plant",
        "p": "Purchase",
        "n": "Nourish",
    }

    # Resolve the filter name using synonyms dictionary
    filter_details = synonyms.get(filter_details, filter_details)

    # Ensure file exists before attempting to read
    if not os.path.exists(transactions_path):
        print("File does not exist!\n")
        return

    found = False
    with open(transactions_path, "r") as r:
        for counter, line in enumerate(r, start=1):
            line = line.strip()  # Removes extra whitespace
            if filter_details == "Ordinary":  # print each line
                print(f"\nReading entry #{counter}...")
                print("--" * 50)
                time.sleep(0.7)
                print(f"\n{line}")
                found = True

            elif filter_details in synonyms:
                if (
                        filter_details in line
                ):  # print only the lines that has the substring of the filter_details
                    print(f"\nReading entry #{counter}...")
                    print("--" * 50)
                    time.sleep(0.7)
                    print(f"\n{line}")
                    found = True

    if not found:
        print(f"No entries found.")

def addLogEntry(p_id, f_id, p_name, f_name, action_type):
    logbook_id = generateID("logbook")
    selected_date = input("Enter Date (day/month/year) separated by '/' ")
    current_date = selected_date.split('/') # will return the list of dates
    formatted_date = " ".join(current_date)
    with open(transactions_path, "a") as f:
        if action_type == "Add Plant" or action_type == "Delete Plant":
            f.write(
                f"Log ID: {logbook_id} || {p_id} - {p_name} || {f_id} - {f_name} || Date: {formatted_date} || Action : {action_type}\n"
            )
        elif action_type == "Purchase":
            f.write(
                f"Log ID: {logbook_id} || {p_id} - {p_name} || {f_id} - {f_name}|| Date: {formatted_date} || Action : {action_type}\n"
            )

        elif action_type == "Nourish":
            f.write(
                f"Log ID: {logbook_id}|| {p_id}:  {p_name} || {f_id} - {f_name}|| Date: {formatted_date} || Action : {action_type}\n"
            )
        else:
            print(f"'{action_type}' not recorded in our logbook!")

    print("Log entry added!")

def addAffected(f_id):
    """
    This function checks for plants affected by the given fertilizer ID.
    It adds affected plants to a dictionary and returns it.
    """
    affected_plants = {}

    # Get the fertilizer details for the current fertilizer ID
    fertilizer_to_check = fertilizer_details[f_id]
    fertilizer_name = fertilizer_to_check["Fertilizer Name"]

    # Loop over all plants and check if their nourishment matches the fertilizer
    for p_id, p_details in plants_details.items():
        if fertilizer_name in p_details["Nourishment"]:
            # If the fertilizer affects this plant, add it to the dictionary
            print(f"Match found! Plant {p_details['Plant Name']} is affected.")
            if f_id not in affected_plants:
                affected_plants[f_id] = {
                    "Fertilizer Name": fertilizer_name,
                    "Stock Amount": fertilizer_to_check["Amount Purchased"],
                    "Last Supplier": fertilizer_to_check["Supplier Name"],
                    "Affected Plants": {},
                }
            affected_plants[f_id]["Affected Plants"][p_id] = p_details["Plant Name"]

    return affected_plants


def generatePlantDetails(plant_id, plant_name, plant_storage, plant_nourishment):
    """This function is to generate the plant details"""
    global plants_details
    plants_details[plant_id] = {
        "Plant Name": plant_name,
        "Storage": plant_storage,
        "Nourishment": plant_nourishment,
    }

def generateFertilizerDetails(id, name, purchased, supplier):
    """This function is to generate the fertilizer details"""
    global fertilizer_details
    fertilizer_details[id] = {
        "Fertilizer Name": name,
        "Amount Purchased": purchased,
        "Supplier Name": supplier,
    }


def updateExisting(name, purchased, supplier):
    global fertilizer_details
    for (
            fertilizer_id,
            details,
    ) in fertilizer_details.items():  # iterate over the values
        if details["Fertilizer Name"] == name:  # if it exists already
            details["Amount Purchased"] += purchased  # update amount
            details["Supplier Name"] = supplier  # update supplier
            break

    return


def display_plant(iterable):
    """
    # '<4' means the string will be left-aligned four characters wide, since '#' takes 1 character it will have 3 spaced after it || all follows the same principle
    Which means, The '#' column takes up 4 characters, 'ID' takes 10 characters, 'Name' takes 20, Storage takes 10, and 'Nourishment' takes 20.
    """
    print(
        f"\n{'#':<4} {'ID':<10} {'Plant Name':<20} {'Storage':<10} {'Nourishment Name':<20} {'Nourishment Needed':<20}"
    )
    print("-" * 100, end="")
    for i, (plant_id, details) in enumerate(iterable.items(), start=1):
        name = details.get("Plant Name", "N/A")  # default is "N/A"
        storage = details.get("Storage", "N/A")  # default is "N/A"
        nourishment_details = details.get("Nourishment", {})
        if nourishment_details:  # Check if "Nourishment" is not empty
            nourishment_name, nourishment_amount = next(
                iter(nourishment_details.items())
            )  # Get the first key-value pair
        else:
            nourishment_name, nourishment_amount = "N/A", "N/A"

        print(
            f"\n{i:<4} {plant_id:<10} {name:<20} {storage:<10} {nourishment_name:<20} {nourishment_amount:<20}"
        )


def display_fertilizer(iterable):
    print(
        f"\n{'#':<4} {'ID':<10} {'Fertilizer Name':<20} {'Amount Purchased':<20} {'Supplier Name':<20}"
    )
    print("-" * 70)
    for i, (fertilizer_id, details) in enumerate(iterable.items(), start=1):
        name = details.get("Fertilizer Name", "N/A")
        amount = details.get("Amount Purchased", "N/A")
        supplier = details.get("Supplier Name", "N/A")
        print(f"{i:<4} {fertilizer_id:<10} {name:<20} {amount:<20} {supplier:<20}")


def display_affected(iterable):
    # display headers
    print(
        f"\n{'#':<4} {'ID':<10} {'Name':<20} {'Stock Amount':<20} {'Last Supplier':<20} {'Affected Plants ID':<30} {'Affected Plants Name':<30}"
    )
    print("-" * 180, end="")

    # get and display the details of the selected plant
    for i, (fertilizer_id, details) in enumerate(iterable.items(), start=1):
        name = details.get("Fertilizer Name", "N/A")  # default is "N/A"
        amount = details.get("Stock Amount", "N/A")
        supplier = details.get("Last Supplier", "N/A")  # default is "N/A"
        affected = details.get("Affected Plants", {})  # get the plant details
        affected_id, affected_name = next(
            iter(affected.items())
        )  # get the first key-value pair

        # print the details
        print(
            f"\n{'1':<4} {fertilizer_id:<10} {name:<20} {amount:<20} {supplier:<20} {affected_id:<30} {affected_name:<30}"
        )


def viewAll(iterable, entity_type):
    """
    Display the contents of the iterable based on entity_type.
    """
    if iterable is None or not iterable:  # check if none type or empty
        print("It is empty!\n")
        return

    handlers = {
        "plant": display_plant,
        "fertilizer": display_fertilizer,
        "affected": display_affected,
    }
    handler = handlers.get(entity_type)  # get the value function
    if handler:
        handler(iterable)  # execute the function

    else:
        print(f"Viewing for '{entity_type}' is not possible.")

    print()  # just extra line for cleaner look


def view(iterable, entity_type):
    """
    Display the contents of the iterable based on entity_type.
    """
    if iterable is None or not iterable:  # check if none type or empty
        print("It is empty!")
        return

    handlers = {"plant": display_plant, "fertilizer": display_fertilizer}
    handler = handlers.get(entity_type)  # get the value function
    if handler:
        handler(iterable)  # execute the function

    else:
        print(f"Viewing for '{entity_type}' is not possible.")

    print()  # just extra line for cleaner look

def useFertilizer(name, ID, iterable):
    """
    A function that subtracts the nourishment from the stock amount

    """
    current_details = iterable.get(ID, "N/A")
    current_nourishment = current_details.get("Nourishment", {})
    f_name, subtract_with = next(
        iter(current_nourishment.items())
    )  # get the first value pair

    if checkDuplicates(f_name, fertilizer_details, "fertilizer"):  # check if it exists
        f_id = getID(f_name, fertilizer_details, "Fertilizer Name")
        f_details = fertilizer_details.get(f_id)
        amount_purchased = f_details["Amount Purchased"]
        if amount_purchased >= subtract_with:
            print(
                f"{ID} : {name} has been nourished successfully, Stock of Fertilizer Purchased : {amount_purchased} || Used: {subtract_with}"
            )
            amount_purchased -= subtract_with
            print(f"{f_id} - {f_name} || Current Stock : {amount_purchased}")
            return
        else:
            print(
                f"Not enough stock! Fertilizer Stock:{amount_purchased} || Trying to consume : {subtract_with}"
            )

    print(
        f"Nourishment is possible as {f_name} does not exist in the fertilizer records."
    )


def addToPlants(fertilizer_name, selected):

    selected_standardized = {"s": "selected", "a": "all"}
    selected = selected_standardized.get(selected, selected)

    if selected == "selected":
        addToSelectedPlant(fertilizer_name)

    elif selected == "all":
        addToAllPlants(fertilizer_name)

    else:
        print(f"{selected} is not an available mode yet.")


def addToAllPlants(fertilizer_name):
    """Add fertilizer to plants"""
    for details in plants_details.values():  # iterate all values in the plants' records
        details["Nourishment"][fertilizer_name] = ""

    print(f"Fertilizer '{fertilizer_name}' added to all plants with an empty value.")

    return


def addToSelectedPlant(fertilizer_name):
    """Add fertilizer to a selected plant"""
    while True:
        plant_selected = input("Enter the plant's name or ID: ").strip().capitalize()
        for plant_id, details in plants_details.items():
            if (
                plant_selected == plant_id or plant_selected == details["Plant Name"]
            ):  # check if the input matches the name or id of the current plant record
                details["Nourishment"][
                    fertilizer_name
                ] = ""  # add the fertilizer name with empty value
                print(
                    f"Fertilizer '{fertilizer_name}' added to plant '{details['Plant Name']}' with an empty value."
                )
                return

        print(f"No plant found with name or ID '{plant_selected}'.")


def updateFertilizerAmount(fertilizer_name):
    """Update the amount of a given fertilizer in all plants where it exists."""
    new_amount = int(
        input(f"Enter the new nourishment amount for '{fertilizer_name}': ")
    )
    # iterate over the values of the dictionary
    for details in plants_details.values():
        if (
            fertilizer_name in details["Nourishment"]
        ):  # check if the fertilizer name exist in the current plant record
            details["Nourishment"][
                fertilizer_name
            ] = new_amount  # key : value || name : amount

    print(f"Fertilizer - '{fertilizer_name}' updated to '{new_amount}'.")




""" Files Functions"""


def addToRecords(p, f, mode_type):  # a function that stores all the records of the user
    with open(records_path, "a") as r_path:
        if mode_type == "p":  # for plant
            for (
                    p_id,
                    p_details,
            ) in p.items():  # iterate over the plants records and then add to the file
                p_name = p_details.get("Plant Name", "N/A")
                p_storage = p_details.get("Plant Storage", "N/A")
                p_nourishment = p_details.get("Nourishment", {})
                # get nourishment details
                if p_nourishment:
                    nourishment_name, nourishment_amount = next(
                        iter(p_nourishment.items())
                    )
                else:
                    nourishment_name, nourishment_amount = "N/A", "N/A"
                r_path.write(
                    f"{p_id} || {p_name} || {p_storage} || {nourishment_name} || {nourishment_amount}\n"
                )
        elif mode_type == "f":  # for fertilizer
            with open(records_path, "a") as r_path:
                for (
                        f_id,
                        f_details,
                ) in (
                        f.items()
                ):  # iterate over the plants records and then add to the file
                    f_name = f_details.get("Fertilizer Name", "N/A")
                    f_stock = f_details.get("Amount Purchased", "N/A")
                    f_supplier = f_details.get("Supplier Name", "N/A")
                    r_path.write(f"{f_id} || {f_name} || {f_stock} || {f_supplier}\n")

        else:
            print(
                f"We are very sorry, such mode type - {mode_type} is not included in our records yet."
            )

def loadFile():
    global plants_details
    global fertilizer_details
    if os.path.exists(records_path):
        with open(
                records_path, "r"
        ) as r_path:  # read the file ; iterate through it then add
            for line in r_path:
                line = line.strip()  # remove extra white space first
                parts = line.split(" || ")  # split into list
                if len(parts) == 5:
                    (
                        plant_id,
                        plant_name,
                        storage,
                        nourishment_name,
                        nourishment_amount,
                    ) = parts # unpack
                    plants_details[plant_id] = (
                        {  # get each element then add to the dictionary
                            "Plant Name": plant_name,
                            "Storage": storage,
                            "Nourishment": {nourishment_name: nourishment_amount},
                        }
                    )
                elif len(parts) == 4:
                    (
                        fertilizer_id,
                        fertilizer_name,
                        stock_amount,
                        last_supplier,
                    ) = parts # unpack
                    fertilizer_details[fertilizer_id] = {
                        "Fertilizer Name": fertilizer_name,
                        "Amount Purchased": stock_amount,
                        "Supplier Name": last_supplier,
                    }
            print(
                f"Loaded {len(plants_details)} plant/s and {len(fertilizer_details)} fertilizer/s."
            )
    else:
        print("No file to load!")

def encrypt(file_path):
    if os.path.exists(file_path):
        caesar_cipher(file_path, +3)

    else:

        print("File does not exist")


def decrypt(file_path):
    if os.path.exists(file_path):
        caesar_cipher(file_path, -3)

    else:
        print("File does not exist")


def caesar_cipher(file, shift):
    with open(file, "r") as f:
        lines = f.readlines()  # Read all lines from the file

    encrypted_lines = []  # Store encrypted lines

    for line in lines:
        content = ""  # Initialize empty string for encrypted line
        for ch in line:
            if ch.isalpha():  # Check if character is alphabetic
                shift_base = 65 if ch.isupper() else 97  # Use ASCII base for case
                # Perform Caesar cipher shift
                new_ch = chr((ord(ch) - shift_base + shift) % 26 + shift_base) 
                content += new_ch
            else:
                # Non-alphabetic characters remain unchanged
                content += ch
        encrypted_lines.append(content)  # Add processed line to result

    # Write encrypted lines back to the file
    with open(file, "w") as f:
        f.writelines(encrypted_lines)


def loadCounters():
    """Load counters from a JSON file"""
    if os.path.exists(counters_path):
        with open(counters_path, "r") as f:
            counter = f.readline()
            string = counter.strip("{}") # remove the curly braces
            pairs = string.split(",") # split the string into key:value pairs

            # use a dictionary comprehension to creat
            # the dictionary, converting the values to
            # integers and removing the quotes from the keys

        return {key[1:-1]: int(value) for key, value in (pair.split(':') for pair in pairs)}
    
    else:
        # If the file doesn't exist, return default counters
        return {"plant_counter": 0, "fertilizer_counter": 0, "log_counter": 0}

def saveCounters(counters):
    """Save counters to a file"""
    with open(counters_path, "w") as f:
        f.write(str(counters))


""" Start Program """

if os.path.exists(records_path):
    # Load counters from the storage file
    counters = loadCounters()
    plant_counter = counters.get("plant_counter", 0)
    fertilizer_counter = counters.get("fertilizer_counter", 0)
    log_counter = counters.get("log_counter", 0)

    # Decrypt both files before starting the program
    decrypt(records_path)
    decrypt(transactions_path)

    # Get the details
    loadFile()


ascii_art = """


██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗██╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝██║
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  ██║
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ╚═╝
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗██╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝

"""
print(ascii_art)
# run the program
mainMenu("start")

""" References """

# w3schools.com
