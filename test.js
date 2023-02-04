var map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
    /* No need to set credentials if already passed in URL */
    center:     new Microsoft.Maps.Location(-0.7167954182300451, 37.14737125795548),
    mapTypeId:  Microsoft.Maps.MapTypeId.roads,
    zoom:       16
});
var center = map.getCenter();
var Events = Microsoft.Maps.Events;
var Location = Microsoft.Maps.Location;
var Pushpin = Microsoft.Maps.Pushpin({


});
var pins = [
    new Pushpin(new Location(center.latitude, center.longitude), { color: '#f00' }),
    new Pushpin(new Location(center.latitude, center.longitude - 0.1), { icon: '/static/map-pin.png', anchor: new Microsoft.Maps.Point(12, 39), draggable: true })
];
map.entities.push(pins);
// Binding the events for the green pin
Events.addHandler(pins[1], 'dragend', function () {
    var newLocation = pins[1].getLocation();
    document.getElementById('latitude').innerHTML = 'Latitude: ' + newLocation.latitude;
    document.getElementById('longitude').innerHTML = 'Longitude: ' + newLocation.longitude;
    var latitude = newLocation.latitude;
    var longitude = newLocation.longitude;
})


