var $show = $('button#show');

function readyToGetDataset() {
  $show.removeProp('disabled');
}

function onDatasetChanged(callback) {
  var $form = $('form#filter');
  var $device = $('select#device');
  var $dateFrom = $('input#date-from');
  var $dateTo = $('input#date-to');
  var $limit = $('input#limit');

  $show.click(function(event) {
    event.preventDefault();
    $show.prop('disabled', true);

    var url = '/api/devices/' + $device.val() + '/measures/';
    var args = { from: $dateFrom.val(), to: $dateTo.val(), limit: $limit.val() };
    $.getJSON(url, args, function(resp) {
      $show.removeProp('disabled');
      callback(resp.measures);
    });
  });
}
