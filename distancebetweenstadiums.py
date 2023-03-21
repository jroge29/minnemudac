from geopy.geocoders import Nominatim
import pandas as pd
# geolocator = Nominatim(user_agent="MyApp", timeout=10)
# location = geolocator.geocode("Petco Park")
# location2 = geolocator.geocode("Truist Park")
# number = ((location2.latitude - location.latitude) ** 2 + (location2.longitude - location.longitude) ** 2) ** (1 / 2)
# print(number)
# print(location)
# print(location2)
# df = pd.read_csv("distwithmil.csv")
# seen_problem = []
# for index, row in df.iterrows():
#     if (row["HomeTeam"] == "ATL" and row["VisitingTeam"] == "SDN" or row["VisitingTeam"] == "ATL" and row["HomeTeam"] == "SDN") and row["DistanceBetweenStadiums"] == 0.0:
#         df.at[index, "DistanceBetweenStadiums"] = number
# df.to_csv("distwithatl.csv", index = False)

# geolocator = Nominatim(user_agent="MyApp", timeout=10)
# location = geolocator.geocode("Petco Park")
# location2 = geolocator.geocode("Truist Park")
# number = ((location2.latitude - location.latitude) ** 2 + (location2.longitude - location.longitude) ** 2) ** (1 / 2)
# print(number)
# print(location)
# print(location2)
df = pd.read_csv("distwithatl.csv")
seen_problem = {}
for index, row in df.iterrows():
    if row["DistanceBetweenStadiums"] == 0.0:
        if row["HomeTeam"] != "COL" and row["VisitingTeam"] != "COL" and (row["HomeTeam"],row["VisitingTeam"]) not in seen_problem or (row["HomeTeam"],row["VisitingTeam"]) not in seen_problem and row["VisitingTeam"] != "TEX" and row["HomeTeam"] != "TEX":
            df2 = pd.read_csv("2023_MLBSchedule.csv")
            for index, row2 in df2.iterrows():
                if row2["home_team"] == row["HomeTeam"]:
                    homeStadium = row2["stadium_name"]
                if row2["away_team"] == row["VisitingTeam"]:
                    awayStadium = row2["stadium_name"]
            geolocator = Nominatim(user_agent="MyApp", timeout=10)
            if homeStadium == "Oriole Park at Camden Yards":
                homeStadium = "Baltimore"
            if awayStadium == "Minute Maid Park":
                awayStadium = "Houston"
            if homeStadium == "Chase Field":
                homeStadium = "Phoenix"
            if awayStadium == "Chase Field":
                awayStadium = "Phoenix"
            if awayStadium == "Oriole Park at Camden Yards":
                awayStadium = "Baltimore"
            if awayStadium == "Oracle Park":
                awayStadium = "San Francisco"
            if homeStadium == "Oracle Park":
                homeStadium = "San Francisco"
            if awayStadium == "Oakland Coliseum":
                awayStadium = "Oakland, California"
            if homeStadium == "Oakland Coliseum":
                homeStadium = "Oakland, California"
            if awayStadium == "Global Life Field":
                awayStadium = "Arlington"
            if awayStadium == "TMobile Park":
                awayStadium = "Seattle"
            if homeStadium == "TMobile Park":
                homeStadium = "Seattle"
            tex = False
            tex2 = False
            if awayStadium == "Global Life Field":
                awayStadium = "Arlington, Texas"
                tex = True
            if homeStadium == "Global Life Field":
                homeStadium = "Arlington, Texas"
                tex2 = True
            location = geolocator.geocode(homeStadium)
            location2 = geolocator.geocode(awayStadium)
            print(awayStadium)
            print(location)
            print(location2)
            print(row["HomeTeam"] + " home team")
            print(row["VisitingTeam"] + " visiting team")
            if tex == True:
                # 32.74742857879089, -97.08396384735033
                number = ((32.74742857879089 - location.latitude) ** 2 + (-97.08396384735033 - location.longitude) ** 2) ** (1 / 2)
            if tex2 == True:
                number = ((location2.latitude - 32.74742857879089) ** 2 + (location2.longitude - -97.08396384735033) ** 2) ** (1 / 2)
            else:
                number = ((location2.latitude - location.latitude) ** 2 + (location2.longitude - location.longitude) ** 2) ** (1 / 2)
            print(number)
            df.at[index, "DistanceBetweenStadiums"] = number
            seen_problem[(row["HomeTeam"],row["VisitingTeam"])] = number
        elif (row["HomeTeam"],row["VisitingTeam"]) in seen_problem or (row["HomeTeam"],row["VisitingTeam"]) in seen_problem:
            df.at[index, "DistanceBetweenStadiums"] = seen_problem[(row["HomeTeam"], row["VisitingTeam"])]
