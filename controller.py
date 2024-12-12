import weather
import hotels
import flights
import rating
import numpy as np
import bayesian
import os
import time

def print_and_log(string1, string2):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_filename = "logs/logs.txt"

    if os.path.isfile(log_filename):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_filename = f"logs/logs_{timestamp}.txt"

    # Print the strings to the terminal
    print(string1)
    print(string2)

    # Write the strings to the log file
    with open(log_filename, 'w') as logfile:
        logfile.write(string1 + "\n")
        logfile.write(string2 + "\n")

def bayesian_format(ratings, dates, suggestion):
    # Rank the ratings
    sorted_indices = np.argsort(ratings)[::-1]
    ranks = np.zeros_like(sorted_indices)
    ranks[sorted_indices] = np.arange(1, len(ratings) + 1)

    # Format the trip information
    trips_info = []
    for i in range(len(ratings)):
        trips_info.append(f"Trip {i + 1} Rating: {ratings[i]:.2f}, Date: {dates[i]}, Rank: {ranks[i]}")
    
    top_trip = sorted_indices[0] + 1
    precip_state = "no"    
    if(int(suggestion[5]) >= 2.0 ):
        precip_state = "high"
    elif(suggestion[5] >= 1.0):
        precip_state = "some"
    elif(suggestion[5] >= 0.5):
        precip_state = "low"
    total = suggestion[0] + suggestion[1]
    suggestion_string = f"          We suggest Trip {top_trip} \n       Expected Cost: ${total:.2f} \n       Average Flight Price: ${suggestion[0]:.2f} \n       Average Hotel Price: ${suggestion[1]:.2f} \n       Average Temperature(F): {suggestion[2]:.2f} \u00B0F \n       With a low of {int(suggestion[3])}\u00B0F and high of {int(suggestion[4])}\u00B0F \n       There is {precip_state} precipitation expected \n"

    formatted_string = "\n".join(trips_info) + "\n\n" + suggestion_string
    return formatted_string


def controller(origin, destination, origin_code, destination_code, month, year):
    
    MONTH_TO_NUMBER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
    
    }   
    monthNum = MONTH_TO_NUMBER[month]
    
    # Query the APIs
    flight_data = flights.get_flight_prices(origin_code, destination_code, monthNum, int(year))
    print(".... Flight Data Gathered")
    weather_data = weather.get_weather_report(destination,monthNum, int(year))
    print(".... Weather Data Gathered")
    hotels_data = hotels.get_weekend_hotel_prices(monthNum, destination, int(year))
    print(".... Hotel Data Gathered")
    print("===DATA GATHERED ==")
    
    # Run the ratings
    rated_dates, dates, suggestion_info = rating.get_rating(flight_data,hotels_data,weather_data)
    
    # Format export of values for UI
    sorted_indices = np.argsort(rated_dates)[::-1] 
    ranks = np.zeros_like(sorted_indices) 
    ranks[sorted_indices] = np.arange(1, len(rated_dates) + 1)
    trips = []
    top_trip = sorted_indices[0] + 1
    precip_state = "no"
    
    if(int(suggestion_info[5]) >= 2.0 ):
        precip_state = "high"
    elif(suggestion_info[5] >= 1.0):
        precip_state = "low"
    
    for i in range(len(rated_dates)): 
        trips.append(f"Trip {i + 1} Rating: {rated_dates[i]:.2f}, Date: {dates[i]}, Rank: {ranks[i]}")
    suggestion = f"We suggest Trip {top_trip} \n \n Average Flight Price: ${suggestion_info[0]:.2f} \n Average Hotel Price: ${suggestion_info[1]:.2f} \n Average Temperatue(F): {suggestion_info[2]:.2f} \u00B0F \n With a low of {int(suggestion_info[3])}\u00B0F and high of {int(suggestion_info[4])}\u00B0F \n There is {precip_state} precipitation expected"
    
    bratings, bdates, bsuggestion = bayesian.get_rating(flight_data, hotels_data, weather_data)
    
    formated_fuzzy = (bayesian_format(rated_dates, dates, suggestion_info))
    fomrated_bayesian = bayesian_format(bratings,bdates,bsuggestion)
    print_and_log(formated_fuzzy, fomrated_bayesian)
    return("\n".join(trips) + "\n\n" + suggestion)