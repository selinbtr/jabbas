
// called when text box value changes. Requires the value from it 
// from the ID of that input 
//document.getElementById.value()
// $('#idname').val();
function preMapper(){
    //get user zip code
    var userZipCode = $('#idname').val();
    //transform user zip code to coordinates in this format userLocation = [lat,long]
    var userLocation = aaaaaaa
    const APIKEY = "200794352-5993ea8c5073db58e8b8515192f76469"
    //query the api with fixed parameters and rtuern a json list object with 15 nearest trais 
    // might have to put this together first? 
    var trailQueryURL = `https://www.hikingproject.com/data/get-trails?lat=${userLocation[0]}`+`&lon=${userLocation[1]}`+`&maxDistance=25&maxResults=15&key=${APIKEY}`
    d3.json(trailQueryURL, markMaker)
}


//NOT COMPLETE
function markMarker(response){
    // Pull the "trails" property off of response.data
    var trails = response.data.trails;
    // Initialize an array to hold trail markers
    var trailMarkers = [];
    // Loop through the trails array
    for (var index = 0; index < trails.length; index++) {
      var station = trails[index];
      // For each station, create a marker and bind a popup with the station's name
      var trailMarker = L.marker([station.lat, station.lon])
        .bindPopup("<h3>" + station.name + "<h3><h3>Capacity: " + station.capacity + "</h3>");
      // Add the marker to the trailMarkers array
      trailMarkers.push(trailMarker);
    }
    // Create a layer group made from the trail markers array, pass it into the createMap function
    trailMapper(L.layerGroup(trailMarkers));
}

//NOT COMPLETE
function trailMapper(nearbyTrails) {
    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "light-v10",
      accessToken: "pk.eyJ1IjoianVsaWFsZW9ub2ZmIiwiYSI6ImNrYXR6NnRwbTBmcWMyeW9jemdnaTJ2ajgifQ.HSHs0WzCPhklGQIJX2-J3A"
    });

    var baseMaps = {
        "Light Map": lightmap
      };
    
      // Create an overlayMaps object to hold the bikeStations layer
      var overlayMaps = {
        "User Trails": nearbyTrails
      };
    
      // Create the map object with options
      var map = L.map("map-id", {
        center: userLocation,
        //center: [40.73, -74.0059],
        zoom: 12,
        layers: [lightmap, nearbyTrails]
      });
    
      // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
      L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
      }).addTo(map);
    
}