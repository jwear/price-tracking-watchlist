var ctx = document.getElementById("myChart").getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [1, 2, 3, 4, 5, 6, 7, 8],
        datasets: [{
            label: 'Item Price',
            data: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            borderColor: '#3e95cd',
            fill: false
          },
        ]
      },
      options: {
        title: {
          display: true,
          text: 'Item Price History'
        }
      }
    });
