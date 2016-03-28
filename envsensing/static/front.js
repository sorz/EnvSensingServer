function initializeNavbar() {

  // Active item correspond to current visiting page on navbar.

  var PATH_REGEX_TO_NAME = {
    '^/users/login/': 'login',
    '^/users/': 'users',
    '^/measures/': 'measures',
    '^/analysis/': 'analysis',
    '^/$': 'home'
  };

  var path = window.location.pathname;
  for (var pathRegex in PATH_REGEX_TO_NAME) {
    if (path.match(pathRegex)) {
      $('li.nav-' + PATH_REGEX_TO_NAME[pathRegex]).addClass('active');
      break;
    }
  }
}


$(document).ready(function() {
  initializeNavbar();

});

var SENSOR_NAMES = ['Temperature', 'Humidity', 'Pressure',
    'Monoxide', 'OxidizingGas', 'ReducingGas'];

var MONTH_NAMES = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.',
    'Jul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];

function formatDatetime(date) {
  var d = date.getDate();
  var m = MONTH_NAMES[date.getMonth()];
  var y = date.getFullYear();
  var H = date.getHours();
  var M = date.getMinutes();
  return d + ' ' + m + ' ' + y + ' ' + H + ':' + M;
}

function formatLatLng(v) {
  return v.lat().toFixed(6) + ' lat, ' + v.lng().toFixed(6) + ' lng';
}
