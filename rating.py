import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math
import matplotlib.pyplot as plt


#all the data
flight_prices_avg= []
flight_prices_max= []
flight_prices_min= []
flight_prices_emin= []
flight_prices_emax= []

hotel_prices_avg= []
hotel_prices_max= []
hotel_prices_min= []
hotel_prices_emin= []
hotel_prices_emax= []
hotel_prices_eavg= []

temperature_avg= []
temperature_max= []
temperature_min= []
temperature_emin= []
temperature_emax= []
temperature_eavg= []

precipitation_avg= []
precipitations_eavg= []

# Function to simplify math
def getAvg(numbers):
    if not numbers: 
        return 0
    return sum(numbers) / len(numbers)
def stda(numbers):
    mean = getAvg(numbers)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in numbers) / len(numbers))
    return mean + std_dev
def stdb(numbers):
    mean = getAvg(numbers)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in numbers) / len(numbers))
    return mean - std_dev

# Export membership function plots
def plot_and_save_membership_functions(variable, name):
    """
    Plots and saves the membership functions of a fuzzy variable.
    """
    plt.figure(figsize=(8, 5))
    for label in variable.terms:
        plt.plot(variable.universe, variable[label].mf, label=label)
    plt.title(f'Membership Functions for {name}')
    plt.xlabel(name)
    plt.ylabel('Membership Degree')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(f"{name}_membership_functions.png")
    plt.close()


def rate_trips(flight_prices, hotel_prices, temperatures, precipitations):
    
    assume_winter = False
    max_temp = max(temperature_max)
    print(f"Max Temp is {max_temp}")
    if(max(temperature_max) < 60):
        max_temp=80
        assume_winter = True
    elif(max(temperature_emax) > max_temp):
        max_temp = max(temperature_emax)
              
    # Define fuzzy variables
    flight_price = ctrl.Antecedent(np.arange(0, max(flight_prices_max)+1, 1), 'flight_price')
    hotel_price = ctrl.Antecedent(np.arange(0, max(hotel_prices_max)+1, 1), 'hotel_price')
    temperature = ctrl.Antecedent(np.arange(min(temperature_emin), max_temp+1, 1), 'temperature')
    precipitation = ctrl.Antecedent(np.arange(0, 5, 0.1), 'precipitation')
    rating = ctrl.Consequent(np.arange(0, 11, 1), 'rating')

    # Define membership functions
    flight_price['low'] = fuzz.trapmf(flight_price.universe, [0, 0,getAvg(flight_prices_min), stdb(flight_prices_avg)])
    flight_price['medium'] = fuzz.trimf(flight_price.universe, [max(flight_prices_emin), getAvg(flight_prices_avg), min(flight_prices_max)])
    flight_price['high'] = fuzz.trapmf(flight_price.universe, [stda(flight_prices_avg), getAvg(flight_prices_max), max(flight_prices_max), max(flight_prices_max)])

    hotel_price['low'] = fuzz.trapmf(hotel_price.universe, [0,0, getAvg(hotel_prices_emin), stdb(hotel_prices_avg)])
    hotel_price['medium'] = fuzz.trimf(hotel_price.universe, [max(hotel_prices_emin), getAvg(hotel_prices_avg), min(hotel_prices_max)])
    hotel_price['high'] = fuzz.trapmf(hotel_price.universe, [stda(hotel_prices_avg)-100,getAvg(hotel_prices_max),max(hotel_prices_max) , max(hotel_prices_max)])
    
    # If winter then warmer weather should be fine even if outside of stda
    if(assume_winter):
        temperature['cold'] = fuzz.trapmf(temperature.universe, [min(temperature_emin),min(temperature_emin), getAvg(temperature_emin), stdb(temperature_avg)])
        temperature['moderate'] = fuzz.trimf(temperature.universe, [max(temperature_min), getAvg(temperature_avg), 60])
        temperature['hot'] = fuzz.trapmf(temperature.universe, [65, 70, 80, 80])
    else:
        temperature['cold'] = fuzz.trapmf(temperature.universe, [min(temperature_emin),min(temperature_emin), getAvg(temperature_emin), stdb(temperature_avg)])
        temperature['moderate'] = fuzz.trimf(temperature.universe, [max(temperature_min), getAvg(temperature_avg), min(temperature_max)])
        temperature['hot'] = fuzz.trapmf(temperature.universe, [stda(temperature_avg), getAvg(temperature_max), max_temp, max_temp])

    precipitation['low'] = fuzz.trapmf(precipitation.universe, [0, 0, 0.1, 0.5])
    precipitation['medium'] = fuzz.trimf(precipitation.universe, [0.3, 1.0, 2.0])
    precipitation['high'] = fuzz.trapmf(precipitation.universe, [1.1, 3, 5,5])

    rating['poor'] = fuzz.trimf(rating.universe, [0, 0, 2]) 
    rating['bad'] = fuzz.trimf(rating.universe, [1, 2, 4]) 
    rating['average'] = fuzz.trimf(rating.universe, [3, 5, 7]) 
    rating['good'] = fuzz.trimf(rating.universe, [6, 8, 9]) 
    rating['excellent'] = fuzz.trimf(rating.universe, [8, 10, 10])
    
    # Plot and save membership functions
    plot_and_save_membership_functions(flight_price, 'Flight Price')
    plot_and_save_membership_functions(hotel_price, 'Hotel Price')
    plot_and_save_membership_functions(temperature, 'Temperature')
    plot_and_save_membership_functions(rating, 'Rating')
    plot_and_save_membership_functions(precipitation, 'Precipitation')

    # Define rules 
    rule1 = ctrl.Rule(flight_price['low'] & hotel_price['low'] & temperature['moderate'] & precipitation['low'], rating['excellent']) 
    rule2 = ctrl.Rule((flight_price['medium'] & hotel_price['low']) | (flight_price['low'] & hotel_price['medium']) & temperature['moderate'] & precipitation['medium'], rating['good']) 
    rule3 = ctrl.Rule(flight_price['medium'] & hotel_price['medium'] & temperature['moderate'] & precipitation['medium'], rating['average']) 
    rule4 = ctrl.Rule(flight_price['high'] | hotel_price['high'] | temperature['cold'] | temperature['hot'] | precipitation['high'], rating['poor']) 
    rule5 = ctrl.Rule(flight_price['high'] & hotel_price['high'] & (temperature['cold'] | temperature['hot']) & precipitation['high'], rating['bad'])    

    # Control system
    rating_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5])
    rating_sim = ctrl.ControlSystemSimulation(rating_ctrl)

    # Compute ratings for each trip
    trip_ratings = []
    for i in range(len(flight_prices)):
        rating_sim.input['flight_price'] = flight_prices[i]
        rating_sim.input['hotel_price'] = hotel_prices[i]
        rating_sim.input['temperature'] = temperatures[i]
        rating_sim.input['precipitation'] = precipitations[i]
        rating_sim.compute()
        trip_ratings.append(rating_sim.output['rating'])

    return trip_ratings

