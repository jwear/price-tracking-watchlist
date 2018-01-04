$(document).ready(function() {
  Date.prototype.formatMMDDYYYY = function() {
    return (this.getMonth() + 1) +
    "/" +  this.getDate() +
    "/" +  this.getFullYear();
  }

  var jsonUrl = 'http://localhost:8000/watch/'+ $('#product').attr('data-item-id') +'/json';
  console.log(jsonUrl);

  var jsonData = $.ajax({
    url: jsonUrl,
    dataType: 'json',
  }).done(function (results) {
    // console.log(results)
    var labels = [], data=[];
    // for price in results:
    results.forEach(function(price) {
      labels.push(new Date(price.changed).formatMMDDYYYY());
      data.push(parseFloat(price.price));
    });

    console.log(labels, data)

    var priceData = {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Item Price',
          data: data,
          borderColor: '#3e95cd',
          fill: false
        },
      ]
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Item Price History'
      },
      scales: {
          xAxes: [{
              time: {
                  unit: 'day'
              }
          }]
      }
    }
  };

  var ctx = document.getElementById("myChart").getContext("2d");

  var myLineChart = new Chart(ctx, priceData);

}).fail(function(err) {
  throw err
})
});
