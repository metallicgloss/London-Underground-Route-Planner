import xlrd
import array
import re


workbook = xlrd.open_workbook("London Underground data.xlsx")
data_sheet = workbook.sheet_by_index(0)

train_information = {}
log_records = []

all_time_values = array.array("i",)

LAST_ROW_NUMBER = 758

def check_for_illegal_characters_present(text):
    """ Returns True if illegal characters are found in the string """
    return re.match("[A-Za-z]+[0-9\(\)\-\.\,\& \'A-Za-z]*", text)[0] != text

def get_lower_and_upper_bound_extreme_values():
    """ Returns the upper and lower bound of what is considered an anomaly """
    # A value is considered an anomaly when it deviates 3 times the standard deviation greater / less than the mean
    global all_time_values
    mean = sum(all_time_values) / len(all_time_values)
    var = sum([x ** 2 for x in all_time_values]) / len(all_time_values)
    sd = var ** 0.5
    upper_bound = round(mean + (3 * sd))
    lower_bound = round(mean - (3 * sd))
    return lower_bound, upper_bound

def get_row_information_from_excel(row_number):
    """ Returns the train line, starting train stop and next train stop at a specific row in the excel document """
    train_line = data_sheet.row(row_number)[0].value
    location_a = data_sheet.row(row_number)[1].value
    location_b = data_sheet.row(row_number)[2].value
    time = data_sheet.row(row_number)[3].value
    return_data = []
    for data in [train_line, location_a, location_b]:
        if data != "":
            data = data.upper()
        else:
            data = None
        return_data.append(data)
    if time != "":
        time = int(time)
    else:
        time = None
    return_data.append(time)
    return return_data

def check_value_is_not_none(value, log_message):
    """ Returns True if the value is not None, otherwise it will add a message to the log_records """
    global log_records
    value_is_none = value is None
    if value_is_none:
        log_records.append(log_message)
    return not value_is_none

def get_sanitised_sub_set_dictionary(dict_key, parent_dictionary, row_number):
    """ Checks for illegal characters in the dictionary key and creates a empty 
        dictionary with the specified key name if the key is not already present """
    global log_records
    if dict_key not in parent_dictionary.keys():
        parent_dictionary[dict_key] = {}
        if check_for_illegal_characters_present(dict_key):
            log_records.append("Illegal characters found in the text '" + dict_key + "' on row " + str(row_number))
    return parent_dictionary

def get_train_information_from_excel():
    """ Formats the data retrieved from the excel document """
    global train_information, log_records
    for row_number in range(LAST_ROW_NUMBER - 1):
        train_line, starting_point, next_point, time = get_row_information_from_excel(row_number)
        
        if check_value_is_not_none(value=train_line, log_message="Train line not provided on row " + str(row_number)):
            train_information = get_sanitised_sub_set_dictionary(train_line, train_information, row_number)
        
            if check_value_is_not_none(value=starting_point, log_message="Start location not provided on row " + str(row_number)):
                train_information[train_line] = get_sanitised_sub_set_dictionary(starting_point, train_information[train_line], row_number)
                
                if next_point is not None:
                    if time is None:
                        log_records.append("Missing time on row " + str(row_number))
                    else:
                        all_time_values.append(time)
                        if next_point not in train_information[train_line][starting_point].keys():
                            train_information[train_line][starting_point][next_point] = [time]
                            if check_for_illegal_characters_present(next_point):
                                log_records.append("Illegal characters found in the text '" + next_point + "' on row " + str(row_number))
                        else:
                            train_information[train_line][starting_point][next_point].append(time)

def check_for_duplicates_and_extreme_values():
    """ Searches for duplicates and extreme values in the formatted data generated from the excel document """
    lower_bound, upper_bound = get_lower_and_upper_bound_extreme_values()
    for train_line in train_information:
        last_stop = list(train_information[train_line].keys())[-1]
        if train_information[train_line][last_stop] != {}:
            log_records.append("End node not detected for train line " + train_line)
        for train_stop in train_information[train_line]:
            for next_stop in train_information[train_line][train_stop]:
                # Check for duplicate values
                if len(train_information[train_line][train_stop][next_stop]) > 1:
                    log_records.append("Multiple times provided from " + train_stop + " to " + next_stop + " using the " + train_line + " train line: [" + ",".join(str(train_information[train_line][train_stop][next_stop])) + "]")
                # Check for extreme values
                for time in train_information[train_line][train_stop][next_stop]:
                    if time >= upper_bound or time <= lower_bound or time == 0:
                        log_records.append("Extreme value '" + str(time) + "' detected from "+  train_stop + " to " + next_stop + " using the " + train_line + " train line")
                if train_information[train_line][train_stop][next_stop] == {}:
                    log_records.append("No time found from " + train_stop + " to " + next_stop + " using the " + train_line + " train line")

if __name__ == "__main__":
    get_train_information_from_excel()
    check_for_duplicates_and_extreme_values()
    for record in log_records: print(record)