var map;
var mc;  // MarkerClusterer
var measures;
var updateTimer;
var dataBounds;

var $map = $('#map');
var $dateFrom = $('input#date-from');
var $dateTo = $('input#date-to');
var $btnCluster = $('#btn-cluster');
var $btnClustered = $('#btn-clustered');
var $clusterInfo = $('#cluster-info');

google.load('visualization', '1.1', { packages: ['corechart'] });

function initMap() {
  map = new google.maps.Map($('#map')[0], {
    center: {lat: 22.18, lng: 113.55}, zoom: 12
  });
  mc = new MarkerClusterer(map, [], {zoomOnClick: false});

  map.addListener('bounds_changed', function() {
    window.clearTimeout(updateTimer);
    updateTimer = window.setTimeout(function() {
      var bounds = map.getBounds();
      if (dataBounds)
        if (dataBounds.contains(bounds.getNorthEast()) &&
            dataBounds.contains(bounds.getSouthWest()))
          return;
      updatePoints();
      dataBounds = bounds;
    }, 3000);
  });

  google.maps.event.addListener(mc, 'clusterclick', displayCluster);
}

function updatePoints() {
  var url = 'area/';
  var args = map.getBounds().toJSON();
  args.from = $dateFrom.val();
  args.to = $dateTo.val();

  $map.loading();
  $.getJSON(url, args, function(resp) {
    console.log(resp.count + ' points loaded.');
    measures = resp.points;
    drawMarkers();
  }).always(function() {
    $map.loading('stop');
  });
}

function drawMarkers() {
  mc.clearMarkers();
  markers = new Array(measures.length);
  measures.forEach(function(m, i) {
    markers[i] = new google.maps.Marker({
      position: { lat: m.latitude, lng: m.longitude },
      title: 'item #' + i
    });
    markers[i].id = i;
    mc.addMarker(markers[i]);
  });
}


function drawLineCharts(points) {
  points.sort(function(a, b) { return a.timestamp - b.timestamp; });

  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Temperature (°C)');
  data.addColumn('number', 'Humidity (%)');
  data.addColumn('number', 'Pressure (hPa)');
  data.addColumn('number', 'Monoxide (ppm)');
  data.addColumn('number', 'Oxidizing Gas (ohm)');
  data.addColumn('number', 'Reducing Gas (ohm)');
  data.addRows(points.map(function(p) {
    var col = new Array(7);
    col[0] = new Date(p.timestamp * 1000);
    p.values.forEach(function(v) {
      if (v.type == 'Temperature')
        col[1] = v.value - 273.15;
      else if (v.type == 'Humidity')
        col[2] = v.value;
      else if (v.type == 'Pressure')
        col[3] = v.value / 100;
      else if (v.type == 'Monoxide')
        col[4] = Math.max(0.0, v.value);
      else if (v.type == 'OxidizingGas')
        col[5] = v.value;
      else if (v.type == 'ReducingGas')
        col[6] = v.value;
    });
    return col;
  }));

  var options = {pointSize: 4, width: 850, height: 450, curveType: 'function'}
  var lineIds = ['temp', 'humi', 'pres', 'mono', 'oxid', 'redu'];
  var lines = new Array(6);
  lineIds.forEach(function(id, i) {
    lines[i] = new google.visualization.LineChart($('#line-' + id)[0]);
    var view = new google.visualization.DataView(data);
    view.setColumns([0, i+1]);
    lines[i].draw(view, options);
  });
}


function displayCluster(cluster) {
  var points = new Array(cluster.getMarkers().length);
  cluster.getMarkers().forEach(function(m, i) {
    points[i] = measures[m.id];
  });

  var timestamps = points.map(function(p) { return p.timestamp; });
  var timeMin = Math.min.apply(null, timestamps);
  var timeMax = Math.max.apply(null, timestamps);

  $('#c-coordinate').text(formatLatLng(cluster.getCenter()));
  $('#c-count').text(cluster.getSize());
  $('#c-date-from').text(formatDatetime(new Date(timeMin * 1000)));
  $('#c-date-to').text(formatDatetime(new Date(timeMax * 1000)));

  drawLineCharts(points);

  // Clustering.
  $btnCluster.show();
  $btnClustered.hide();
  $clusterInfo.hide();
  $btnCluster.unbind('click');
  $btnCluster.click(function() {
    var keys = new Array(points.length);
    points.forEach(function(p, i) {
      keys[i] = [p.deviceId, p.timestamp];
    });

    $btnCluster.attr('disabled', '');
    $.ajax('cluster/', {
      data: JSON.stringify(keys),
      contentType: 'application/json',
      type: 'POST'
    }).done(function(result) {
      // result: { score: ..., groups: [[...], [...]]}
      $('#c-score').text(result.score.toFixed(4));
      $('#c-g1-count').text(result.groups[0].length);
      $('#c-g2-count').text(result.groups[1].length);
      $clusterInfo.show();

      var $btns = $btnClustered.children('.btn');
      $btnCluster.hide();
      $btnClustered.show();
      $btns.unbind('click')
        .click(function() {
          if (this.id == 'btn-mixed')
            drawLineCharts(points);
          else if (this.id == 'btn-group-1')
            drawLineCharts(result.groups[0]);
          else if (this.id == 'btn-group-2')
            drawLineCharts(result.groups[1]);
          $btns.removeClass('active');
          $(this).addClass('active');
          $btnClustered.children('')
        });
      $btns.removeClass('active');
      $('#btn-mixed').addClass('active');
    }).always(function() {
      $btnCluster.removeAttr('disabled');
    });

  });

  $('#cluster-modal').modal('show');
}

$('#update').click(function(event) {
  event.preventDefault();
  updatePoints();
});
