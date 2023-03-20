from geopy.geocoders import Nominatim
from datetime import datetime
from meteostat import Hourly, Point
import matplotlib.pyplot as plt
import pandas as pd
import time
from tqdm import tqdm

# geolocator = Nominatim(user_agent="MyApp",timeout=10)
# location = geolocator.geocode("Lakewood")
# print(location)
# location = Point(location.latitude, location.longitude, 70) # 3rd param is altitude
# start = datetime(2006, 10, 4, hour=2)  # year month day hour = x
# end = datetime(2006, 10, 4, hour=2)  # year month day hour = x
# data = Hourly(location, start, end)
# #
# data = data.fetch()
# print(data)

def historicalHourlyTemp(date: str, stadiumName: str, day_night: str):
    start_time = time.time()
    locations = {}
    if stadiumName == "COL":
        return 0
    if len(stadiumName) < 4: ## triggers if given abbreviation, turns it into a stadium name
        if stadiumName == "MON":
            stadiumName = "Montreal"
        else:
            df = pd.read_csv("../minnemudac github/2023_MLBSchedule.csv")
            for index, row in df.iterrows():
                if row["home_team"] == stadiumName:
                    stadiumName = row["stadium_name"]
                    break
    # day is 2pm
    # night 7pm
    if (day_night == "D"):
        timeOfDay = 2
    elif(day_night == "N"):
        timeOfDay = 7

    # manual locations (not found in geolocator)
    if stadiumName == "Oriole Park at Camden Yards":
        stadiumName = "Baltimore"
    if stadiumName == "TMobile Park":
        stadiumName = "Seattle"
    if stadiumName == "Busch Stadium":
        stadiumName = "St. Louis"
    if stadiumName == "loanDepot park":
        stadiumName = "Miami"
    if stadiumName == "Angel Stadium":
        stadiumName = "Anaheim"
    if stadiumName == "Coors Field":
        stadiumName = "Denver"
    if stadiumName not in locations.keys():
        geolocator = Nominatim(user_agent="MyApp",timeout=10)
        location = geolocator.geocode(stadiumName)
        locations[stadiumName] = location
    else:
        location = locations[stadiumName]
    # if location is None:
    #     print(stadiumName + "geolocation not found")
    #     return 0
    month = date[4:6]
    if (month[0] == '0'): ## fixes date formatting
        month = month.replace("0", "")
    month = int(month)
    day = date[6:8]
    if (day[0] == '0'): ## fixes date formatting
        day = day.replace("0", "")
    day = int(day)
    location = Point(location.latitude, location.longitude, 70) # 3rd param is altitude
    hourlyTemp = []
    current_year = 2005
    end_year = 2023
    while current_year != end_year:
        start = datetime(current_year, month, day, hour=timeOfDay)  # year month day hour = x
        end = datetime(current_year, month, day, hour=timeOfDay)  # year month day hour = x
        data = Hourly(location, start, end)

        data = data.fetch()
        # print(data)
        # print(data)
        if not data.empty:
            hourlyTemp.append(float(data["temp"]))
        current_year += 1
    # print(str(time.time() - start_time) + " time to complete")

    # start = datetime(current_year, month, day, hour=timeOfDay)  # year month day hour = x
    # end = datetime(end_year, month, day, hour=timeOfDay)  # year month day hour = x
    # data = Hourly(location, start, end)
    # data = data.fetch()
    # # slower approach?
    # hour_counter = 0
    # year_counter = 0
    # total_hours = (end_year - current_year + 1) * 24 * 365
    # while hour_counter <= total_hours: ## ends when 2023 ends
    #     try:
    #         hourlyTemp.append(float(data.iloc[hour_counter]["temp"]))
    #     except IndexError: ## might want to remove this?
    #         print("no data")
    #         return 0
    #     # print(data.iloc[hour_counter]) # for time validation
    #     if (((year_counter + 1) % 4 == 0) and (year_counter != 0)): ## for leap years
    #         hour_counter += 8784 # 8784 hrs in a leap year
    #     else:
    #         hour_counter += 8760 #8760 hrs in a year
    #     year_counter += 1
    # print(str(time.time() - start_time) + " time to complete")

    if len(hourlyTemp) == 0:
        return 0
    hourlyTempAvgOnDay = float(sum(hourlyTemp) / len(hourlyTemp)) # gets the mean temp at a certain hour of the year over many years
    # print(hourlyTempAvgOnDay)
    return hourlyTempAvgOnDay # in celsius °C

    #plot code
    # data.plot(y=['tavg', 'tmin', 'tmax'])
    # plt.show()

# print(historicalHourlyTemp(str(20010402), "BAL", "D"))
df = pd.read_csv("fileoutput3.csv")
# df.insert(1, column="HistoricalAvgHrlyTemp", value="")
for index, row in df.iterrows():
    if 1793 <= index:
        try:
            output_val = historicalHourlyTemp(str(row["Date"]), row["HomeTeam"], row["DayNight"])
            df.at[index, "HistoricalAvgHrlyTemp"] = output_val
            # print(index)
        except Exception as e:
            print(e)
            df.to_csv("fileoutput3.csv", index=False)
            break

    # seen_gamedates[row["Date"]] = output_val
    # else:
    #     df.at[index,"HistoricalAvgHrlyTemp"] = seen_gamedates[row["Date"]]
    # print(seen_gamedates)
df.to_csv("outputs2.csv", index = False)
# print(df)





