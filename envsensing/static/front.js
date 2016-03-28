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

