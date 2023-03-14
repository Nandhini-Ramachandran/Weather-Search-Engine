''' 1. Seach engine that takes a city name as input from the user and displays 
the weather in that city.
2. API used = "https://openweathermap.org/current"
'''

# Importing required modules
import requests 
import json
from tabulate import tabulate
import re


#key generated from user account
from config import api_key


#function to display the weather data in a tabular form
def display_weather(weather_data):

    #extracting the weather parametes of interest from the json file
    output = [["Weather ", weather_data["weather"][0]["description"],"-"],
             ["Temperature ", weather_data["main"]["temp"], "\u00b0C"],
             ["Feels like ", weather_data["main"]["feels_like"], "\u00b0C"],
             ["Wind speed ",weather_data["wind"]["speed"], " km/hr"],
             ["Pressure ", weather_data["main"]["pressure"], "hPa"],
             ["Humidity ",weather_data["main"]["humidity"], " %"],
            ]

    # Displaying weather parameters of the city
           
    print (tabulate(output,
                    headers=["Parameter", "Value", "Unit"],
                    tablefmt="fancy_grid", showindex= False
                    ))
    
   
#function to fetch & return the weather data of the passed city from the server
def get_weather(city_name):

    base_url_coordinates = "http://api.openweathermap.org/geo/1.0/direct?"

    url_coordinates = (base_url_coordinates 
                       + "q=" 
                       + city_name 
                       + "&limit=5&appid=" 
                       + api_key
                       + "&units=metric"     
                       )
    
    # HTTP request to fetch the coordinates data on the city in json format
    geographical_data = requests.get(url_coordinates).json()

    #extracting the coordinates
    latitude = geographical_data[0]["lat"]
    longitude = geographical_data[0]["lon"]

    
    base_url_weather = "https://api.openweathermap.org/data/2.5/weather?"

    url_weather = (base_url_weather
                   + "lat="
                   + str(latitude)
                   + "&lon="
                   + str(longitude)
                   + "&appid="
                   + api_key
                   + "&units=metric"
                   )
                   

    # HTTP request to fetch weather data at coordinates of city in json format
    weather_data = requests.get(url_weather).json()
    
    try:           
        #function call to display the weather information to user
        display_weather(weather_data)
        return weather_data
        
    except TypeError:
        print ("Invalid entry. Kindly enter a valid city name.\n")
        return
        

# getting user input and handling exceptions
if __name__ == "__main__":

    response = 'y'
    while response == 'y':
        #creating a cache file 
        filename = "cache.json"

        #checking for existing cache else creating one 
        try:
            with open(filename,"r") as json_cache:
                cache = json.load(json_cache)
        except FileNotFoundError:
            cache = {}

        # loop to fetch user input  
        # and display the weather data 
        # or appropiate error message
        while True:

            # getting city name from the user
            city_name = input("\nEnter the name of the city: ")
            print('\n')
            
            lower_city_name = city_name.lower()
            # checking for city's weather data in cache
            if lower_city_name in cache:
                weather_data = cache[lower_city_name]
                display_weather(weather_data)
                break

            else:
                # validating user input using regular expression 
                city_regex = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ][\wÀ-ÖØ-öø-ÿ.\',\s-]*[^\W\d_]$')
                if city_regex.match(city_name):
                    
                    # fetching and displaying weather data from server
                    try:
                        weather_data = get_weather(lower_city_name)
                        cache[lower_city_name] = weather_data
                        break 
                        
                    except IndexError:
                        print("Invalid entry. Kindly enter a valid city name.\n")
                        break
                    except KeyError:
                        print("Invalid API\n")
                        break

                else:
                    print("Invalid entry. Kindly enter a valid city name.\n")

        # updating cache file with new city data 
        with open(filename, 'w') as json_cache:
            json.dump(cache,json_cache,indent=4)
        
        
        response = input("\nWould you like to enter more cities (y/n)?: ")
        if response not in ['y','n']:
            print("Invalid Input.\n")
            break
