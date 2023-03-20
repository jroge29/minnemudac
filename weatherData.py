import math

from geopy.geocoders import Nominatim
from datetime import datetime
from meteostat import Hourly, Point
import matplotlib.pyplot as plt
import pandas as pd
import time
from tqdm import tqdm

# geolocator = Nominatim(user_agent="MyApp",timeout=10)
# location = geolocator.geocode("Seattle")
# location = Point(location.latitude, location.longitude, 70) # 3rd param is altitude
#
# start = datetime(2005, 4, 3, hour=2)  # year month day hour = x
# end = datetime(2005, 4, 3, hour=2)  # year month day hour = x
# data = Hourly(location, start, end)
# data = data.fetch()
# # print(data)
# print(data.iloc[:, 0])
# data.to_csv("testing.csv")

def historicalHourlyTemp(date: str, stadiumName: str, day_night: str):
    start_time = time.time()
    locations = {}
    if stadiumName == "COL":
        return 0
    if len(stadiumName) < 4: ## triggers if given abbreviation, turns it into a stadium name
        if stadiumName == "MON":
            stadiumName = "Montreal"
        else:
            df = pd.read_csv("2023_MLBSchedule.csv")
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
    current_year = 1973
    end_year = 2022

    start = datetime(current_year, 1, 1, hour=timeOfDay)  # year month day hour = x
    end = datetime(end_year, 12, 31, hour=timeOfDay)  # year month day hour = x
    data = Hourly(location, start, end)
    data = data.fetch()


    # print(str(time.time() - start_time) + " time to complete")



    return data


# print(historicalHourlyTemp(str(20010402), "BAL", "D"))
df = pd.read_csv("fullgl.csv")
df.insert(1, column="HistoricalAvgHrlyTemp", value="")
seen_teams = []
db_lst = []
for index, row in df.iterrows():
            if row["HomeTeam"] not in seen_teams:
                output_data = historicalHourlyTemp(str(row["Date"]), row["HomeTeam"], row["DayNight"])
                seen_teams.append(row["HomeTeam"])
                db_lst.append(output_data)
            elif row["HomeTeam"] in seen_teams:
                output_data = db_lst[seen_teams.index(row["HomeTeam"])]
            hourlyTemp = []
            current_year = 1973
            end_year = 2022
            hour_counter = 0
            year = int(str(row["Date"])[:4])
            month = str(row["Date"])[4:6]
            if (month[0] == '0'):  ## fixes date formatting
                month = month.replace("0", "")
            month = int(month)
            day = str(row["Date"])[6:8]
            if (day[0] == '0'):  ## fixes date formatting
                day = day.replace("0", "")
            day = int(day)
            # print(year)
            # hour_counter = 8784  # 8784 hrs in a leap year
              ## for leap years
            if month == 1:
                hour_counter = 24 * day
            if month == 2:
                hour_counter = 24 * day + (31 * 24)
            if month == 3:
                hour_counter = 24 * day + (31 * 24) + (28 * 24)
            if month == 4:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24)
            if month == 5:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24)
            if month == 6:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24)
            if month == 7:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24)
            if month == 8:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24) + (31 * 24)
            if month == 9:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (31 * 24)
            if month == 10:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (31 * 24) + (30 * 24)
            if month == 11:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (31 * 24) + (30 * 24) + (31 * 24)
            if month == 12:
                hour_counter = 24 * day + (31 * 24) + (28 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (31 * 24) + (30 * 24) + (31 * 24) + (30 * 24)
            if year % 4 == 0:
                print("here")
                hour_counter += 24
            year_counter = 0
            # total_hours = (end_year - current_year -1) * 24 * 365
            # print(total_hours)
            if type(output_data) != int:
                # print((output_data.shape[0]-1))
                while hour_counter <= (output_data.shape[0]-1):  ## ends when 2023 ends
                    # print(output_data)
                    # print(hour_counter)
                    if type(output_data) == int:
                        break
                    # print(output_data.iloc[[hour_counter]])
                    # print(row["Date"])
                    hourlyTemp.append(float(output_data.iat[hour_counter, 0]))
                    # print(data.iloc[hour_counter]) # for time validation
                    if (((year_counter+1) % 4 == 0)):  ## for leap years
                        hour_counter += 8784  # 8784 hrs in a leap year
                    else:
                        hour_counter += 8760  # 8760 hrs in a year
                    year_counter += 1
                if len(hourlyTemp) == 0:
                    df.at[index, "HistoricalAvgHrlyTemp"] = 0
                else:
                    hourlyTemp = [x for x in hourlyTemp if str(x) != 'nan']
                    hourlyTempAvgOnDay = float(sum(hourlyTemp) / len(hourlyTemp))
                    df.at[index, "HistoricalAvgHrlyTemp"] = hourlyTempAvgOnDay
            else:
                df.at[index, "HistoricalAvgHrlyTemp"] = 0
            # print(hourlyTemp)
            print(index)

df.to_csv("outputs2.csv", index = False)





