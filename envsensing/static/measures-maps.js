var map;
var measures;
var markers = [];
var heatmap;
var $dimesion = $('#heatmap');

function initMap() {
  map = new google.maps.Map($('#map')[0], {
    center: {lat: 22.18, lng: 113.55}, zoom: 12
  });
  readyToGetDataset();
}

function drawHeatmap() {
  var dimesion = $dimesion.val();
  var heatMapData = [];
  measures.forEach(function(m) {
    var val;
    m.values.some(function(v) {
      if (v.type == dimesion) {
        val = v.value;
        return true;
      }
    });
    if (val == undefined)
      return;
    heatMapData.push(new google.maps.LatLng(m.latitude, m.longitude));
  });
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatMapData,
  });
  heatmap.setMap(map);
}

function drawMarkers() {
  markers = new Array(measures.length);
  measures.forEach(function(m, i) {
    markers[i] = new google.maps.Marker({
      position: { lat: m.latitude, lng: m.longitude },
      title: 'item #' + i
    });
    markers[i].addListener('click', function() {
      var content = new Date(m.timestamp * 1000) + '<br>';
      content += 'Lat: ' + m.latitude + ', lng: ' + m.longitude + '<br>';
      m.values.forEach(function(v) {
        content += v.type + ': ' + v.value + '<br>';
      });
      var infowindow = new google.maps.InfoWindow({
        content: content
      });
      infowindow.open(map, this);
    });
    markers[i].setMap(map);
  });
}

function drawMap() {
  if (markers)
    for (var i = 0; i < markers.length; i++)
      markers[i].setMap(null);
  if (heatmap)
    heatmap.setMap(null);

  if (!measures)
    return;

  console.log($dimesion.val());
  if ($dimesion.val())
    drawHeatmap();
  else
    drawMarkers();
}

onDatasetChanged(function(measures) {
  window.measures = measures;
  drawMap();
});

$('form#display-options').change(drawMap);

