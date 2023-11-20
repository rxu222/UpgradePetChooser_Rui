# Rui Xu
# Purpose: for Upgrade Pet Chooser assignment

# Import the MySQL Connector Python library to connect pycham to MySQL database
import mysql.connector
# Import the configuration settings
from configure import config
# Import the Pets class
from pet_class import Pets


# Function to connect to the MySQL database
def connect_to_database():
    try:
        # Establish a database connection using the provided configuration
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as e:  # Handle any connection errors
        print(f"Error connecting to the database: {e}")


# Function to retrieve data from the database and create Pets objects
def retrieve_pet_info(connection):
    cursor = connection.cursor()
    try:
        # SQL query to retrieve pet information from multiple tables
        query = """
        SELECT 
            pets.id, 
            pets.name, 
            pets.age, 
            types.animal_type,
            owners.name
        FROM pets
        JOIN types ON pets.animal_type_id = types.id
        JOIN owners ON pets.owner_id = owners.id;
        """
        cursor.execute(query)  # Execute the SQL query
        pet_info_data = cursor.fetchall()  # Fetch the query results as pet_info_data

        pets_list = []  # Create a list to store Pets objects
        for row in pet_info_data:
            pet = Pets(*row)  # Create a Pets object from each row of data
            pets_list.append(pet)  # Add the Pets object to the list

        return pets_list  # Return the list of Pets objects

    except mysql.connector.Error as e:  # Handle any query execution errors
        print(f"Error retrieving pet information: {e}")

    finally:
        cursor.close()  # Close the cursor no matter an exception is raised or not


# Define a list of pet names and allow the user to choose a pet
def display_pet_list(pets_list):
    print("Please input a number to choose a pet from the list below:")
    for i, pet in enumerate(pets_list):  # Keep track of both the item's index and its value
        print(f"[{i + 1}] {pet.pet_name}")  # Display each pet's name with a number (start from 1)
    print("[Q] Quit")  # Option to quit the program

# Function to edit a pet's name and age
def edit_pet(pets_list, index):
    pet = pets_list[index]
    print(f"You have chosen to edit {pet.pet_name}.")

    new_name = input("New name: ").strip()
    # Check if the user input to quit and exit without saving changes
    if new_name.lower() == "quit":
        print("Exiting without saving changes.")
        return True  # Signal to exit without saving changes

    # If a new name is provided, update the pet's name and display the change
    if new_name:
        pet.pet_name = new_name
        print(f"The pet's name has been updated to {new_name}.")

    # Continuously prompt the user for a new age until a valid integer or quit command is entered
    while True:
        new_age = input("New age: ").strip()

        # Check if the user input to quit and exit without saving changes
        if new_age.lower() == "quit":
            print("Exiting without saving changes.")
            return True  # Signal to exit without saving changes

        # Check if the input is a valid integer
        if new_age.isdigit():
            pet.pet_age = int(new_age)
            print(f"The pet's age has been updated to {new_age}.")
            break  # Exit the loop after successfully updating age
        else:
            print("Please enter a valid integer for the age.")

    return False  # Signal to continue with the updated changes

# Main function to start choose!
def main():
    connection = connect_to_database()
    pet_info_data = retrieve_pet_info(connection)  # Retrieve the updated pet information
    # Start an infinite loop for user interaction
    while True:
        display_pet_list(pet_info_data)  # Display the list of pet names
        choice = input("Choice: ")  # Prompt the user for their choice

        if choice.lower() == "q":
            break  # Exit the loop and end the program when the user wants to quit
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(pet_info_data):
                pet = pet_info_data[choice - 1]  # Subtract 1 from the user's choice to match the true index
                # Get the selected pet object
                # Print the information for the selected pet
                print(str(pet))

                # Check the user's chosen action
                action = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet? ").strip().lower()
                if action == "c":
                    continue
                elif action == "q":
                    break
                elif action == "e":
                    edit_pet(pet_info_data, choice - 1)
                    continue
                else:
                    print("Invalid choice. Please choose a valid option.")
            else:
                print("Invalid choice. Please choose a valid option.")
        else:
            print("Invalid choice. Please choose a valid option.")

    # Close the database connection when the program ends
    connection.close()

# Call the main function and try to catch any error
try:
    main()
except ValueError as ve:
    print(f"ValueError: {ve}")
except EOFError as ee:
    print(f"EOFError: {ee}")
