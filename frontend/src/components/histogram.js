function createHistogramChart() {
    fetch('./hour_acc_hist.json')
      .then(response => response.json())
      .then(data => {
        const chartData = {
          labels: data.map(d => d.x),
          datasets: [{
            label: 'accident counts',
            backgroundColor: 'orange',
            data: data.map(d => d.y)
          }]
        };
        const chartConfig = {
          type: 'bar',
          data: chartData,
          options: {
            scales: {
              yAxes: [{
                ticks: {
                  beginAtZero: true
                }
              }]
            }
          }
        };
        const histogramChart = new Chart(document.getElementById('histogram'), chartConfig);
      });
  }
