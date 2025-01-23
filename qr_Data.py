import sqlite3

# Function to insert QR code into the database
def insert_qr_code(qr_data):
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()

    # Insert the QR code data
    cursor.execute('''
    INSERT INTO scanned_qr_codes (qr_data) 
    VALUES (?)
    ''', (qr_data,))

    conn.commit()
    conn.close()

# Function to update a QR code in the database
def update_qr_code(old_qr_data, new_qr_data):
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()

    # Update the QR code data
    cursor.execute('''
    UPDATE scanned_qr_codes
    SET qr_data = ?
    WHERE qr_data = ?
    ''', (new_qr_data, old_qr_data))

    conn.commit()
    conn.close()

# Function to delete a QR code from the database
def delete_qr_code(qr_data):
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()

    # Delete the QR code data
    cursor.execute('''
    DELETE FROM scanned_qr_codes WHERE qr_data = ?
    ''', (qr_data,))

    conn.commit()
    conn.close()

# Function to fetch all QR codes from the database
def fetch_all_qr_codes():
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()

    # Select all QR codes
    cursor.execute('''
    SELECT * FROM scanned_qr_codes
    ''')

    qr_codes = cursor.fetchall()
    conn.close()

    return qr_codes

# Function to manage QR codes (Add, Update, Delete, View)
def manage_qr_codes():
    while True:
        print("\nQR Code Management")
        print("1. Add a new QR code")
        print("2. Update a QR code")
        print("3. Delete a QR code")
        print("4. View all QR codes")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            qr_data = input("Enter the new QR code data: ")
            insert_qr_code(qr_data)
            print(f"QR code '{qr_data}' added successfully.")
        elif choice == '2':
            old_qr_data = input("Enter the old QR code data: ")
            new_qr_data = input("Enter the new QR code data: ")
            update_qr_code(old_qr_data, new_qr_data)
            print(f"QR code '{old_qr_data}' updated to '{new_qr_data}'.")
        elif choice == '3':
            qr_data = input("Enter the QR code data to delete: ")
            delete_qr_code(qr_data)
            print(f"QR code '{qr_data}' deleted successfully.")
        elif choice == '4':
            qr_codes = fetch_all_qr_codes()
            if qr_codes:
                print("\nValid QR codes:")
                for qr_code in qr_codes:
                    print(f"ID: {qr_code[0]}, QR Code: {qr_code[1]}")
            else:
                print("No QR codes found.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Call this function to manage QR codes
manage_qr_codes()
