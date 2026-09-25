import mysql.connector

# Connect to MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="STUDENT",
    database="spacetracker"
)

cursor = con.cursor()

def get_valid_id():
    while True:
        try:
            object_id = int(input("Enter object ID: "))

            if object_id <= 0:
                print("Object ID must be a positive number.")
                continue

            return object_id

        except ValueError:
            print("Invalid ID. Please enter a number.")

def AddObject():
    print("\n========== ADD SPACE OBJECT ==========")

    object_id = get_valid_id()

     # Check if the ID already exists
    cursor.execute(
        "SELECT object_id FROM space_objects WHERE object_id = %s",
        (object_id,)
    )

    if cursor.fetchone() is not None:
        print("\nError: An object with this ID already exists.")
        return

    while True:
        name = input("Enter object name: ").strip()

        if name:
            break

        print("Object name cannot be empty.")

    valid_types = ["Asteroid", "Comet", "Meteoroid", "Satellite"]

    while True:
        object_type = input("Enter object type: ").strip().title()

        if object_type in valid_types:
            break

        print("Invalid object type.")
        print("Choose: Asteroid, Comet, Meteoroid, or Satellite.")

    size = input("Enter size: ")

    while True:
        distance = input("Enter distance from Earth: ").strip()

        if distance:
            break

        print("Distance cannot be empty.")

    shape = input("Enter shape: ")
    status = input("Enter status: ")

    sql = """
        INSERT INTO space_objects
        (object_id, name, object_type, size, distance, shape, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        object_id,
        name,
        object_type,
        size,
        distance,
        shape,
        status
    )

    try:
        cursor.execute(sql, values)
        con.commit()
        print("\nObject added successfully!")

    except mysql.connector.IntegrityError:
        print("\nError: An object with this ID already exists.")

def ViewObjects():
    print("\n" + "=" * 80)
    print("                         SPACE OBJECTS")
    print("=" * 80)

    cursor.execute("SELECT * FROM space_objects")

    data = cursor.fetchall()

    if not data:
        print("No space objects found.")
        return

    print(
        f"{'ID':<6}"
        f"{'NAME':<15}"
        f"{'TYPE':<13}"
        f"{'SIZE':<15}"
        f"{'DISTANCE':<20}"
        f"{'STATUS':<15}"
    )

    print("-" * 80)

    for row in data:
        print(
            f"{row[0]:<6}"
            f"{row[1]:<15}"
            f"{row[2]:<13}"
            f"{row[3]:<15}"
            f"{row[4]:<20}"
            f"{row[6]:<15}"
        )

    print("=" * 80)

def SearchObject():
    print("\n========== SEARCH SPACE OBJECT ==========")

    print("1. Search by Name")
    print("2. Search by Type")
    print("3. Search by Status")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter object name: ")

        sql = """
            SELECT * FROM space_objects
            WHERE name = %s
        """
        cursor.execute(sql, (name,))

    elif choice == "2":
        object_type = input("Enter object type: ")

        sql = """
            SELECT * FROM space_objects
            WHERE object_type = %s
        """
        cursor.execute(sql, (object_type,))

    elif choice == "3":
        status = input("Enter status: ")

        sql = """
            SELECT * FROM space_objects
            WHERE status = %s
        """
        cursor.execute(sql, (status,))

    else:
        print("Invalid choice.")
        return

    data = cursor.fetchall()

    if not data:
        print("\nNo matching objects found.")
        return

    print("\nSearch Results:")
    print("-" * 80)

    for row in data:
        print(
            f"ID: {row[0]} | "
            f"Name: {row[1]} | "
            f"Type: {row[2]} | "
            f"Size: {row[3]} | "
            f"Distance: {row[4]} | "
            f"Shape: {row[5]} | "
            f"Status: {row[6]}"
        )

    print("-" * 80)
def UpdateObject():
    print("\n========== UPDATE SPACE OBJECT ==========")

    object_id = get_valid_id()

    cursor.execute(
        "SELECT * FROM space_objects WHERE object_id = %s",
        (object_id,)
    )

    object_data = cursor.fetchone()

    if object_data is None:
        print("\nObject not found.")
        return

    print("\nObject found:")
    print(f"Name: {object_data[1]}")
    print(f"Type: {object_data[2]}")
    print(f"Size: {object_data[3]}")
    print(f"Distance: {object_data[4]}")
    print(f"Shape: {object_data[5]}")
    print(f"Status: {object_data[6]}")

    print("\nWhat do you want to update?")
    print("1. Distance")
    print("2. Size")
    print("3. Shape")
    print("4. Status")

    choice = input("Enter your choice: ")

    if choice == "1":
        new_value = input("Enter new distance: ")
        column = "distance"

    elif choice == "2":
        new_value = input("Enter new size: ")
        column = "size"

    elif choice == "3":
        new_value = input("Enter new shape: ")
        column = "shape"

    elif choice == "4":
        new_value = input("Enter new status: ")
        column = "status"

    else:
        print("Invalid choice.")
        return

    sql = f"""
        UPDATE space_objects
        SET {column} = %s
        WHERE object_id = %s
    """

    cursor.execute(sql, (new_value, object_id))
    con.commit()

    print("\nObject updated successfully!")

def DeleteObject():
    print("\n========== DELETE SPACE OBJECT ==========")

    object_id = get_valid_id()

    cursor.execute(
        "SELECT * FROM space_objects WHERE object_id = %s",
        (object_id,)
    )

    object_data = cursor.fetchone()

    if object_data is None:
        print("\nObject not found.")
        return

    print("\nObject found:")
    print(f"ID: {object_data[0]}")
    print(f"Name: {object_data[1]}")
    print(f"Type: {object_data[2]}")

    confirm = input("\nAre you sure you want to delete it? (Y/N): ")

    if confirm.upper() == "Y":
        cursor.execute(
            "DELETE FROM space_objects WHERE object_id = %s",
            (object_id,)
        )

        con.commit()

        print("\nObject deleted successfully!")

    else:
        print("\nDeletion cancelled.")

def TrackObject():
    print("\n========== OBJECT TRACKING ==========")

    print("1. Show approaching objects")
    print("2. Show objects near Earth")
    print("3. Show all asteroids")
    print("4. Show all comets")

    choice = input("Enter your choice: ")

    if choice == "1":
        cursor.execute("""
            SELECT * FROM space_objects
            WHERE status = 'Approaching'
        """)

    elif choice == "2":
        cursor.execute("""
            SELECT * FROM space_objects
            WHERE distance LIKE '%km%'
        """)

    elif choice == "3":
        cursor.execute("""
            SELECT * FROM space_objects
            WHERE object_type = 'Asteroid'
        """)

    elif choice == "4":
        cursor.execute("""
            SELECT * FROM space_objects
            WHERE object_type = 'Comet'
        """)

    else:
        print("Invalid choice.")
        return

    data = cursor.fetchall()

    if not data:
        print("\nNo matching objects found.")
        return

    print("\nTracking Results")
    print("-" * 80)

    for row in data:
        print(
            f"ID: {row[0]} | "
            f"Name: {row[1]} | "
            f"Type: {row[2]} | "
            f"Size: {row[3]} | "
            f"Distance: {row[4]} | "
            f"Status: {row[6]}"
        )

    print("-" * 80)

def main():
    while True:
        print("\n")
        print("╔═════════════════════════════════════╗")
        print("║         SPACE OBJECT TRACKER        ║")
        print("╠═════════════════════════════════════╣")
        print("║  1. Add Space Object                ║")
        print("║  2. View Space Objects              ║")
        print("║  3. Search Space Object             ║")
        print("║  4. Update Space Object             ║")
        print("║  5. Delete Space Object             ║")
        print("║  6. Track Object                    ║")
        print("║  7. Exit                            ║")
        print("╚═════════════════════════════════════╝")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            AddObject()

        elif choice == "2":
            ViewObjects()

        elif choice == "3":
            SearchObject()

        elif choice == "4":
            UpdateObject()

        elif choice == "5":
            DeleteObject()

        elif choice == "6":
            TrackObject()

        elif choice == "7":
            print("\nThank you for using Space Object Tracker!")
            cursor.close()
            con.close()
            break

        else:
            print("\nInvalid choice. Please try again.")


main()