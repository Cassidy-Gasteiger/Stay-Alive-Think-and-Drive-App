import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';

function Histogram() {
  const chartRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [totalAccidents, setTotalAccidents] = useState(null);
  console.log("Inside Histogram func");

  useEffect(() => {
    fetch('./hour_acc_hist.json'
    ,{
      headers : { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
       }
    })
      .then(response => response.json())
      .then(data => {
        console.log(123);
        setLoading(false);
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
        const histogramChart = new Chart(chartRef.current, chartConfig);
        const total = data.reduce((acc, curr) => acc + curr.y, 0);
        setTotalAccidents(total);
        console.log("histogram total",total);
        return () => {
          histogramChart.destroy();
        };
      })
      .catch(error => {
        setLoading(false);
        setError(true);
        console.log("inside error");
        console.log(error);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error loading data.</div>;
  }

  return (
  <div>
    <div id="histogram_return1">
      <h1>Histogram of Accidents</h1>
      <canvas ref={chartRef} id="Histogram"></canvas>
    </div>
    <div id="histogram_return2">
      <h1>Total number of Accidents</h1>
      <p style={{ fontSize: '36px' }}>{totalAccidents}</p>
    </div>
  </div>
  );
}

export default Histogram;
