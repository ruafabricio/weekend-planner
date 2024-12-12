# weekend-planner
A fuzzy logic system to determine the best weekend to travel in the US

Powered by SerpAPI and WeatherAPI, keys may need to be updated. If response is 504 then API key needs to be refreshed

ui.py - creates a ui with dropdown bars to send inputs to controlles and display results
controller.py - take inputs calls gotels,flights,weather to get data then calls rating, bayesian to get ratings then formats and returns
flights.py- uses SerpAPI and API key to query flight price data for given parameters
hotels.py- uses SerpAPI and API key to query hotel price data for given parameters
weather.py- uses WeatherAPI and API key to query weather data for given parameters
rating.py - fuzzy logic system that creates membership functions with parameters based on data, plots functions and returns raitings and information for suggested date
beysian.py - uses bayesian logic to get ratings based on data

