import json

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Data Formatter Class                          #
#                            1.1 Initialise Object                            #
#                            1.2 Get Route                                    #
#                            1.3 Get Formatted Route                          #
#                            1.4 Get Formatted Summary                        #
#                            1.5 Get Formatted Change                         #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. Data Formatter Class                          #
# --------------------------------------------------------------------------- #


class HTMLFormatter:

    # ----------------------------------------------------------------------- #
    #                        1.1 Initialise Object                            #
    # ----------------------------------------------------------------------- #

    # Initialise the data Formatter object.
    def __init__(self, route_data):
        # Initialise Variables
        self.time_sub_total = 0
        self.time_to_station = 0
        self.origin_of_line = ""
        self.current_underground_line = ""
        self.route_data = route_data

        # Define response format.
        self.formatted = {
            'route_table': '',
            'route_summary': '',
            'route_travel_time': 0
        }

    # ----------------------------------------------------------------------- #
    #                        1.2 Get Route                                    #
    # ----------------------------------------------------------------------- #

    # Generate HTML formatted data
    def format_route(self):
        # For each route in the data, build HTML table content to display and location list.
        for route_index, route in enumerate(self.route_data['route']):
            # Get the time taken to get to station from last route.
            if (route_index != 0):
                # If not the first station, set time to station from previous route.
                self.time_to_station = self.route_data['route'][
                    route_index - 1
                ]['travel_time']

            else:
                # First station, set first origin of the line.
                self.origin_of_line = route['from']
                self.current_underground_line = route['train_line']

            # Create list table entry.
            self.formatted['route_table'] += self.get_route(
                route['from'],
                route['train_line'],
                self.time_to_station,
                self.time_sub_total
            )

            # If change_line flag set, route has changed to the previous route.
            # Add summary line to the data set, reset origin.
            if(route['change_line']):
                # Create summary list entry.
                self.formatted['route_summary'] += self.get_summary(
                    self.origin_of_line,
                    route['from'],
                    self.current_underground_line
                )

                # Create summary list entry.
                self.formatted['route_summary'] += self.get_change(
                    route['from'],
                    self.current_underground_line,
                    route['train_line']
                )

                # Reset origin for new underground line.
                self.origin_of_line = ""

            # If origin of line blank, this is the first route on the new line.
            if(self.origin_of_line == ""):
                # Set new origin, set line of the route.
                self.origin_of_line = route['from']
                self.current_underground_line = route['train_line']

            # Add travel time from previous station to running total.
            self.time_sub_total += route['travel_time']

            # If last route in the list.
            if (len(self.route_data['route']) == (route_index + 1)):
                # Add destination.
                self.formatted['route_table'] += self.get_route(
                    route['to'],
                    "-",
                    self.route_data['route'][route_index]['travel_time'],
                    self.time_sub_total
                )

                # Create summary list entry.
                self.formatted['route_summary'] += self.get_summary(
                    self.origin_of_line,
                    route['to'],
                    self.current_underground_line
                )

        self.formatted['route_travel_time'] = self.time_sub_total

        return self.formatted

    # ----------------------------------------------------------------------- #
    #                        1.3 Get Formatted Route                          #
    # ----------------------------------------------------------------------- #

    # Return the route segment formatted for HTML list.
    def get_route(self, station_name: str, underground_line: str, travel_time: int, total_travel_time: int) -> str:
        return (
            "<tr> <td>{stn}</td><td class='{line_cls}'>{line} {line_status}</td><td>{total} mins <small>(+{increase} mins)</small></td></tr>".format(
                stn=station_name,
                line_cls=underground_line.lower(),
                line=underground_line,
                line_status="Line" if underground_line != "-" else "",
                total=str(total_travel_time),
                increase=str(travel_time)
            )
        )

    # ----------------------------------------------------------------------- #
    #                        1.4 Get Formatted Summary                        #
    # ----------------------------------------------------------------------- #

    # Return the route segment formatted for HTML summary.
    def get_summary(self, origin_station: str, destination_station: str, underground_line: str) -> str:
        return (
            "<li>{orig} Station to {dest} Station - <span class='{line_cls}'>{line} Line</span></li>".format(
                orig=origin_station,
                dest=destination_station,
                line_cls=underground_line.lower().split(" ", 1)[0],
                line=underground_line
            )
        )

    # ----------------------------------------------------------------------- #
    #                        1.5 Get Formatted Change                         #
    # ----------------------------------------------------------------------- #

    # Return the route segment formatted for HTML summary.
    def get_change(self, station_name: str, from_line: str, to_line: str) -> str:
        return (
            "<li>Change at {stn} from the <span class='{from_cls}'>{from_line} Line</span> to the <span class='{to_cls}'>{to_line} Line</span></li>".format(
                stn=station_name,
                from_cls=from_line.lower().split(" ", 1)[0],
                from_line=from_line,
                to_cls=to_line.lower().split(" ", 1)[0],
                to_line=to_line
            )
        )
