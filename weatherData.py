from geopy.geocoders import Nominatim
from datetime import datetime
from meteostat import Hourly, Point
import matplotlib.pyplot as plt
import pandas as pd

def historicalHourlyTemp(date, stadiumName, day_night):
    if len(stadiumName) < 4: ## triggers if given abbreviation, turns it into a stadium name
        df = pd.read_csv("../minnemudac github/2023_MLBSchedule.csv")
        for index, row in df.iterrows():
            if row["home_team"] == stadiumName:
                stadiumName = row["stadium_name"]
                break
    # day is 2pm
    # night 7pm
    if (day_night == 1):
        timeOfDay = 2 # in military hrs?
    else:
        timeOfDay = 7
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(stadiumName)
    year = int(date[:3])
    month = date[4:6]
    if (month[0] == '0'):
        month = month.replace("0", "")
    month = int(month)
    day = date[6:8]
    if (day[0] == '0'):
        day = day.replace("0", "")
    day = int(day)
    location = Point(location.latitude, location.longitude, 70) # 3rd param is altitude
    start = datetime(1967, month, day,hour = timeOfDay) # year month day hour = x
    end = datetime(1967, month, day, hour=timeOfDay)  # year month day hour = x
    # end = datetime(2022, month, day, hour = timeOfDay + 1)
    # Get hourly data
    data = Hourly(location, start, end)
    data = data.fetch()
    # data.plot(y=['tavg', 'tmin', 'tmax'])
    # plt.show()
    print(data.temp)
    return data




historicalHourlyTemp("20230330","NYA",1)



