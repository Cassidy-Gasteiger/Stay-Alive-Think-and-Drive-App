import React, {useState } from 'react'

function UserInput() {
  // create two state variables and two setter functions to update their values
  const [startingLocation, setStartingLocation] = useState('');
  const [destination, setDestination] = useState('');

  // two event handlers - user these to update state variables whenever corresponding input fields change
  const handleStartingLocationChange = (event) => {
    setStartingLocation(event.target.value);
  };

  const handleDestinationChange = (event) => {
    setDestination(event.target.value);
  };

  const UserInputStyle = {
    backgroundColor: 'lightgray',
    height: '25vh',
    width: '100%',
    padding: '20px'
  };

  const inputContainerStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginBottom: '20px'
  };

  const inputLabelStyle = {
    fontWeight: 'bold',
    marginBottom: '5px'
  };

  // use the two state variables as the values of the starting location and destination fields
  return (
    <div style={UserInputStyle}>
      <div style={inputContainerStyle}>
        <label htmlFor="startingLocation" style={inputLabelStyle}>Starting Location:</label>
        <input type="text" id="startingLocation" value={startingLocation} onChange={handleStartingLocationChange} /> 
      </div>
      <div style={inputContainerStyle}>
        <label htmlFor="destination" style={inputLabelStyle}>Destination:</label>
        <input type="text" id="destination" value={destination} onChange={handleDestinationChange} />
      </div>
    </div>
  )
}

export default UserInput;
