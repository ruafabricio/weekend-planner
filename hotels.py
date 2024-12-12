import requests
import json
import calendar
from datetime import datetime, timedelta
from serpapi import GoogleSearch  

# API key
API_KEY = '47bbb0aae3f88f1348fff5b4410a477387fb24f9d4b04a8fb2080e3fd93f99bc'
#function to process the data
def process_data(data):
    prices = []
    top_picks = []
    for item in data["properties"]:
        if item.get("total_rate") is not None:
            if item["total_rate"]["extracted_lowest"] is not None:
                prices.append(item["total_rate"]["extracted_lowest"])
                if item.get("overall_rating") is not None:
                    if(item.get("overall_rating") >= 3.5):
                        top_picks.append(item["total_rate"]["extracted_lowest"])
             
    eavg= sum(prices) / len(prices)
    emin = min(prices)
    emax = max(prices)
    
    avg = sum(top_picks) / len(top_picks)
    minn = min(top_picks)
    maxx = max(top_picks)
    return[emin,emax,eavg,minn,maxx,avg]

# Function to get weekends for a specific month
def get_friday_sunday_dates(year, month):
        # Start date for the given month
        first_day_of_month = datetime(year, month, 1)
        friday_dates = []
        
        # Find the first Friday in the month
        days_ahead = 4 - first_day_of_month.weekday()  # 4 is Friday
        if days_ahead <= 0:
            days_ahead += 7
        
        first_friday = first_day_of_month + timedelta(days=days_ahead)
        # Collect Friday-Sunday dates
        current_friday = first_friday
        while current_friday.month == month:
            friday_dates.append((current_friday, current_friday + timedelta(days=2)))  # Friday to Sunday
            current_friday += timedelta(weeks=1)
        
        return friday_dates

# Function to fetch hotel prices using SerpAPI
def get_hotel_prices(city, checkin_date, checkout_date):
    params = {
        "engine": "google_hotels",
        "q": f"hotels in {city}",
        "check_in_date": checkin_date.strftime("%Y-%m-%d"),
        "check_out_date": checkout_date.strftime("%Y-%m-%d"),
        "adults": "2",
        "currency": "USD",
        "gl": "us",
        "hl": "en",
        "api_key": API_KEY
        }
    hotel_prices = []
    search = GoogleSearch(params)
    results = search.get_dict()
    print("<Response[200]>")
    processed = process_data(results)
    return processed

# Main function to get weekend hotel prices
def get_weekend_hotel_prices(month, city, year):
    weekends = get_friday_sunday_dates(year, month)
    final = []
    for friday, sunday in weekends:
        hotel_prices = get_hotel_prices(city, friday, sunday)
        if hotel_prices:
            final.append({
                "in": friday.strftime("%Y-%m-%d"),
                "out": sunday.strftime("%Y-%m-%d"),
                "emin": hotel_prices[0],
                "emax": hotel_prices[1],
                "eavg": hotel_prices[2],
                "min": hotel_prices[3],
                "max": hotel_prices[4],
                "avg": hotel_prices[5],
            })
        else:
            print("No hotel prices found.")
    return(final)