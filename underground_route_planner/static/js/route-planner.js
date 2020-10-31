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
    if (stationList.valueCache.indexOf($(this).val()) === -1) {
        // Add text danger to the applicable title - parent seems to not be working as expected.
        if ($(this).attr('id') == "origin-location") {
            $('.from-title').addClass('text-danger');
        } else {
            $('.to-title').addClass('text-danger');
        }

        // Clear value
        $('#' + $(this).attr('id')).val('')
    }
    else {
        // Else, clear warning and accept input.
        if ($(this).attr('id') == "origin-location") {
            $('.from-title').removeClass('text-danger');
        } else {
            $('.to-title').removeClass('text-danger');
        }
    }
});

var existingSearch = false;

// Handle route search query
$('#selection-submit-button').click(function () {
    // If existing search performed, reset.
    if (existingSearch == true) {
        $("#route-table").empty();
        $("#summary-block").empty();
    }

    // If both search fields are not blank.
    if ([$('#origin-location').val(), $('#destination-location').val()].every(function (i) { return i !== ""; })) {
        existingSearch = true;
        var locations = [];

        // Execute ajax call to get route data.
        $.ajax({
            url: "search-route",
            data: {
                "origin_location": $('#origin-location').val(),
                "destination_location": $('#destination-location').val()
            },
            success: function (response) {
                // Export data to table, summary and total box.
                $('#route-table').append(response['TABLE_OUTPUT'])
                $('#summary-block').append(response['SUMMARY_OUTPUT'])
                $('#total-travel-time').html(response['RAW_DATA']['TOTAL_TRAVEL_TIME'])

                // Expand route box.
                $('.selection-box').addClass('selection-box-large');
                $('.route-selection').show();

                // Set map object to correct height based on number of stations in the route.
                $('#map-object').height(((Object.keys(response['RAW_DATA']['ROUTE']).length - 1) * 42) + 100)

                // Create styled map with center in the middle of London
                const map = new google.maps.Map(document.getElementById("map-object"), {
                    center: {
                        lat: 51.5074,
                        lng: -0.1278
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

                // Define locations.
                locations = response['LOCATION_DATA']

                // Draw lines between each station with their corresponding tube line colour.
                // Not using Google direction service to have more control over the colours; also, direction service doesnt allow waypoints / stops when using train as transport.
                locations.forEach(function (value, i) {
                    // If there is a next station (not at the end of the route)
                    if (typeof locations[i + 1] !== 'undefined') {
                        // Parse polygon shape using the current station and the next station.
                        var selectedPolygon = [
                            { lat: locations[i]['LATITUDE'], lng: locations[i]['LONGITUDE'] },
                            { lat: locations[i + 1]['LATITUDE'], lng: locations[i + 1]['LONGITUDE'] },
                        ]

                        // Create a new polyline with the data.
                        const selectedJourney = new google.maps.Polyline({
                            path: selectedPolygon,
                            geodesic: true,
                            strokeColor: getComputedStyle(document.documentElement).getPropertyValue(locations[i]['CSS_COLOR_VARIABLE']),
                            strokeOpacity: 1.0,
                            strokeWeight: 4,
                            map: map
                        });
                    }
                });
            },
            error: function (xhr) {
                console.log(xhr)
            }
        });
    } else {
        // Nicely handle error here.
    }

    // Clear input boxes to allow for immediate new route.
    $("#origin-location, #destination-location").val('');
});

