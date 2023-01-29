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
van_img = '../static/img/van.img'

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
    const panelEl = document.getElementById('locations-panel');
    locator.panelListEl = document.getElementById('locations-panel-list');
    const sectionNameEl =
        document.getElementById('location-results-section-name');
    const resultsContainerEl = document.getElementById('location-results-list');
  
    locator.searchLocation = null;
    locator.searchLocationMarker = null;
    locator.selectedLocationIdx = null;
    locator.userCountry = null;
  
    // Initialize the map -------------------------------------------------------
    locator.map = new google.maps.Map(mapEl, configuration.mapOptions);
    const locationButton = document.createElement("button");

    const geocoder = new google.maps.Geocoder();
    const startInputEl = document.getElementById('start-input');

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
                curPosMarker.addListener("dragend", function(event){
                    var pos = event.latLng;
                    geocoder
                    .geocode({ location: pos })
                    .then((response) => {
                      if (response.results[0]) {
                        startInputEl.value = response.results[0].formatted_address
                      }
                    });
                });
    
                geocoder
                .geocode({ location: pos })
                .then((response) => {
                  if (response.results[0]) {
                    startInputEl.value = response.results[0].formatted_address
                  }
                });
    
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


    locationButton.textContent = "Pan to Current Location";
    locationButton.classList.add("custom-map-control-button");
    locator.map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {curPosMarker.setMap(null); updateStart()});
  
    // Store selection.
    const selectResultItem = function(locationIdx, panToMarker, scrollToResult) {
      locator.selectedLocationIdx = locationIdx;
      for (let locationElem of resultsContainerEl.children) {
        locationElem.classList.remove('selected');
        if (getResultIndex(locationElem) === locator.selectedLocationIdx) {
          locationElem.classList.add('selected');
          if (scrollToResult) {
            panelEl.scrollTop = locationElem.offsetTop;
          }
        }
      }
      if (panToMarker && (locationIdx != null)) {
        locator.map.panTo(locator.locations[locationIdx].coords);
      }
    };
  
    // Create a marker for each location.
    const markers = locator.locations.map(function(location, index) {
      const marker = new google.maps.Marker({
        position: location.coords,
        map: locator.map,
        title: location.title,
        icon: {url:van_img, scaledSize: new google.maps.Size(40, 40)}
      });
      marker.addListener('click', function() {
        selectResultItem(index, false, true);
      });
      return marker;
    });


    // Fit map to marker bounds.
    locator.updateBounds = function() {
      const bounds = new google.maps.LatLngBounds();
      bounds.extend(curPosMarker.position)
      if (locator.searchLocationMarker) {
        bounds.extend(locator.searchLocationMarker.getPosition());
      }
      for (let i = 0; i < markers.length; i++) {
        bounds.extend(markers[i].getPosition());
      }
      locator.map.fitBounds(bounds);
    };
    if (locator.locations.length) {
      locator.updateBounds();
    }
  
    // Render the results list --------------------------------------------------
  
    // When the results list re-renders, always update directions on the
    // first selection event.
    const getResultIndex = function(elem) {
      return parseInt(elem.getAttribute('data-location-index'));
    };
  
  
    // Optional capability initialization --------------------------------------
    initializeSearchInput(locator);
  
  }
  
  /** When the search input capability is enabled, initialize it. */
  function initializeSearchInput(locator) {
    const geocodeCache = new Map();
    const geocoder = new google.maps.Geocoder();
  
    const startInputEl = document.getElementById('start-input');
    const startButtonEl = document.getElementById('start-search-button');
  
    const destInputEl = document.getElementById('dest-input');
    const destButtonEl = document.getElementById('dest-search-button');

    const updateSearchLocation = function(address, location) {
      if (locator.searchLocationMarker) {
        locator.searchLocationMarker.setMap(null);
      }
      if (!location) {
        locator.searchLocation = null;
        return;
      }
      locator.searchLocation = {'address': address, 'location': location};
      locator.searchLocationMarker = new google.maps.Marker({
        position: location,
        map: locator.map,
        title: 'My location',
        draggable: true,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 12,
          fillColor: '#3367D6',
          fillOpacity: 0.5,
          strokeOpacity: 0,
        }
      })
      locator.searchLocationMarker.addListener("dragend", function(event){
        var pos = event.latLng;
        geocoder
        .geocode({ location: pos })
        .then((response) => {
          if (response.results[0]) {
            destInputEl.value = response.results[0].formatted_address
          }
        });
      });

      // Update the locator's idea of the user's country, used for units. Use
      // `formatted_address` instead of the more structured `address_components`
      // to avoid an additional billed call.
      const addressParts = address.split(' ');
      locator.userCountry = addressParts[addressParts.length - 1];
  
      // Update map bounds to include the new location marker.
      locator.updateBounds();
      // Update the result list so we can sort it by proximity.
    //   locator.renderResultsList();
    };
  
    const geocodeSearch = function(query, inputEl) {
      if (!query) {
        return;
      }
  
      const handleResult = function(geocodeResult) {
        inputEl.value = geocodeResult.formatted_address;
        updateSearchLocation(
            geocodeResult.formatted_address, geocodeResult.geometry.location);
      };
  
      if (geocodeCache.has(query)) {
        handleResult(geocodeCache.get(query));
        return;
      }
      const request = {address: query, bounds: locator.map.getBounds()};
      geocoder.geocode(request, function(results, status) {
        if (status === 'OK') {
          if (results.length > 0) {
            const result = results[0];
            geocodeCache.set(query, result);
            handleResult(result);
          }
        }
      });
    };
  
    // Set up geocoding on the search input.
    startButtonEl.addEventListener('click', function() {
      geocodeSearch(startInputEl.value.trim(), startButtonEl);
    });

    destButtonEl.addEventListener('click', function() {
        geocodeSearch(destInputEl.value.trim(), destButtonEl);
      });
  
    // Initialize Autocomplete.
    initializeSearchInputAutocomplete(
        locator, startInputEl, geocodeSearch, updateSearchLocation);
    initializeSearchInputAutocomplete(
        locator, destInputEl, geocodeSearch, updateSearchLocation);
  }

  /** Add Autocomplete to the search input. */
  function initializeSearchInputAutocomplete(
      locator, searchInputEl, fallbackSearch, searchLocationUpdater) {
    // Set up Autocomplete on the search input. Bias results to map viewport.
    const autocomplete = new google.maps.places.Autocomplete(searchInputEl, {
      types: ['geocode'],
      fields: ['place_id', 'formatted_address', 'geometry.location']
    });
    autocomplete.bindTo('bounds', locator.map);
    autocomplete.addListener('place_changed', function() {
      const placeResult = autocomplete.getPlace();
      if (!placeResult.geometry) {
        // Hitting 'Enter' without selecting a suggestion will result in a
        // placeResult with only the text input value as the 'name' field.
        fallbackSearch(placeResult.name);
        return;
      }
      searchLocationUpdater(
          placeResult.formatted_address, placeResult.geometry.location);
    });
  }

window.initMap = initMap;



  

  

