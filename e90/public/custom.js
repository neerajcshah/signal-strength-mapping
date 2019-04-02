var map, heatmap, overlay
USGSOverlay.prototype = new google.maps.OverlayView();

function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 39.906912, lng: -75.354920},
        scrollwheel: false,
        zoom: 18,
    });

   var heatmap = new google.maps.visualization.HeatmapLayer({
	    data: readJSON(),
	    map: map
    });

		var bounds = new google.maps.LatLngBounds(
				new google.maps.LatLng(39.902725, -75.349260),
				new google.maps.LatLng(39.908450, -75.35727));

    var srcImage = 'wifi_gps_data.json.phantom.1000.png'
		overlay = new USGSOverlay(bounds, srcImage, map);

}

/** @constructor */
function USGSOverlay(bounds, image, map) {

        // Initialize all properties.
        this.bounds_ = bounds;
        this.image_ = image;
        this.map_ = map;

        // Define a property to hold the image's div. We'll
        // actually create this div upon receipt of the onAdd()
        // method so we'll leave it null for now.
        this.div_ = null;

        // Explicitly call setMap on this overlay.

        try {
          this.setMap(map);
        }
        catch(err){
          alert(err)
        }
}

/**
 * onAdd is called when the map's panes are ready and the overlay has been
 * added to the map.
 */
USGSOverlay.prototype.onAdd = function() {

    alert("here!")
		var div = document.createElement('div');
		div.style.borderStyle = 'none';
		div.style.borderWidth = '0px';
		div.style.position = 'absolute';

		// Create the img element and attach it to the div.
		var img = document.createElement('img');
		img.src = this.image_;
		img.style.width = '100%';
		img.style.height = '100%';
		img.style.position = 'absolute';
		div.appendChild(img);

		this.div_ = div;

		// Add the element to the "overlayLayer" pane.
		var panes = this.getPanes();
		panes.overlayLayer.appendChild(div);
};

USGSOverlay.prototype.draw = function() {

		// We use the south-west and north-east
		// coordinates of the overlay to peg it to the correct position and size.
		// To do this, we need to retrieve the projection from the overlay.
		var overlayProjection = this.getProjection();

		// Retrieve the south-west and north-east coordinates of this overlay
		// in LatLngs and convert them to pixel coordinates.
		// We'll use these coordinates to resize the div.
		var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
		var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());

		// Resize the image's div to fit the indicated dimensions.
		var div = this.div_;
		div.style.left = sw.x + 'px';
		div.style.top = ne.y + 'px';
		div.style.width = (ne.x - sw.x) + 'px';
		div.style.height = (sw.y - ne.y) + 'px';
};

	// The onRemove() method will be called automatically from the API if
	// we ever set the overlay's map property to 'null'.
USGSOverlay.prototype.onRemove = function() {
	this.div_.parentNode.removeChild(this.div_);
	this.div_ = null;
};



function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

function getPoints(data) {

  var heatMapData = [];
  for (var i=0; i<data.length; i++) {
    var max = -1000;
    for (var j=0; j<data[i]['wifi'].length; j++) {
      if (parseFloat(data[i]['wifi'][j]['DBM']) > max && data[i]['wifi'][j]['SSID'] == 'eduroam') {

        max = parseFloat(data[i]['wifi'][j]['DBM']);

      }
    }

    max = Math.pow(10,max/10) //Convert to mW
    heatMapData[i] = {location: new google.maps.LatLng(data[i]['Latitude'],data[i]['Longitude'])};
  }
  return heatMapData;
}

function readJSON() {
  var pts;

  $.ajax({
    url: 'wifi_gps_data.json',
    dataType: 'json',
    async: false,
    success: function(json){
      pts = getPoints(json['JsonData'])
  }});
  return pts;
}

google.maps.event.addDomListener(window, 'load', initMap);
