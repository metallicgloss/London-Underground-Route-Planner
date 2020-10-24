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

    print(data.iloc[50:150])

    """Inserting all the stations in alphabetic order"""
    def insert_stations(dataframe, S):
        for i in range(dataframe.size):
            try:
                S.add_station_alphabetically(dataframe["Origin"].iloc[i])
            except Exception:
                pass
        return S

    S = insert_stations(data, S)
    """This does return some duplicated stations, however, those are issues on the data sanitization"""
    S.print_all_stations()


