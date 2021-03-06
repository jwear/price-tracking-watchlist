$(document).ready(function() {
  var $deleteWatch = $('#delete_watch');

  $deleteWatch.on('click', function(event) {

    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: window.location.href,
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .done(function() {
        var $watchButton = $('<button/>', {
          id: 'add_watch',
          text: 'Watch'
        })
        $(event.target).before($watchButton);
        $(event.target).remove();
      })
      .fail(function(error) {
      });

    return false;
  });
});
