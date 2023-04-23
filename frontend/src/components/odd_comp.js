import sunny_img from "./sunny.png";
import thunder_img from "./thunder.png";
import React, { useEffect, useRef, useState } from 'react';

function odds_component(props) {
  const { odds_good, odds_bad } = props;
  console.log(`Good Odds: ${odds_good}`);
  console.log(`Bad Odds: ${odds_bad}`);

  return (
    <div>
      <h1 style={{ fontWeight: 'bold' }}>Odds of Accident</h1>
      {/* <h2>*Likelihood of being involved in an accident basis the current weather and average historical weather seen at your location. </h2> */}
      <span class="odds_description">
        Accidents might be influenced by a multitude of factors, including human mistakes, bad driving conditions and inclement weather. To capture this effect, we provide the measure of "Odds", which represents the likelihood of being involved in an accident basis the real-time weather and average historical weather at your location.
      </span>
      <div>
        <span> </span>
        <h3 style={{ color: "#4da270", fontSize: '25px' }}>Current Weather Odds</h3>
        <span> Represents how good or bad the current weather is compared to the average historical weather.</span>
        <img src={sunny_img} alt="" style={{ width: "7%", height: "auto" }} />
        <p style={{ fontSize: '16px' }}> Current weather Odds = {odds_good} </p>
      </div>
      <div>
        <h3 style={{ color: "#a24d58", fontSize: '25px'}}>Bad Weather Odds</h3>
        <span> Represents how much worse can the weather be compared to the average historical weather.</span>
        <img src={thunder_img} alt="" style={{ width: "7%", height: "auto" }} />
        <p style={{ fontSize: '16px' }}> Odds for bad weather = {odds_bad} </p>
      </div>
    </div>
  );
}

function odds_component_param(WrappedComponent,o1,o2) {
  return function (props) {
    const [odds1, set_odds1] = useState(null);
    const [odds2, set_odds2] = useState(null);
useEffect(() => {
  fetch('logOdds_output.json')
    .then(response => response.json())
    .then(data => {
      set_odds1(data.odds1);
      set_odds2(data.odds2);
    })
    .catch(error => console.error(error));
  }, []);
  // console.log("odds check",odds);
  console.log("odds check1",odds1);
  console.log("odds check2",odds2);
    return <WrappedComponent {...props} odds_good={odds1} odds_bad={odds2} />;
  };
}



export default odds_component_param(odds_component);
