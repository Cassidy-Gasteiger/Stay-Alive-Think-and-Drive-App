// rfce - to fill boilerplate code for a new component
// npm start - use this command in terminal to view the front end in browser

import React from 'react';
import Map from './components/Map';
import OddComp from './components/odd_comp';
import UserInput from './components/UserInput';
import Graphs from './components/graphs';

function App() {
  const titleStyle = {
    fontSize: '48px',
    fontWeight: 'bold',
    textAlign: 'center'
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
      <div style={{ display: 'flex' }}>
        <div style={mapStyle}><Map /></div>
        <div style={rightColumnStyle}>
          <div style={componentStyle}><UserInput /></div>
          <div style={componentStyle}><Graphs /></div>
          <div style={componentStyle}><OddComp /></div>
        </div>
      </div>
    </div>
  );
}

export default App;


 