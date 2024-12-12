import requests
import json
from datetime import datetime, timedelta

# API key
API_KEY = '47bbb0aae3f88f1348fff5b4410a477387fb24f9d4b04a8fb2080e3fd93f99bc'


def process_data(data):
    prices = []
    for item in data["best_flights"]:
        prices.append(item["price"])
    for item in data["other_flights"]:
        prices.append(item["price"])
    average = sum(prices) / len(prices)
    minn = min(prices)
    maxx = max(prices)
    minmax = data["price_insights"]["typical_price_range"]
    emin = minmax[0]
    emax = minmax[1]
    return[minn,emin,maxx,emax,average]
    
        

def get_flight_prices(origin, destination, month, year):
    results = []
    # Helper function to get Friday to Sunday dates for a given month
    def get_friday_sunday_dates(month, year):
        # Start date for the given month
        first_day_of_month = datetime(year, month, 1)
        friday_dates = []
        
        # Find the first Friday in the month
        days_ahead = 4 - first_day_of_month.weekday() 
        if days_ahead <= 0:
            days_ahead += 7
        
        first_friday = first_day_of_month + timedelta(days=days_ahead)
        # Collect Friday-Sunday dates
        current_friday = first_friday
        while current_friday.month == month:
            friday_dates.append((current_friday, current_friday + timedelta(days=2))) 
            current_friday += timedelta(weeks=1)
        
        return friday_dates

    # Helper function to query SerpApi for flight prices
    def get_flight_data(departure_date, return_date, destination, origin):
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date" : departure_date,
            "return_date" : return_date,
            "currency": "USD",
            "hl": "en",
            "api_key": API_KEY,
        }
        response = requests.get(url, params=params)
        print(response)
        return response.json() if response.status_code == 200 else None

    friday_sunday_dates = get_friday_sunday_dates(month, year)
    flight_prices = []

    for friday, sunday in friday_sunday_dates:
        departure_date = friday.strftime("%Y-%m-%d")
        return_date = sunday.strftime("%Y-%m-%d")
        flight_data = get_flight_data(departure_date, return_date, destination, origin)
        processed = process_data(flight_data)
        
        if processed:
            # Extract the flight price from the response (assuming the API returns flight data)
            flight_prices.append({
                "departure": departure_date,
                "return": return_date,
                "min": processed[0],
                "emin": processed[1],
                "max": processed[2],
                "emax": processed[3],
                "avg": processed[4]
            })

    return(flight_prices)