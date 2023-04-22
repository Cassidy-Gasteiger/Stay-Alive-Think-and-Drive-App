import React, { useState, useEffect } from 'react';
import RouteStatistics from './RouteStatistics';
// import { BarChart, DensityChart } from './charts';

function Graphs() {
  const titleStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: '20px'
  };

  const numberStyle = {
    fontSize: '48px',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: '20px'
  };

  return (
    <div>
      <h1 style={titleStyle}>Route Statistics</h1>
      <div>
        <RouteStatistics />
      </div>
    </div>
  );
}

export default Graphs;
