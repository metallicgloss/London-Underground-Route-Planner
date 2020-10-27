// Initialise bloodhound suggestion engine.
var stationList = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/search-station?station=%QUERY',
        wildcard: '%QUERY'
    }
});

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
});

// Handle route search query
$('#selection-submit-button').click(function () {
    // Expand route box.
    $('.selection-box').addClass('selection-box-large');
    $('.route-selection').show();

    // TODO: QUERY ROUTE DATA HERE
    // TODO: OUTPUT ROUTE DATA HERE

    // TEMPORARY: variable for station count.
    var stations = 5;

    // TEMPORARY: List of station coordinates
    var locations = [
        { lat: 51.5024413, lng: -0.1134282, color: '#ff0000' },
        { lat: 51.5072554, lng: -0.1221937, color: '#00ff00' },
        { lat: 51.501343, lng: -0.1248413 },
    ];

    // Set map object to correct height based on number of stations in the route.
    $('#map-object').height(((stations - 1) * 42) + 100)

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

    // Draw lines between each station with their corresponding tube line colour.
    // Not using Google direction service to have more control over the colours; also, direction service doesnt allow waypoints / stops when using train as transport.
    locations.forEach(function (value, i) {
        // If there is a next station (not at the end of the route)
        if (typeof locations[i + 1] !== 'undefined') {
            // Parse polygon shape using the current station and the next station.
            var selectedPolygon = [
                { lat: locations[i]['lat'], lng: locations[i]['lng'] },
                { lat: locations[i + 1]['lat'], lng: locations[i + 1]['lng'] },
            ]

            // Create a new polyline with the data.
            const selectedJourney = new google.maps.Polyline({
                path: selectedPolygon,
                geodesic: true,
                strokeColor: locations[i]['color'],
                strokeOpacity: 1.0,
                strokeWeight: 3,
                map: map
            });
        }
    });
});

