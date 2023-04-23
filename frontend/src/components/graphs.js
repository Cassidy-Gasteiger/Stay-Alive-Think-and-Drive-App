import React, { useState, useEffect } from 'react';
import RouteStatistics from './RouteStatistics';
import Histogram from './histogram';

function Graphs() {
  const containerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };

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
      {/* <div style={containerStyle}>
        <div id="num" style={{ marginRight: '50px' }}>
          <RouteStatistics />
      </div>
      </div> */}
      <div style={containerStyle}>
      <div id = "hist">
        <Histogram />
      </div>
    </div>
  </div>
  );
}

export default Graphs;
