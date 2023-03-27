# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:26:11 2023

@author: Jackrog
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:01:56 2023

@author: Jackrog
"""

import pandas as pd
import numpy as np
import datetime

gl = pd.read_csv("C:\\Users\\Jackrog\\Desktop\\MinneMudac\\train.csv")


gl = gl.dropna()
gl['Date'] = pd.to_datetime(gl['Date'])

gl = gl.loc[gl['HomeTeam'] == "MIN"]
gl.info()

gl.head()

gl['Month'] = gl['Date'].dt.strftime('%m')
gl['Month'].unique()


gl["Month"] = gl["Month"].astype("category")
gl["DayNight"] = gl["DayNight"].astype("category")
gl["DayofWeek"] = gl["DayofWeek"].astype("category")

from sklearn.preprocessing import OrdinalEncoder
encoder = OrdinalEncoder()
encoder.fit(gl[["Month", "DayNight", "DayofWeek"]])
gl[["Month_encoded", "DayNight_encoded", "DayofWeek_encoded"]] = encoder.transform(gl[["Month", "DayNight", "DayofWeek"]])


gl["Capacity"] = gl["Capacity"].str.replace(',','')
gl["Capacity"] = gl["Capacity"].astype("float")


war = pd.read_csv("C:\\Users\\Jackrog\\Desktop\\MinneMudac\\top3war.csv")
gl = pd.merge(gl, war, right_on=["Team", "Season"], left_on=["VisitingTeam", "Year"])


from sklearn.preprocessing import OrdinalEncoder

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score

mask = gl['Date'] >= pd.Timestamp('2022-01-01')
test=gl.loc[mask]

mask = gl['Date'] < pd.Timestamp('2022-01-01')
train=gl.loc[mask]
mask = gl['Date'] > pd.Timestamp('2013-01-01')
train=train.loc[mask]


xtrain = train[['DistanceBetweenStadiums', 'HistoricalAvgHrlyTemp', 'NumberofGames',"Month_encoded", "DayNight_encoded", "DayofWeek_encoded", 'same_division', 'elo', 'Sum_WAR']]
ytrain = train['Attendance']

xtest = test[['DistanceBetweenStadiums', 'HistoricalAvgHrlyTemp', 'NumberofGames',"Month_encoded", "DayNight_encoded", "DayofWeek_encoded", 'same_division', 'elo', 'Sum_WAR']]
ytest = test['Attendance']

from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

boost = GradientBoostingRegressor()
boost.fit(xtrain,ytrain)
y_pred=boost.predict(xtest)
test = mean_absolute_error(ytest.to_numpy(),y_pred)
test


from boruta import BorutaPy
boruta = BorutaPy(boost, n_estimators = 'auto', verbose = 2, random_state = 1)
boruta.fit(np.array(xtrain), np.array(ytrain))

print("Ranking: ",boruta.ranking_)          
print("No. of significant features: ", boruta.n_features_)



list(xtest.columns)

import matplotlib.pyplot as plt
fi = boost.feature_importances_
fi[1]
plt.bar(range(len(fi)),fi)
plt.xlabel('Index')
plt.ylabel('Value')
plt.xticks(range(12))
plt.show()



# from sklearn.model_selection import cross_val_predict
# import matplotlib.pyplot as plt
# from sklearn.metrics import PredictionErrorDisplay

# fig, axs = plt.subplots(ncols=2, figsize=(8, 4))
# PredictionErrorDisplay.from_predictions(
#     ytest,
#     y_pred=y_pred,
#     kind="actual_vs_predicted",
#     subsample=100,
#     ax=axs[0],
#     random_state=0,
# )
# axs[0].set_title("Actual vs. Predicted values")
# PredictionErrorDisplay.from_predictions(
#     ytest,
#     y_pred=y_pred,
#     kind="residual_vs_predicted",
#     subsample=100,
#     ax=axs[1],
#     random_state=0,
# )
# axs[1].set_title("Residuals vs. Predicted Values")
# fig.suptitle("Plotting cross-validated predictions")
# plt.tight_layout()
# plt.show()

# import sklearn
# print(sklearn.__version__)