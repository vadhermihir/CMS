import mysql.connector
from datetime import datetime, timedelta, date

# Set today's database name
today = date.today()
db_name = f"bus_booking_{today.year}_{today.month:02d}_{today.day:02d}"

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

# Check connection
if conn.is_connected():
    print("✅ Connected to MySQL Server")

cursor = conn.cursor()

# Create database and tables
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_name VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(100),
    total_seats INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT,
    passenger_name VARCHAR(100),
    seats_booked INT,
    booking_date DATETIME,
    FOREIGN KEY (bus_id) REFERENCES Buses(bus_id)
)
""")

# ---------- FUNCTIONS ----------

def insert_bus():
    name = input("Enter bus name: ")
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    seats = int(input("Enter total seats: "))
    cursor.execute("INSERT INTO Buses (bus_name, source, destination, total_seats) VALUES (%s, %s, %s, %s)",
                   (name, source, destination, seats))
    conn.commit()
    print("✅ Bus inserted.\n")

def book_ticket():
    display_buses()
    bus_id = int(input("Enter bus ID: "))
    name = input("Enter passenger name: ")
    seats = int(input("Enter seats to book: "))
    booking_date = datetime.now()
    cursor.execute("INSERT INTO Bookings (bus_id, passenger_name, seats_booked, booking_date) VALUES (%s, %s, %s, %s)",
                   (bus_id, name, seats, booking_date))
    conn.commit()
    print("✅ Ticket booked.\n")

def cancel_ticket():
    booking_id = int(input("Enter booking ID to cancel: "))
    cursor.execute("SELECT booking_date FROM Bookings WHERE booking_id = %s", (booking_id,))
    result = cursor.fetchone()
    if result:
        booking_time = result[0]
        time_diff = datetime.now() - booking_time
        if time_diff <= timedelta(hours=24):
            print("🕒 Cancelled within 24 hours — 50% refund applicable.")
        else:
            print("❌ Cancelled after 24 hours — No refund.")
        cursor.execute("DELETE FROM Bookings WHERE booking_id = %s", (booking_id,))
        conn.commit()
        print("✅ Ticket cancelled.\n")
    else:
        print("⚠️ Booking not found.\n")

def update_booking():
    booking_id = int(input("Enter booking ID to update: "))
    new_name = input("Enter new passenger name: ")
    cursor.execute("UPDATE Bookings SET passenger_name = %s WHERE booking_id = %s",
                   (new_name, booking_id))
    conn.commit()
    print("✅ Booking updated.\n")

def display_bookings():
    cursor.execute("""
    SELECT b.booking_id, bu.bus_name, b.passenger_name, b.seats_booked, b.booking_date
    FROM Bookings b
    JOIN Buses bu ON b.bus_id = bu.bus_id
    """)
    results = cursor.fetchall()
    print("\n📄 All Bookings:")
    for row in results:
        print(f"ID: {row[0]} | Bus: {row[1]} | Passenger: {row[2]} | Seats: {row[3]} | Date: {row[4]}")
    print()

def display_buses():
    cursor.execute("SELECT * FROM Buses")
    buses = cursor.fetchall()
    print("\n🚌 Available Buses:")
    for b in buses:
        print(f"Bus ID: {b[0]} | Name: {b[1]} | Route: {b[2]} ➝ {b[3]} | Seats: {b[4]}")
    print()

# ---------- MAIN MENU ----------
def main():
    while True:
        print("\n===== BUS BOOKING SYSTEM =====")
        print("1. Insert Bus")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. Update Passenger Name")
        print("5. Show All Bookings")
        print("6. Show Buses")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            insert_bus()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            cancel_ticket()
        elif choice == '4':
            update_booking()
        elif choice == '5':
            display_bookings()
        elif choice == '6':
            display_buses()
        elif choice == '0':
            print("👋 Exiting...")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

# Run the main menu
main()

# Close DB
cursor.close()
conn.close()