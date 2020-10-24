"""A class used to store each station as a node and its connections"""
from station_manager import StationHandler
import time
import array
import pandas as pd
import sys
from pprint import pprint

sys.path.append("../Experiments_And_Prototypes/Prototypes/station_manager.py")


if __name__ == "__main__":
    """Reading the Excel Sheet, and renaming the DataFrame Columns"""
    data = pd.read_excel("TFL_Underground_Data_Original.xlsx")
    data.columns = ["Line", "Origin", "Destination", "Time"]
    S = StationHandler()

    '''Sanitizing the missing Lines, making it comparing to the before and the after'''
    for i in range(len(data.index)):
        if pd.isna(data["Line"].iloc[i]):
            print("No Line on index {}".format(i))
            if data["Line"].iloc[i-1] == data["Line"].iloc[i+1]:
                print("Changing index {} to {}".format(
                    i, data["Line"].iloc[i+1])
                )
                data.at[i, "Line"] = data["Line"].iloc[i+1]

    '''Sanitizing the extra White Spaces'''
    for i in range(len(data.index)):
        if type(data.at[i, "Line"]) is str:
            data.at[i, "Line"] = data["Line"].iloc[i].strip(" ")
        if type(data.at[i, "Origin"]) is str:
            data.at[i, "Origin"] = data["Origin"].iloc[i].strip(" ")
        if type(data.at[i, "Destination"]) is str:
            data.at[i, "Destination"] = data["Destination"].iloc[i].strip(" ")

    """Inserting all the stations in alphabetic order"""
    def insert_stations(dataframe, S):
        for i in range(len(dataframe.index)):
            try:
                S.add_station_alphabetically(dataframe["Origin"].iloc[i])
            except Exception:
                pass
        return S

    """Inserting all the connections"""
    def insert_connections(dataframe, S):
        for i in range(len(data.index)):
            if pd.isna(data["Destination"].iloc[i]):
                pass
            else:
                origin = S.get_station_node_by_name(
                    dataframe["Origin"].iloc[i]
                )
                destination = S.get_station_node_by_name(
                    dataframe["Destination"].iloc[i]
                )
                line = dataframe["Line"].iloc[i]
                time = int(dataframe["Time"].iloc[i])
                try:
                    origin.add_station_connection(destination, time, line)
                except Exception:
                    pass
        return S

    S = insert_stations(data, S)
    S.print_all_stations()
    S = insert_connections(data,S)
    print(S.get_station_node_by_name("Bank").get_station_connection("Moorgate"))
    print(S.get_station_node_by_name("Bermondsey").get_station_connection("Canada Water"))
    print(S.get_station_node_by_name("Green Park").get_station_connection("Bond Street"))
    # S.print_all_stations()
