// rfce - to fill boilerplate code for a new component
// npm start - use this command in terminal to view the front end in browser

import React from 'react';
import Map from './components/Map';
import OddComp from './components/odd_comp';
import UserInput from './components/UserInput';
import Graphs from './components/graphs';
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const titleStyle = {
    fontSize: '48px',
    fontWeight: 'bold',
    textAlign: 'center'
  };

  const subtitleStyle = {
    fontSize: '20px',
    textAlign: 'center',
    padding: '20px'
  };

  const mapStyle = {
    height: '100vh',
    width: '50%',
    float: 'left',
    padding: '20px'
  };

  const rightColumnStyle = {
    display: 'flex',
    flexDirection: 'column',
    width: '50%'
  }

  const componentStyle = {
    padding: '20px'
  }

  return (
    <div>
      <div style={titleStyle}>Stay Alive: Think and Drive</div>
      <div style={subtitleStyle}>Enter a starting and ending address within the state of Georgia. This tool only displays data for accidents on 
      major roads and highways.  </div>
      <div style={{ display: 'flex' }}>
        <div style={mapStyle}><Map /></div>
        <div style={rightColumnStyle}>
          <div style={componentStyle}><UserInput /></div>
          <div id = "graphs" style={componentStyle}><Graphs /></div>
          <div style={componentStyle}><OddComp /></div>
        </div>
      </div>
    </div>
  );
}

export default App;


 