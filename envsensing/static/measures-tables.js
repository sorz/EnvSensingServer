google.load("visualization", "1.1", {packages:["table"]});
google.setOnLoadCallback(function() {
  readyToGetDataset();
});

onDatasetChanged(function(measures) {
  var table = new google.visualization.Table($('#table')[0]);
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Time');
  data.addColumn('number', 'Latitude');
  data.addColumn('number', 'Longitude');
  data.addColumn('number', 'Accuracy (m)');
  data.addColumn('number', 'Temperature (K)');
  data.addColumn('number', 'Humidity (%)');
  data.addColumn('number', 'Pressure (Pa)');
  data.addColumn('number', 'Monoxide (ppm)');
  data.addColumn('number', 'Oxidizing Gas (Ohm)');
  data.addColumn('number', 'Reducing Gas (Ohm)');

  data.addRows(measures.length);
  for (var i=0; i<measures.length; ++i) {
    var m = measures[i];
    var time = new Date(m.timestamp * 1000);
    data.setCell(i, 0, time);
    data.setCell(i, 1, m.latitude);
    data.setCell(i, 2, m.longitude);
    data.setCell(i, 3, m.accuracy);

    for (var j=0; j<m.values.length; ++j) {
      var column = 4 + SENSOR_NAMES.indexOf(m.values[j].type);
      data.setCell(i, column, m.values[j].value);
    }
  }

  var formatter = new google.visualization.NumberFormat({pattern: '#.#'});
  for (var i=3; i<10; i++)
    formatter.format(data, i);

  table.draw(data, {page: 'enable', pageSize: 30,
    sortColumn: 0, sortAscending: false});
});
