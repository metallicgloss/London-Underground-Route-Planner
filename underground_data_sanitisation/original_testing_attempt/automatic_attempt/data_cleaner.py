import xlrd
import array
import re

"""
checks
MISSING Train LINE                [ CHECK ]
MISSING TIME ENTRIE               [ CHECK ]
MISSING Start Stop                [ CHECK ]
ILLEGAL CHARACTER                 [ CHECK ]
EXTREME VALUES                    [ CHECK ] [Can trigger false positives]
MULTIPLE TIME ENTRIES             [ CHECK ]
DUPLICATE ROUTES                  [ CHECK ] [Can trigger false positive as the program cannot identify which nodes are meant to have multiple connected stations]
INCORRECT ROUTES                  [ Unable to complete unless the program is given data specifying which stations are connected to each other]
MISSING ROUTES                    [ CHECK ]
MISSING END NODE                  [ CHECK ]
UNKNOWN STATION NAME              [ CHECK ]
"""


class DataCleaner:

    class LogRecord:

        def __init__(self):
            self.MISSING_ROUTE = "MISSING ROUTE"
            self.INCORRECT_ROUTE = "INCORRECT ROUTE"
            self.DUPLICATE_ROUTE = "DUPLICATE ROUTE"
            self.MULTIPLE_TIME_ENTRIE = "MULTIPLE TIME ENTRIE"
            self.MISSING_TIME_ENTRY = "MISSING TIME ENTRY"
            self.EXTREME_VALUE = "EXTREME VALUE"
            self.MISSING_TRAIN_LINE = "MISSING TRAIN LINE"
            self.MISSING_START_STOP = "MISSING START STOP"
            self.ILLEGAL_CHARACTER = "ILLEGAL CHARACTER"
            self.MISSING_END_NODE = "MISSING END NODE"
            self.UNKOWN_STATION_NAME = "UNKNOWN STATION NAME"

            self._log_records = {
                self.MISSING_ROUTE: [],
                self.INCORRECT_ROUTE: [],
                self.DUPLICATE_ROUTE: [],
                self.MULTIPLE_TIME_ENTRIE: [],
                self.MISSING_TIME_ENTRY: [],
                self.EXTREME_VALUE: [],
                self.MISSING_TRAIN_LINE: [],
                self.MISSING_START_STOP: [],
                self.ILLEGAL_CHARACTER: [],
                self.MISSING_END_NODE: [],
                self.UNKOWN_STATION_NAME: []
            }

        def create_log(self, log_type: str, log_message: str) -> None:
            """ Adds a log message to the log records """
            self._log_records[log_type].append(log_message)

        def console_print_log(self) -> None:
            """ Displays all the log messages in a formatted form to the console """
            for log_type in self._log_records:
                if self._log_records[log_type] != []:
                    print(
                        log_type +
                        " (" + str(len(self._log_records[log_type])) + ")"
                    )
                    for message in self._log_records[log_type]:
                        print(message)

        @property
        def log_records(self) -> dict:
            return self._log_records

    def __init__(self, filename, last_row_number):
        self._train_information = {}
        self._log_records = self.LogRecord()
        self._LAST_ROW_NUMBER = last_row_number
        workbook = xlrd.open_workbook(filename)
        self._data_sheet = workbook.sheet_by_index(0)
        self._all_time_values = array.array("i",)
        self._get_train_information_from_excel()
        self._scan_for_errors()

    def _check_for_illegal_characters_present(self, text: str) -> bool:
        """ Returns True if illegal characters are found in the string """
        return re.match("[A-Za-z]+[0-9\(\)\-\.\,\& \'A-Za-z]*", text)[0] != text

    def _get_row_information_from_excel(self, row_number: int) -> list:
        """ Returns the train line, starting train stop and next train stop at a specific row in the excel document """
        train_line = self._data_sheet.row(row_number)[0].value
        location_a = self._data_sheet.row(row_number)[1].value
        location_b = self._data_sheet.row(row_number)[2].value
        time = self._data_sheet.row(row_number)[3].value
        return_data = []
        for data in [train_line, location_a, location_b]:
            if data != "":
                data = data.upper().strip()
                if self._check_for_illegal_characters_present(data):
                    self._log_records.create_log(
                        self._log_records.ILLEGAL_CHARACTER, "Illegal characters found in the text '" +
                        data + "' on row " + str(row_number + 1)
                    )
            else:
                data = None
            return_data.append(data)
        if time != "":
            time = int(time)
            self._all_time_values.append(time)
        else:
            time = None
        return_data.append(time)
        return return_data

    def _get_train_information_from_excel(self):
        """ Formats the data retrieved from the excel document """
        for row_number in range(self._LAST_ROW_NUMBER - 1):
            train_line, starting_point, next_point, time = self._get_row_information_from_excel(
                row_number
            )
            if train_line is None:
                self._log_records.create_log(
                    self._log_records.MISSING_TRAIN_LINE, "Train line not provided on row " +
                    str(row_number + 1)
                )
            else:
                if train_line not in self._train_information:
                    self._train_information[train_line] = {}

                if starting_point is None:
                    self._log_records.create_log(
                        self._log_records.MISSING_START_STOP, "Start location not provided on row " +
                        str(row_number + 1)
                    )

                else:
                    if starting_point not in self._train_information[train_line]:
                        self._train_information[train_line][starting_point] = {
                        }
                    if next_point is not None:
                        if next_point not in self._train_information[train_line][starting_point]:
                            self._train_information[train_line][starting_point][next_point] = [
                            ]

                        if time is not None:
                            self._train_information[train_line][starting_point][next_point].append(
                                time
                            )

                        else:
                            self._log_records.create_log(
                                self._log_records.MISSING_TIME_ENTRY, "Missing time on row " + str(row_number + 1) +
                                " between " + starting_point + " and " + next_point +
                                " using the " + train_line + " train line"
                            )

    def _scan_for_errors(self):
        """ Checks for errors in the given data and adds them to the log records """
        self._check_for_extreme_values_and_duplicate_time_entries()
        # TODO Find a way to determine if the node is meant to have multiple stations heading towards it e.g Harrow-on-the-Hill
        self._check_for_duplicate_next_points_in_same_train_line()
        self._check_for_missing_routes()
        self._check_for_missing_end_nodes()

    def _check_for_duplicate_next_points_in_same_train_line(self):
        """ Checks to see if multiple stations visit a specific station """
        for train_line in self._train_information:
            used_destination_points = []
            for starting_point in self._train_information[train_line]:
                for next_stop in self._train_information[train_line][starting_point]:
                    if next_stop not in used_destination_points:
                        used_destination_points.append(next_stop)
                    else:
                        log_message = "Duplicate Destination route to " + \
                            next_stop + " using the " + train_line + " train line"
                        if log_message not in self._log_records.log_records[self._log_records.DUPLICATE_ROUTE]:
                            self._log_records.create_log(
                                self._log_records.DUPLICATE_ROUTE, log_message
                            )

    def _check_for_extreme_values_and_duplicate_time_entries(self) -> None:
        """ Checks for extreme vaues and duplicate time entries in the data """
        lower_bound, upperbound = self._get_lower_and_upper_bound_extreme_values()
        for train_line in self._train_information:
            for start_point in self._train_information[train_line]:
                for next_point in self._train_information[train_line][start_point]:
                    if len(self._train_information[train_line][start_point][next_point]) > 1:
                        self._log_records.create_log(
                            self._log_records.MULTIPLE_TIME_ENTRIE,
                            "Multiple times provided from " + start_point + " to " + next_point +
                            " using the " + train_line + " train line: [" +
                            ",".join(
                                [
                                    str(x) for x in self._train_information[train_line][start_point][next_point]
                                ]
                            ) + "]"
                        )
                    elif len(self._train_information[train_line][start_point][next_point]) == 0:
                        self._log_records.create_log(
                            self._log_records.MISSING_TIME_ENTRY,
                            "No time entry provided from " + start_point + " to " +
                            next_point + " using the " + train_line + " train line"
                        )
                    for time in self._train_information[train_line][start_point][next_point]:
                        if time >= upperbound or time <= lower_bound or time == 0:
                            self._log_records.create_log(
                                self._log_records.EXTREME_VALUE, "Extreme value '" + str(time) +
                                "' detected from " + start_point + " to " + next_point +
                                " using the " + train_line + " train line"
                            )

    def _get_lower_and_upper_bound_extreme_values(self) -> [int, int]:
        """ Returns the upper and lower bound of what is considered an anomaly """
        # A value is considered an anomaly when it deviates 3 times the standard deviation greater / less than the mean
        arr_size = len(self._all_time_values)
        mean = sum(self._all_time_values) / arr_size
        var = sum([x ** 2 for x in self._all_time_values]) / arr_size
        sd = var ** 0.5
        upper_bound = round(mean + (3 * sd))
        lower_bound = round(mean - (3 * sd))
        return lower_bound, upper_bound

    def _check_for_missing_routes(self):
        """ Checks for stations that are not visited """
        for train_line in self._train_information:
            all_stations_used_frequencies = {
                a: 0 for a in self._train_information[train_line]}
            for starting_point in self._train_information[train_line]:
                for next_point in self._train_information[train_line][starting_point]:
                    if next_point not in list(all_stations_used_frequencies.keys()):
                        self._log_records.create_log(
                            self._log_records.UNKOWN_STATION_NAME,
                            "Station " + next_point + " has been registred as a station for the " +
                            train_line + " train line"
                        )
                    else:
                        all_stations_used_frequencies[next_point] += 1
            for starting_point in all_stations_used_frequencies:
                starting_point_has_not_been_visited = all_stations_used_frequencies[
                    starting_point] == 0
                starting_point_has_no_next_stop = self._train_information[train_line][starting_point] == {
                }
                if starting_point_has_not_been_visited and starting_point_has_no_next_stop:
                    self._log_records.create_log(
                        self._log_records.MISSING_ROUTE,
                        "Missing Route to " + starting_point + " using the " + train_line + " train line"
                    )

    def _check_for_missing_end_nodes(self):
        """ Checks that the last train station in a train line has no destination (next point) """
        for train_line in self._train_information:
            last_stop_key = list(
                self._train_information[train_line].keys())[-1]
            if self._train_information[train_line][last_stop_key] != {}:
                self._log_records.create_log(
                    self._log_records.MISSING_END_NODE,
                    "Missing End Node for train line: " + train_line
                )

    @property
    def train_information(self):
        """ Returns the train information """
        return self._train_information

    @property
    def log_records(self) -> dict:
        """ Returns the log records """
        return self._log_records.log_records

    def console_print_logs(self):
        """ Displays all the log messages in a formatted form to the console """
        self._log_records.console_print_log()


if __name__ == "__main__":
    LAST_ROW_NUMBER = 758
    data_cleaner_obj = DataCleaner(
        "London Underground data.xlsx", LAST_ROW_NUMBER)
    data_cleaner_obj.console_print_logs()
