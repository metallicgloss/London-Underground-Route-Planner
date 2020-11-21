// Initialise bloodhound suggestion engine.
var stationList = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/search-station?station=%QUERY',
        wildcard: '%QUERY',
        transform(response) {
            // For each response, if not in list, add to cache.
            response.forEach(function (item) {
                if (stationList.valueCache.indexOf(item) === -1) {
                    stationList.valueCache.push(item);
                }
            });
            return response;
        }
    }
});
stationList.valueCache = [];

// Assign origin and destination fields to be typeahead fields. Point to suggestion engine.
$('#origin-location, #destination-location').typeahead({
    minLength: 1,
    hint: true,
    highlight: true,
    autoselect: true
}, {
    name: 'available-stations',
    limit: 10,
    source: stationList,

    templates: {
        header: '<p class="results-found">Suggested Underground Stations</p><hr>',
        empty: [
            '<div class="empty-message">',
            '<p class="no-results-found">Sorry!</p><hr>No available suggestions.<br>',
            '</div>'
        ].join('\n'),
        suggestion: function (data) {
            return '<p>' + data + '</p>';
        }
    }
}).bind('change blur', function () {
    // On field change, if value is not in the cached list, clear and warn.
    if ((stationList.valueCache.indexOf($(this).val()) === -1) && ($(this).val() != "")) {
        // Add text danger to the applicable title - parent seems to not be working as expected.
        if ($(this).attr('id') == "origin-location") {
            $('.from-title').addClass('text-danger');
            $('#origin-location').addClass('invalid-selection');
        } else {
            $('.to-title').addClass('text-danger');
            $('#destination-location').addClass('invalid-selection');
        }

        // Display error popup to user.
        $('#error-message-content').html("Please select a station from the available dropdown.");
        $('#error-message').modal('show');

        // Clear value
        $('#' + $(this).attr('id')).val('')
    }
    else {
        // Else, clear warning and accept input.
        if ($(this).attr('id') == "origin-location") {
            $('.from-title').removeClass('text-danger');
            $('#origin-location').removeClass('invalid-selection');
        } else {
            $('.to-title').removeClass('text-danger');
            $('#destination-location').removeClass('invalid-selection');
        }
    }
});

// Modify user interaction with page to provide a more clean experience.
$("body").on("contextmenu", function (e) {
    return false;
});
$("img").mousedown(function (e) {
    e.preventDefault()
});


function time_set() {
    $('.at-title').removeClass('text-danger');
}

var existingSearch = false;