def getDates(trip_dates):
    departure_date = trip_dates['departure']
    return_date = trip_dates['return']
    departure_formatted = departure_date[5:10]
    return_formatted = return_date[5:10]
    year = departure_date[:4]
    return(f"{departure_formatted} to {return_formatted} {year}")

    
def get_rating(flight,hotel,weather):
    dates = []
    
    for item in flight:
        dates.append(getDates(item))
        flight_prices_min.append(item.get("min"))
        flight_prices_max.append(item.get("max"))
        flight_prices_avg.append(item.get("avg"))
        flight_prices_emin.append(item.get("emin"))
        flight_prices_emax.append(item.get("emax"))
    
    for item in hotel:
        hotel_prices_min.append(item.get("min"))
        hotel_prices_max.append(item.get("max"))
        hotel_prices_avg.append(item.get("avg"))
        hotel_prices_emin.append(item.get("emin"))
        hotel_prices_emax.append(item.get("emax"))
        hotel_prices_eavg.append(item.get("avg"))
    
    for item in weather:
        temperature_min.append(item[2])
        temperature_max.append(item[3])
        temperature_avg.append(item[4])
        precipitation_avg.append(item[5])
        temperature_emin.append(item[6])
        temperature_emax.append(item[7])
        temperature_eavg.append(item[8])
        precipitations_eavg.append(item[9])
    
    ratings = rate_trips(flight_prices_avg, hotel_prices_avg, temperature_avg, precipitation_avg)
    suggestion_index = np.argmax(ratings)
    suggestion = [flight_prices_avg[suggestion_index],hotel_prices_avg[suggestion_index],temperature_avg[suggestion_index]]
    suggestion.append(temperature_emin[suggestion_index])
    suggestion.append(temperature_emax[suggestion_index])
    suggestion.append(precipitation_avg[suggestion_index])
    
    return(ratings,dates,suggestion)
