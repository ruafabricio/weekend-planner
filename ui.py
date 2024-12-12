import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import controller

# Map of cities with major airports and their airport codes
CITY_AIRPORT_MAP = {
    "Akron": "CAK",
    "Albany": "ALB",
    "Albuquerque": "ABQ",
    "Anchorage": "ANC",
    "Asheville": "AVL",
    "Atlanta": "ATL",
    "Austin": "AUS",
    "Baltimore": "BWI",
    "Billings": "BIL",
    "Birmingham": "BHM",
    "Boise": "BOI",
    "Boston": "BOS",
    "Bozeman": "BZN",
    "Buffalo": "BUF",
    "Burlington": "BTV",
    "Charleston": "CHS",
    "Charlotte": "CLT",
    "Chattanooga": "CHA",
    "Chicago": "ORD",
    "Cleveland": "CLE",
    "Colorado Springs": "COS",
    "Columbus": "CMH",
    "Dallas": "DFW",
    "Dayton": "DAY",
    "Denver": "DEN",
    "Des Moines": "DSM",
    "Detroit": "DTW",
    "El Paso": "ELP",
    "Fort Lauderdale": "FLL",
    "Fresno": "FAT",
    "Grand Rapids": "GRR",
    "Greenville": "GSP",
    "Harrisburg": "MDT",
    "Hartford": "BDL",
    "Hilton Head": "HHH",
    "Honolulu": "HNL",
    "Houston": "IAH",
    "Indianapolis": "IND",
    "Jacksonville": "JAX",
    "Kansas City": "MCI",
    "Key West": "EYW",
    "Knoxville": "TYS",
    "Las Vegas": "LAS",
    "Little Rock": "LIT",
    "Los Angeles": "LAX",
    "Louisville": "SDF",
    "Lubbock": "LBB",
    "Madison": "MSN",
    "Memphis": "MEM",
    "Miami": "MIA",
    "Milwaukee": "MKE",
    "Minneapolis": "MSP",
    "Myrtle Beach": "MYR",
    "Nashville": "BNA",
    "New Orleans": "MSY",
    "New York": "JFK",
    "Oklahoma City": "OKC",
    "Omaha": "OMA",
    "Orlando": "MCO",
    "Palm Springs": "PSP",
    "Pensacola": "PNS",
    "Philadelphia": "PHL",
    "Phoenix": "PHX",
    "Pittsburgh": "PIT",
    "Portland": "PDX",
    "Providence": "PVD",
    "Raleigh/Durham": "RDU",
    "Reno": "RNO",
    "Richmond": "RIC",
    "Sacramento": "SMF",
    "Salt Lake City": "SLC",
    "San Antonio": "SAT",
    "San Diego": "SAN",
    "San Francisco": "SFO",
    "San Jose": "SJC",
    "Santa Ana (Orange County)": "SNA",
    "Savannah": "SAV",
    "Seattle": "SEA",
    "Spokane": "GEG",
    "St. Louis": "STL",
    "Syracuse": "SYR",
    "Tampa": "TPA",
    "Tulsa": "TUL",
    "Washington, D.C.": "DCA",
    "Wichita": "ICT"
}

def submit_data():
    """Handles the submission of user inputs."""
    origin = origin_combobox.get()
    destination = destination_combobox.get()
    month_year = month_combobox.get()

    if not origin or not destination:
        messagebox.showerror("Input Error", "Please select both origin and destination.")
        return

    if not month_year:
        messagebox.showerror("Input Error", "Please select a future month.")
        return

    try:
        # Translate city names to airport codes
        origin_code = CITY_AIRPORT_MAP[origin]
        destination_code = CITY_AIRPORT_MAP[destination]

        month, year = month_year.split()

        # Call the controller function
        print(f"Looking for Weekend Trips to {destination} for {month} in {year}")
        result = controller.controller(origin, destination, origin_code, destination_code, month, year)
        result_label.config(text=f"Results: \n {str(result)}")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main application window
root = tk.Tk()
root.title("City Travel Planner")

# Dropdown for origin city
origin_label = tk.Label(root, text="City of Origin:")
origin_label.grid(row=0, column=0, padx=10, pady=10)
origin_combobox = ttk.Combobox(root, values=list(CITY_AIRPORT_MAP.keys()), state="readonly")
origin_combobox.grid(row=0, column=1, padx=10, pady=10)

# Dropdown for destination city
destination_label = tk.Label(root, text="Destination City:")
destination_label.grid(row=1, column=0, padx=10, pady=10)
destination_combobox = ttk.Combobox(root, values=list(CITY_AIRPORT_MAP.keys()), state="readonly")
destination_combobox.grid(row=1, column=1, padx=10, pady=10)

# Dropdown for future months
month_label = tk.Label(root, text="Select Future Month:")
month_label.grid(row=2, column=0, padx=10, pady=10)

# Generate a list of months up to 300 days from today
current_date = datetime.now()
future_dates = [current_date + timedelta(days=i) for i in range(0, 301, 30)]
month_options = [date.strftime("%B %Y") for date in future_dates]

month_combobox = ttk.Combobox(root, values=month_options, state="readonly")
month_combobox.grid(row=2, column=1, padx=10, pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=3, column=0, columnspan=2, pady=20)

# Label to display results
result_label = tk.Label(root, text="Result: ", wraplength=400)
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
