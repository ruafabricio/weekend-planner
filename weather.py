import requests
from datetime import datetime, timedelta
from datetime import date
import calendar  # Import the calendar module to use monthrange

# Replace with your WeatherAPI key
API_KEY = "648516589b874889853193315241012"
BASE_URL = "http://api.weatherapi.com/v1/history.json"
FUTURE_URL = "http://api.weatherapi.com/v1/future.json"

def process_data(data):
    mint = []
    maxt = []
    avgt = []
    avgp =[]
    weather = []
    weather.append(data[0].get('date'))
    weather.append(data[2].get('date'))
    for item in data:
        avgp.append(item["total_precip"])
        mint.append(item["min_temp"])
        maxt.append(item["max_temp"])
        avgt.append(item["avg_temp"])
        
    amint = sum(mint) / len(mint)
    amaxt = sum(maxt) / len(maxt)
    aavgt = sum(avgt) / len(avgt)
    aavgp = sum(avgp) / len(avgp)
    
    weather.append(amint)
    weather.append(amaxt)
    weather.append(aavgt)
    weather.append(aavgp)
    
    return weather

def process_historical_data(data, num):
    final = []
    for i in range(num):
        mint = []
        maxt = []
        avgt = []
        avgp =[]
        weather = []
        for j in range(len(data)):
            mint.append(data[j][i][2])
            maxt.append(data[j][i][3])
            avgt.append(data[j][i][4])
            avgp.append(data[j][i][5])
        
        amint = sum(mint) / len(mint)
        amaxt = sum(maxt) / len(maxt)
        aavgt = sum(avgt) / len(avgt)
        aavgp = sum(avgp) / len(avgp)
    
        weather.append(amint)
        weather.append(amaxt)
        weather.append(aavgt)
        weather.append(aavgp)
        final.append(weather)
    
    return final


def get_historical_weather(zip_code, start_date, end_date):
    """
    Fetch historical weather data (average, min, max precipitation, and temperature) for a given zip code and date range.
    """
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    #current_date = start_date
    weather_data = []
    today = date.today()
    formatted_today = today.strftime("%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        params = {
            "key": API_KEY,
            "q": zip_code,
            "dt": date_str,
            "days": 1,
            
        }
        
        if(start_date > formatted_today ):
            response = requests.get(FUTURE_URL, params=params)
        else:
            response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            day_data = data.get("forecast", {}).get("forecastday", [])[0].get("day", {})

            weather_data.append({
                "date": date_str,
                "avg_temp": day_data.get("avgtemp_f"),
                "min_temp": day_data.get("mintemp_f"),
                "max_temp": day_data.get("maxtemp_f"),
                "total_precip": day_data.get("totalprecip_in")
            })
        else:
            print(f"Failed to fetch data for {date_str}: {response.status_code} {response.text}")

        current_date += timedelta(days=1)
    processed = process_data(weather_data)
    return processed

def get_friday_sunday_dates(month, year):
        # Start date for the given month
        first_day_of_month = datetime(year, month, 1)
        # Get the first Friday of the month
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

def get_weather_for_weekends(zip_code, month, year):
    """
    Get the weather for each weekend (Friday to Sunday) in the specified month and year.
    """
    weekends = get_friday_sunday_dates(month, year)
    final = []

    for friday, sunday in weekends:
        start_date = friday.strftime("%Y-%m-%d")
        end_date = sunday.strftime("%Y-%m-%d")
        weather_results = get_historical_weather(zip_code, start_date, end_date)
        print("<Response [200]>")
        final.append(weather_results)
    return(final)



def get_weather_report(zip_code, month, year):
    future = get_weather_for_weekends(zip_code, month, year)
    lastFive = []
    for i in range(1,6):
        new_year = year - i
        results = get_weather_for_weekends(zip_code, month, new_year)
        lastFive.append(results)
    averages = process_historical_data(lastFive, len(future))
    for i in range(len(future)):
        future[i].append(averages[i][0])
        future[i].append(averages[i][1]) 
        future[i].append(averages[i][2]) 
        future[i].append(averages[i][3]) 
    return future
    #[[start, end, min, max, average t, average p, e min, e max, e avg t, e avg p],...,[]]