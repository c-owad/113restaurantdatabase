import sqlite3

def setup_database():
    # Connect to the database (this creates the .db file if it doesn't exist)
    con = sqlite3.connect('pgh_restaurants.db')
    cur = con.cursor()

    # Create the restaurants table if it isn't already there
    cur.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            neighborhood TEXT,
            cuisine TEXT,
            rating INTEGER,
            visited TEXT
        )
    ''')
    
    # Save the changes and close the connection for now
    con.commit()
    con.close()
    print("Database and 'restaurants' table ready to go!")

def add_restaurant():
    print("\n--- Add a New Restaurant ---")
    
    # 1. Get input from the user
    name = input("Restaurant Name: ")
    neighborhood = input("Neighborhood (e.g., Oakland, Squirrel Hill): ")
    cuisine = input("Cuisine (e.g., Thai, Burgers): ")
    rating_input = input("Rating 1-5 (Press Enter to skip if you haven't been): ")
    visited = input("Have you visited? (Yes/No): ")

    # Handle the optional rating so it goes in as an integer or NULL (None in Python)
    rating = int(rating_input) if rating_input.isdigit() else None

    # 2. Connect to the database
    con = sqlite3.connect('pgh_restaurants.db')
    cur = con.cursor()

    # 3. Execute the INSERT statement using parameterized queries (?)
    # Note: We don't insert 'id' because SQLite automatically generates it for us!
    cur.execute('''
        INSERT INTO restaurants (name, neighborhood, cuisine, rating, visited)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, neighborhood, cuisine, rating, visited))

    # 4. Save and close
    con.commit()
    con.close()
    
    print(f"\n✅ Successfully added '{name}' to your tracker!")

def view_restaurants():
    print("\n--- View Restaurants ---")
    print("1. Show all restaurants")
    print("2. Search by neighborhood")
    print("3. Show all, sorted by highest rating")
    
    choice = input("Choose an option (1-3): ")
    
    # Connect to the database
    con = sqlite3.connect('pgh_restaurants.db')
    cur = con.cursor()
    
    # Execute the correct SELECT statement based on the user's choice
    if choice == '1':
        cur.execute("SELECT * FROM restaurants")
        results = cur.fetchall()
        
    elif choice == '2':
        search_hood = input("Enter neighborhood (e.g., Oakland, Strip District): ")
        # Using a parameterized query (?) to filter safely based on user input!
        cur.execute("SELECT * FROM restaurants WHERE neighborhood = ?", (search_hood,))
        results = cur.fetchall()
        
    elif choice == '3':
        # ORDER BY sorts the data. DESC means descending (highest to lowest).
        cur.execute("SELECT * FROM restaurants ORDER BY rating DESC")
        results = cur.fetchall()
        
    else:
        print("Invalid choice. Returning to main menu.")
        con.close()
        return

    # Display the results neatly
    if not results:
        print("\nNo restaurants found matching that criteria.")
    else:
        print("\nID | Name | Neighborhood | Cuisine | Rating | Visited")
        print("-" * 65)
        for row in results:
            # 'row' is a tuple containing the data for one restaurant
            # We use string formatting just for printing, which is perfectly safe
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
            
    # Close the connection
    con.close()

def update_restaurant():
    print("\n--- Update a Restaurant ---")
    
    con = sqlite3.connect('pgh_restaurants.db')
    cur = con.cursor()
    
    # 1. Let the user search for the restaurant first
    search_term = input("Enter the name (or part of the name) of the restaurant you want to update: ")
    
    # The % signs act as wildcards in SQL, meaning "anything before or after this text"
    search_pattern = f"%{search_term}%"
    cur.execute("SELECT id, name, neighborhood, rating FROM restaurants WHERE name LIKE ?", (search_pattern,))
    matches = cur.fetchall()
    
    # 2. Check if we found anything
    if not matches:
        print(f"\n⚠️ No restaurants found matching '{search_term}'.")
        con.close()
        return  # Exit the function early if nothing is found
        
    # 3. Display the matches so the user can see the IDs
    print("\nFound the following matches:")
    print("ID | Name | Neighborhood | Current Rating")
    print("-" * 50)
    for row in matches:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        
    # 4. Now ask for the specific ID to update
    target_id = input("\nEnter the ID of the exact restaurant you want to update: ")
    
    # 5. Get the new data
    new_rating_input = input("What is your new rating (1-5)? (Press Enter to keep current): ")
    new_visited_input = input("Have you visited? (Yes/No) (Press Enter to keep current): ")
    
    # If the user pressed Enter to skip, we don't update that field. 
    # To keep it simple for this assignment, let's just update both fields based on whatever they type,
    # or you can write logic to only update the fields they provided. 
    # Let's keep it straightforward for now:
    if new_rating_input and new_visited_input:
         cur.execute('''
            UPDATE restaurants 
            SET rating = ?, visited = ?
            WHERE id = ?
        ''', (new_rating_input, new_visited_input, target_id))
         con.commit()
         print(f"\n✅ Successfully updated restaurant ID {target_id}!")
    else:
         print("\n⚠️ Update canceled: You must provide both a rating and visit status for this basic version.")

    con.close()

def delete_restaurant():
    print("\n--- Delete a Restaurant ---")
    
    con = sqlite3.connect('pgh_restaurants.db')
    cur = con.cursor()
    
    # 1. Let the user search for the restaurant first
    search_term = input("Enter the name (or part of the name) of the restaurant you want to delete: ")
    search_pattern = f"%{search_term}%"
    
    cur.execute("SELECT id, name, neighborhood, rating FROM restaurants WHERE name LIKE ?", (search_pattern,))
    matches = cur.fetchall()
    
    # 2. Check if we found anything
    if not matches:
        print(f"\n⚠️ No restaurants found matching '{search_term}'.")
        con.close()
        return  # Exit early if nothing is found
        
    # 3. Display the matches so the user can verify the ID
    print("\nFound the following matches:")
    print("ID | Name | Neighborhood | Current Rating")
    print("-" * 50)
    for row in matches:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        
    # 4. Ask for the specific ID to delete
    target_id = input("\nEnter the ID of the exact restaurant you want to delete: ")
    
    # 5. Confirm the deletion
    confirm = input(f"Are you SURE you want to permanently delete restaurant ID {target_id}? (y/n): ")
    
    if confirm.lower() == 'y':
        # Execute the DELETE statement using parameterized queries
        cur.execute("DELETE FROM restaurants WHERE id = ?", (target_id,))
        con.commit()
        
        # Check if a row was actually deleted
        if cur.rowcount > 0:
            print(f"\n🗑️ Successfully deleted restaurant ID {target_id}.")
        else:
            print(f"\n⚠️ No restaurant found with ID {target_id}.")
    else:
        print("\nDeletion canceled.")
        
    con.close()

def main_menu():
    while True:
        print("\n" + "="*35)
        print("🍔 PGH Restaurant Tracker 🍟")
        print("="*35)
        print("1. Add a new restaurant")
        print("2. View restaurants")
        print("3. Update a restaurant")
        print("4. Delete a restaurant")
        print("5. Quit")
        
        choice = input("\nChoose an option (1-5): ")
        
        if choice == '1':
            add_restaurant()
        elif choice == '2':
            view_restaurants()
        elif choice == '3':
            update_restaurant()
        elif choice == '4':
            delete_restaurant()
        elif choice == '5':
            print("\nClosing tracker. Go eat something good! 👋")
            break  # This stops the while loop and exits the app
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 5.")

# Run the setup function when the script executes
if __name__ == '__main__':
    main_menu()