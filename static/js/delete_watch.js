$(document).ready(function() {
  var $deleteWatch = $('#delete_watch');

  $deleteWatch.on('click', function() {
    if(!confirm('Are you sure you want to delete this from your watchlist?'))
      return

    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: $deleteWatch.parent(),
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken
      }

    })
      .done(function() {
        $deleteWatch.parent().remove();
      })
      .fail(function(error) {
        console.log(error);
      });

    return false;
  });
});
