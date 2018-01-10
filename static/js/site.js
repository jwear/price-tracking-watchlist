$(document).ready(function() {
  var $exception = $('#exception');

  $exception.on('submit', function(event) {
    event.preventDefault()

    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: '/watch/create',
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: $(this).serialize()
    })
      .done(function(data) {
        $.ajax({
          url: data.detail_url,
          method: 'GET',
        })
        .done(function() {
          window.location.href = data.detail_url
        })
        .fail(function() {
          alert('Product not found!')
        })
      })
      .fail(function() {
        alert('Invalid URL');
      });

    return false;
  });
});
