/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">


// ====================================== MAP ===========================================

let map;
let curPosMarker;

pin_img = '../static/img/location-pin.png';
van_img = '../static/img/van.png'

api_key = '&key=AIzaSyAs2Up6ElWDzv9GdisewIH2jMfvJXWp4bs'
geocode_request = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='

function initMap() {
    const CONFIGURATION = {
        "locations": [

        ],
        "mapOptions": {"fullscreenControl":false,"mapTypeControl":false,"streetViewControl":false,"zoom":18,"zoomControl":false,"maxZoom":20,"mapId":""},
        "mapsApiKey": "AIzaSyAs2Up6ElWDzv9GdisewIH2jMfvJXWp4bs",
        "capabilities": {"input":true,"autocomplete":true}
      };

    new LocatorPlus(CONFIGURATION);
  }

  function handleLocationError(browserHasGeolocation, map, pos) {
    infoWindow = new google.maps.InfoWindow();
    infoWindow.setPosition(pos);
    infoWindow.setContent(
      browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
  }
  
  /**
 * Defines an instance of the Locator+ solution, to be instantiated
 * when the Maps library is loaded.
 */
function LocatorPlus(configuration) {
    const locator = this;
  
    locator.locations = configuration.locations || [];
    locator.capabilities = configuration.capabilities || {};
  
    const mapEl = document.getElementById('gmp-map');
  
    locator.searchLocation = null;
    locator.searchLocationMarker = null;
    locator.selectedLocationIdx = null;
    locator.userCountry = null;
  
    // Initialize the map -------------------------------------------------------
    locator.map = new google.maps.Map(mapEl, configuration.mapOptions);

    const geocoder = new google.maps.Geocoder();
  
    var lat = document.getElementById("lat").value;
    var lon = document.getElementById("lon").value;

    var coords = new google.maps.LatLng(parseFloat(lat), parseFloat(lon))
    const vanMarker = document.createElement("div");

    vanMarker.className = "marker";

    updateStart();

    function updateStart(){
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                locator.map.setCenter(pos);

                curPosMarker = new google.maps.Marker({
                    position: pos,
                    map: locator.map,
                    title: 'Current Position',
                    draggable: true,
                    icon: {url:pin_img, scaledSize: new google.maps.Size(40, 40)}
                });

                const van = new google.maps.Marker({
                    position: coords,
                    map: locator.map,
                    icon: {url:van_img, scaledSize: new google.maps.Size(40, 40)}
                });

                const bounds = new google.maps.LatLngBounds();
                bounds.extend(curPosMarker.position)
                bounds.extend(coords);
                locator.map.fitBounds(bounds);
    
                },
                () => {
                handleLocationError(true, locator.map, locator.map.getCenter());
                }
            );
        } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, locator.map, locator.map.getCenter());
        }
    }
  

  }
  
window.initMap = initMap;