"""
# Created by ashish1610dhiman at 17/04/23
Contact at ashish1610dhiman@gmail.com
"""

import pandas as pd
import numpy as np
import datetime
from meteostat import Stations,Daily,Hourly
import pickle
from scipy import stats

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    :param lat1: latitude point 1
    :param lon1: longitude point 1
    :param lat2: latitude point 2
    :param lon2: longitude point 2
    :return: distance in Kms b/w 2 points
    """
    p = (np.pi/180)
    hav = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p)*np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p)) / 2
    return 12742 * np.arcsin(np.sqrt(hav))

def closest_airport(lat,long):
    """
    :param lat: latitude current location
    :param long: longitude current location
    :return: closest weather station
    """
    latitude_longitude_repo = pd.read_csv("../data/station_lat_longitude.csv", index_col=0)
    latitude_longitude_repo["distance"] = latitude_longitude_repo.apply(
        lambda x: haversine_distance(lat1=lat, lon1=long, \
                                     lat2=x["latitude"], lon2=x["longitude"]), axis=1)
    latitude_longitude_repo = latitude_longitude_repo.sort_values(by=["distance"])
    #     assert len(closest_aiport)==1, "More than 1 closest airport"
    return latitude_longitude_repo.iloc[0]["icao"], latitude_longitude_repo.index[0]

def get_discreet_time():
    """
    :return: current discretised time
    """
    time_now = datetime.datetime.now()
    hr_session = "day" if time_now.hour >= 9 and time_now.hour <= 21 else "night"
    season = "summer" if time_now.month >= 6 and time_now.month <= 9 else "winter"
    time_ad = f"{season}_{hr_session}"
    return time_ad

def get_realtime_weather(airport_api_id):
    """
    Get realtime weather at a location
    :param lat: point latitude
    :param long: point longitude
    :return: current weather
    """
    time_now = pd.Timestamp.now().round('60min').to_pydatetime()
    time_one = time_now + datetime.timedelta(hours=1)
    data = Hourly(airport_api_id, start=time_now, end=time_now)
    current_weather = data.fetch()
    return current_weather

def transform_weather(weather_avg_6):
    """
    Convert weather from metric to imperial
    :param weather_avg_6: point latitude
    :return: weather in imperial
    """
    temp_f = weather_avg_6[0] * 1.8 + 32
    hum = weather_avg_6[1]
    precip_in = weather_avg_6[2] / 25.4
    wspd_mph = weather_avg_6[4] / 1.609
    pres_in = weather_avg_6[5] * 0.02952998057228486
    return np.array([temp_f, hum, pres_in, precip_in, wspd_mph])

def weather_odds_helper(kde_pca_accidents,kde_pca_history,weather_now,if_bad=False,N=100):
    """
    :param kde_pca_accidents: KDE PCA dict for airport from accidents data
    :param kde_pca_history: KDE PCA dict for airport from history data
    :param weather_now: current weather
    :param N: number of trials for sample mean
    :return: Odds
    """
    #get discreet time
    time_ad = get_discreet_time()
    #get weather avg from history
    kde_kernel_accidents = kde_pca_accidents["kde"][time_ad]
    kde_kernel_accidents = stats.gaussian_kde(kde_kernel_accidents.dataset)
    kde_kernel_history = kde_pca_history["KDE"][time_ad]
    kde_kernel_history = stats.gaussian_kde(kde_kernel_history.dataset)
    weather_avg_samples = np.array([kde_kernel_history.resample(160).mean(axis=1) for i in range(N)])
    weather_avg_hist = np.mean(weather_avg_samples,axis=0)
    #densities from hist data
    density_weather_avg_hist = kde_kernel_history.evaluate(weather_avg_hist)[0]
    weather_cols_hist = ["temp","rhum","prcp","wdir","wspd","pres"]
    weather_now_pca_hist = kde_pca_history["PCA"].transform(weather_now[weather_cols_hist])[:,:2]
    density_weather_now_hist = kde_kernel_history.evaluate(weather_now_pca_hist)[0]
    #densities from accidents data
    weather_now_acc = transform_weather(weather_now[weather_cols_hist].values[0])
    weather_avg_6 = (weather_avg_hist @ kde_pca_history["PCA"].components_[:2,:]) + kde_pca_history["PCA"].mean_
    weather_avg_acc = transform_weather(weather_avg_6)
    weather_now_acc_pca = kde_pca_accidents["pca"].transform(weather_now_acc.reshape(1,-1))
    weather_avg_acc_pca = kde_pca_accidents["pca"].transform(weather_avg_acc.reshape(1,-1))
    density_weather_avg_acc = kde_kernel_accidents.evaluate(weather_avg_acc_pca)[0]
    density_weather_now_acc = kde_kernel_accidents.evaluate(weather_now_acc_pca)[0]
    if if_bad:
        density_weather_now_acc = density_weather_now_acc*1.1
    print (f""" density_weather_now_acc:{density_weather_now_acc:.6f}
    density_weather_avg_acc:{density_weather_avg_acc:.6f}
    density_weather_avg_hist:{density_weather_avg_hist:.6f}
    density_weather_now_hist:{density_weather_now_hist:.6f}""")
    log_odds = (np.log(density_weather_now_acc) -\
                np.log(density_weather_avg_acc) +\
               np.log(density_weather_avg_hist) - \
               np.log(density_weather_now_hist))
    return np.exp(log_odds)

def get_odds(lat,long, N= 250):
    """
    :param lat: latitude for current location
    :param long: longitude for current location
    :param N: #trials for estimating KDE mean
    :return:
    """
    # find closest airport
    airport_icao, airport_api_id = closest_airport(lat, long)
    print (f"Nearest airport weather stn to ({lat:.4f},{long:.4f}) is {airport_icao}")
    # find realtime weather
    print ("Fetching current weather")
    weather_now = get_realtime_weather(airport_api_id)
    # read kde estimate for historical data
    with open('../data/accidents_kde.pickle', 'rb') as f:
        # Load the data from the pickle file
        kde_accidents_dict = pickle.load(f)
    with open('../data/kde_dict.pickle', 'rb') as f:
        # Load the data from the pickle file
        kde_historical_dict = pickle.load(f)
    kde_pca_accidents = kde_accidents_dict[airport_icao]
    kde_pca_history = kde_historical_dict[airport_icao]
    print ("Densities for weather now")
    weather_odds_normal = weather_odds_helper(kde_pca_accidents, kde_pca_history, weather_now,False,N)
    weather_now_bad = weather_now.copy()
    kde_pca_accidents = kde_accidents_dict["KBMG"]
    weather_bad_acc_samples = kde_pca_accidents["kde"][get_discreet_time()].resample(250)
    kde2 = stats.gaussian_kde(kde_pca_accidents["kde"][get_discreet_time()].dataset)
    weather_bad_acc_samples_density = kde2.evaluate(weather_bad_acc_samples)
    # print(weather_bad_acc_samples.shape,weather_bad_acc_samples_density.shape)
    weather_bad = weather_bad_acc_samples[:,np.argmax(weather_bad_acc_samples_density)]
    weather_bad_5cols = kde_pca_accidents["pca"].inverse_transform(weather_bad)
    weather_now_bad["prcp"] = weather_bad_5cols[3] * 25.4
    weather_now_bad["temp"] = (weather_bad_5cols[0]-32)/1.8
    weather_now_bad["pres"] = weather_bad_5cols[2] / 0.02952998057228486
    weather_now_bad["wspd"] = weather_bad_5cols[4] / 0.02952998057228486
    print("Densities for weather bad")
    weather_odds_bad = weather_odds_helper(kde_pca_accidents, kde_pca_history, weather_now_bad,True, N)
    print(f"\nOdds for weather_now={weather_odds_normal:.5f} vs Odds for weather_bad={weather_odds_bad:.5f}")
    return (weather_odds_normal,weather_odds_bad)