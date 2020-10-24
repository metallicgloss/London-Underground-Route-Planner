"""A class used to store each station as a node and its connections"""
import time, array
import pandas as pd
import sys
sys.path.append("../Experiments_And_Prototypes/Prototypes/station_manager_fixed.py")
from station_manager_fixed import StationHandler


if __name__ == "__main__":

    """Reading the Excel Sheet, and renaming the DataFrame Columns"""
    data = pd.read_excel("TFL_Underground_Data_Original.xlsx")
    data.columns = ["Line", "Origin", "Destination", "Time"]
    S = StationHandler()


    def data_handler(dataframe, S):
        for i in range(dataframe.size):
            if dataframe["Origin"].iloc[i] == S._head.station_name:
                print("station already added")
            S.add_station_alphabetically(dataframe["Origin"].iloc[i])
        return S


    S = data_handler(data, S)
    S.print_all_stations()


