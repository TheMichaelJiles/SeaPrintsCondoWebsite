var placeSearch, autocomplete;
var componentForm = {
    id_street_number: 'short_name',
    id_route: 'long_name',
    id_city: 'long_name',
    id_state: 'short_name',
    id_country: 'long_name',
    id_zip_code: 'short_name',
};

var converter = {
    street_number: 'id_street_number',
    route: 'id_route',
    locality: 'id_city',
    administrative_area_level_1: 'id_state',
    country: 'id_country',
    postal_code: 'id_zip_code',
}

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'), { types: ['geocode'] }
    );
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    var place = autocomplete.getPlace();
    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[converter[addressType]]) {
            var val = place.address_components[i][componentForm[converter[addressType]]];
            document.getElementById(converter[addressType]).value = val;
        }
    }
}

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}