import numpy as np

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

def getAvg(numbers):
    if not numbers:  
        return 0
    return sum(numbers) / len(numbers)

def calculate_prior_probabilities():
    # Define prior probabilities for each criterion being favorable (good rating)
    # These probabilities should sum to 1
    prior_prob_flight = 0.25
    prior_prob_hotel = 0.25
    prior_prob_temp = 0.25
    prior_prob_precip = 0.25
    
    return prior_prob_flight, prior_prob_hotel, prior_prob_temp, prior_prob_precip

def calculate_likelihoods(flight_prices, hotel_prices, temperatures, precipitations):
    # Convert lists to numpy arrays
    flight_prices = np.array(flight_prices)
    hotel_prices = np.array(hotel_prices)
    temperatures = np.array(temperatures)
    precipitations = np.array(precipitations)

    # Define likelihoods based on the preferences
    likelihoods_flight = 1 / (1 + np.exp((flight_prices - getAvg(flight_prices_avg)) / 100))  # Sigmoid function, prefer lower flight prices
    likelihoods_hotel = 1 / (1 + np.exp((hotel_prices - getAvg(hotel_prices_eavg)) / 100))   # Sigmoid function, prefer lower hotel prices
    likelihoods_temp = 1 / (1 + np.exp((np.abs(temperatures - getAvg(temperature_eavg)) / 5)))  # Sigmoid, prefer moderate temperature (~22°C)
    likelihoods_precip = 1 / (1 + np.exp((precipitations -getAvg(precipitations_eavg)) / 0.1))  # Sigmoid, prefer lower precipitation
    
    return likelihoods_flight, likelihoods_hotel, likelihoods_temp, likelihoods_precip

def calculate_posteriors(prior_prob, likelihoods):
    # Posterior probability for each trip
    posteriors = prior_prob * likelihoods
    return posteriors / np.sum(posteriors, axis=0)  # Normalize to get a probability

def bayesian_rating(flight_prices, hotel_prices, temperatures, precipitations):
    # Calculate prior probabilities
    prior_prob_flight, prior_prob_hotel, prior_prob_temp, prior_prob_precip = calculate_prior_probabilities()
    
    # Calculate likelihoods
    likelihoods_flight, likelihoods_hotel, likelihoods_temp, likelihoods_precip = calculate_likelihoods(flight_prices, hotel_prices, temperatures, precipitations)
    
    # Calculate posteriors
    posteriors_flight = calculate_posteriors(prior_prob_flight, likelihoods_flight)
    posteriors_hotel = calculate_posteriors(prior_prob_hotel, likelihoods_hotel)
    posteriors_temp = calculate_posteriors(prior_prob_temp, likelihoods_temp)
    posteriors_precip = calculate_posteriors(prior_prob_precip, likelihoods_precip)
    
    # Combine all posteriors (average the probabilities)
    combined_posteriors = (posteriors_flight + posteriors_hotel + posteriors_temp + posteriors_precip) / 4
    
    # Scale to rating out of 10
    ratings = combined_posteriors * 10
    return ratings.tolist()

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
        
    ratings = bayesian_rating(flight_prices_avg, hotel_prices_avg, temperature_avg, precipitation_avg)
    suggestion_index = np.argmax(ratings)
    suggestion = [flight_prices_avg[suggestion_index],hotel_prices_avg[suggestion_index],temperature_avg[suggestion_index]]
    suggestion.append(temperature_emin[suggestion_index])
    suggestion.append(temperature_emax[suggestion_index])
    suggestion.append(precipitation_avg[suggestion_index])
    print(ratings,dates, suggestion)
    return(ratings,dates, suggestion)