// Handle route search query
$('#selection-submit-button').click(function () {
    // If both search fields are not blank.
    if ([$('#origin-location').val(), $('#destination-location').val(), $('#start-time').val()].every(function (i) { return i !== ""; })) {
        // If time ends in 0 or 5
        if (/^([0-1]?[0-9]|2[0-3]):[0-5][0,5]$/.test($('#start-time').val())) {

            // If existing search performed, reset.
            if (existingSearch == true) {
                $("#route-table, #summary-block").empty();
            }

            existingSearch = true;
            var locations = [];

            // Execute ajax call to get route data.
            $.ajax({
                url: "search-route",
                data: {
                    "origin_location": $('#origin-location').val(),
                    "destination_location": $('#destination-location').val(),
                    "start_time": $('#start-time').val()
                },
                success: function (response) {
                    // Route confirmed as valid.
                    if (response['raw_data']['response_message'] == "") {

                        // Export data to table, summary and total box.
                        $('#route-table').append(response['route_table'])
                        $('#summary-block').append(response['route_summary'])
                        $('#dijkstra').html(parseFloat(response['raw_data']['route_timings']['dijkstra']).toFixed(10))
                        $('#structure').html(parseFloat(response['raw_data']['route_timings']['structure']).toFixed(10))
                        $('#total-travel-time').html(response['route_travel_time'])

                        // Expand route box.
                        $('.selection-box').addClass('selection-box-large');
                        $('.route-selection').show();

                        // Define locations.
                        locations = response['raw_data']['route_locations']

                        // If coordinates are empty, geocoding disabled.
                        if (locations.length != 0) {
                            // Set map object to correct height based on number of stations in the route.
                            $('#map-object').height(((Object.keys(response['raw_data']['route']).length - 1) * 42) + 100)

                            // Create styled map with center in the middle of London
                            const map = new google.maps.Map(document.getElementById("map-object"), {
                                center: {
                                    lat: response['raw_data']['route_locations'][0]['latitude'],
                                    lng: response['raw_data']['route_locations'][0]['longitude']
                                },
                                zoom: 12,
                                disableDefaultUI: true,
                                // To adjust styles, please import json to https://mapstyle.withgoogle.com/
                                styles: [
                                    {
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#ffffff"
                                            }
                                        ]
                                    },
                                    {
                                        "elementType": "labels.icon",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#616161"
                                            }
                                        ]
                                    },
                                    {
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "color": "#f5f5f5"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "administrative",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "administrative",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape",
                                        "elementType": "labels.text",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape.natural.landcover",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape.natural.terrain",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "landscape.natural.terrain",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#eeeeee"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi",
                                        "elementType": "labels",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi",
                                        "elementType": "labels.text",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#757575"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi.park",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#e5e5e5"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi.park",
                                        "elementType": "geometry.fill",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "poi.park",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#ffffff"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.arterial",
                                        "elementType": "geometry.fill",
                                        "stylers": [
                                            {
                                                "color": "#dadada"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.arterial",
                                        "elementType": "labels",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.arterial",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#757575"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.highway",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#ebebeb"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.highway",
                                        "elementType": "labels",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.highway",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#616161"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.highway.controlled_access",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#dadada"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.local",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "road.local",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#9e9e9e"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "transit",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "transit.line",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#e5e5e5"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "transit.station",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#eeeeee"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "water",
                                        "elementType": "geometry",
                                        "stylers": [
                                            {
                                                "color": "#dedede"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "water",
                                        "elementType": "labels.text",
                                        "stylers": [
                                            {
                                                "color": "#0060a8"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "water",
                                        "elementType": "labels.text.fill",
                                        "stylers": [
                                            {
                                                "color": "#9e9e9e"
                                            }
                                        ]
                                    },
                                    {
                                        "featureType": "water",
                                        "elementType": "labels.text.stroke",
                                        "stylers": [
                                            {
                                                "visibility": "off"
                                            }
                                        ]
                                    }
                                ]
                            });

                            // Draw lines between each station with their corresponding tube line colour.
                            // Not using Google direction service to have more control over the colours; also, direction service doesnt allow waypoints / stops when using train as transport.
                            locations.forEach(function (value, i) {
                                // If there is a next station (not at the end of the route)
                                if (typeof locations[i + 1] !== 'undefined') {
                                    // Parse polygon shape using the current station and the next station.
                                    var selectedPolygon = [
                                        { lat: locations[i]['latitude'], lng: locations[i]['longitude'] },
                                        { lat: locations[i + 1]['latitude'], lng: locations[i + 1]['longitude'] },
                                    ]

                                    // Create a new polyline with the data.
                                    const selectedJourney = new google.maps.Polyline({
                                        path: selectedPolygon,
                                        geodesic: true,
                                        strokeColor: getComputedStyle(document.documentElement).getPropertyValue(locations[i]['css_color_variable']),
                                        strokeOpacity: 1.0,
                                        strokeWeight: 4,
                                        map: map
                                    });
                                }
                            });
                        }
                        else {
                            $('#map-object').html("<div style='text-align:center'><span class='text-warning'><b>Geolocation Map Disabled By Administrator</b></span><p>The geocoding facility of this application has been disabled by the website administrator. We're sorry for any inconvenience caused. <br><br>To enable geolocation, please enable route_geocoding in the configuration file; if you're not the admin, please contact support.</p></div>")
                        }
                    } else {
                        // Route invalid.
                        // Display error popup to user.
                        $('#error-message-content').html("Sorry! We couldn't calculate your route.<br><br>Your requested journey would have taken " + response['route_travel_time'] + " minutes; please ensure that your entire journey can be completed during opening hours.");
                        $('#error-message').modal('show');
                        $('.at-title').addClass('text-danger');
                    }
                },
                error: function (xhr) {
                    $('#error-message-content').html("Sorry! We've run into an undefined error. Please report the following to a system administrator. <br><br>" + xhr);
                    $('#error-message').modal('show');
                }
            });
        }
        else {
            $('#error-message-content').html("Sorry! Your selected departure time is unavailable, please select an alternative start time time.<br><br>Trains leaving your selected origin station depart every 5 minutes (EG :00, :05, :10, :15).");
            $('#error-message').modal('show');
        }
    } else {
        // One field failed to be entered.
        error_message = ""

        // If origin station not set, add message to error and set field to red.
        if ($('#origin-location').val() == "") {
            error_message += "Please enter your origin station.<br>";
            $('.from-title').addClass('text-danger');
            $('#origin-location').addClass('invalid-selection');
        }

        // If destination station not set, add message to error and set field to red.
        if ($('#destination-location').val() == "") {
            error_message += "Please enter your destination station.<br>";
            $('.to-title').addClass('text-danger');
            $('#destination-location').addClass('invalid-selection');
        }

        // If start time not set, add message to error and set field to red.
        if ($('#start-time').val() == "") {
            error_message += "Please enter a time to start your journey.";
            $('.at-title').addClass('text-danger');
        }

        // Set modal content, display.
        $('#error-message-content').html(error_message);
        $('#error-message').modal('show');
    }
});
