$(document).ready(function() {
  var $addWatch = $('#add_watch');

  $addWatch.on('click', function(event) {

    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: window.location.href,
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .done(function() {
        var $deleteButton = $('<button/>', {
        id: 'delete_watch',
        text: 'Delete'
      })
        $(event.target).before($deleteButton);
        $(event.target).remove();
      })
      .fail(function(error) {
      });

    return false;
  });
});
