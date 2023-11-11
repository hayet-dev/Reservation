
var address = '4 rue gabriel goudy 44420 Nantes FRANCE';
var geocoder = new google.maps.Geocoder();

geocoder.geocode({ 'address': address }, function (results, status) {
    if (status === 'OK') {
        var latitude = results[0].geometry.location.lat();
        var longitude = results[0].geometry.location.lng();
        console.log('Latitude : ' + latitude);
        console.log('Longitude : ' + longitude);
    } else {
        console.log('La géolocalisation a échoué pour la raison suivante : ' + status);
    }
});
// getCoordinates.js