df.to_csv("add_dist.csv", index = False)

# def betweenTwoStadiums(homeStadium, awayStadium):
#     df = pd.read_csv("2023_MLBSchedule.csv")
#     part1 = False
#     part2 = False
#     if homeStadium == "MON":
#         homeStadium = "Montreal"
#     if awayStadium == "LAN" and homeStadium == "ARI":
#         print("HERE")
#         geolocator = Nominatim(user_agent="MyApp", timeout=10)
#         location = geolocator.geocode("Dodger Stadium")
#         location2 = geolocator.geocode("Chase Field")
#         number = ((location2.latitude - location.latitude) ** 2 + (location2.longitude - location.longitude) ** 2) ** (1 / 2)
#         print(number)
#         return [number, location, location2]
#     else:
#         changed = False
#         changed2 = False
#
#         for index, row in df.iterrows():
#             if row["home_team"] == homeStadium and part1 == False:
#                 homeStadium = row["stadium_name"]
#                 part1 = True
#             if row["away_team"] == awayStadium and part2 == False:
#                 awayStadium = row["stadium_name"]
#             if part1 and part2:
#                 break
#         if homeStadium == "Oriole Park at Camden Yards":
#             homeStadium = "Baltimore"
#             changed = True
#         if homeStadium == "TMobile Park":
#             homeStadium = "Seattle"
#             changed = True
#         if homeStadium == "Busch Stadium":
#             homeStadium = "St. Louis"
#             changed = True
#         if homeStadium == "loanDepot park":
#             homeStadium = "Miami"
#             changed = True
#         if homeStadium == "Angel Stadium":
#             homeStadium = "Anaheim"
#             changed = True
#         if homeStadium == "Coors Field":
#             homeStadium = "Denver"
#             changed = True
#         if awayStadium == "Oriole Park at Camden Yards":
#             awayStadium = "Baltimore"
#             changed2 = True
#         if awayStadium == "TMobile Park":
#             awayStadium = "Seattle"
#             changed2 = True
#         if awayStadium == "Busch Stadium":
#             awayStadium = "St. Louis"
#             changed2 = True
#         if awayStadium == "loanDepot park":
#             awayStadium = "Miami"
#             changed2 = True
#         if awayStadium == "Angel Stadium":
#             awayStadium = "Anaheim"
#             changed2 = True
#         if awayStadium == "Coors Field":
#             awayStadium = "Denver"
#             changed2 = True
#         geolocator = Nominatim(user_agent="MyApp", timeout=10)
#         location = geolocator.geocode(homeStadium)
#         location2 = geolocator.geocode(awayStadium)
#         number = ((location2.latitude - location.latitude)**2 + (location2.longitude - location.longitude)**2)**(1/2)
#         # print(number)
#         if homeStadium == "COL" or awayStadium == "COL":
#             number = 0.0
#         return [number, location, location2]
#
#
# df = pd.read_csv("add_dist.csv")
# df.insert(1, column="DistanceBetweenStadiums", value="")
# seen_matchups = {}
# home_pos = {}
# away_pos = {}
# for index, row in df.iterrows():
#     if (row["HomeTeam"], row["VisitingTeam"]) and (row["VisitingTeam"], row["HomeTeam"]) in seen_matchups.keys():
#         df.at[index, "DistanceBetweenStadiums"] = seen_matchups[(row["HomeTeam"], row["VisitingTeam"])]
#     else:
#         if row["HomeTeam"] not in home_pos.keys() or row["VisitingTeam"] not in away_pos.keys():
#             output = betweenTwoStadiums(row["HomeTeam"], row["VisitingTeam"])
#             # print(output)
#             home_pos[row["HomeTeam"]] = output[1]
#             # print(output[2])
#             away_pos[row["VisitingTeam"]] = output[2]
#
#
#             seen_matchups[(row["HomeTeam"], row["VisitingTeam"])] = output[0]
#             seen_matchups[(row["VisitingTeam"], row["HomeTeam"])] = output[0]
#         else:
#             x = home_pos[row["HomeTeam"]]
#             y = away_pos[row["VisitingTeam"]]
#             output = ((y.latitude - x.latitude)**2 + (y.longitude - x.longitude)**2)**(1/2)
#             df.at[index, "DistanceBetweenStadiums"] = output
#
# df.to_csv("distoutputs2.csv", index = False)