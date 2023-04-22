import sunny_img from "./sunny.png";
import thunder_img from "./thunder.png";

function odds_component(props) {
  const { odds_good, odds_bad } = props;
  console.log(`Good Odds: ${odds_good}`);
  console.log(`Bad Odds: ${odds_bad}`);

  return (
    <div>
      <h1 style={{ fontWeight: 'bold' }}>Odds of Accident</h1>
      {/* <h2>*Likelihood of being involved in an accident basis the current weather and average historical weather seen at your location. </h2> */}
      <span class="odds_description">
        The Odds number represent the likelihood of being involved in an accident basis the realtime weather and average historical weather seen at your location.
      </span>
      <div>
        <span> </span>
        <h3 style={{ color: "#4da270" }}>Current Odds</h3>
        <img src={sunny_img} alt="" style={{ width: "7%", height: "auto" }} />
        <p> Odds estimated using your current weather = {odds_good} </p>
      </div>
      <div>
        <h3 style={{ color: "#a24d58" }}>Bad Odds</h3>
        <img src={thunder_img} alt="" style={{ width: "7%", height: "auto" }} />
        <p> Odds estimation in worst scenerio = {odds_bad} </p>
      </div>
    </div>
  );
}

function odds_component_param(WrappedComponent, o1, o2) {
  return function (props) {
    return <WrappedComponent {...props} odds_good={o1} odds_bad={o2} />;
  };
}

export default odds_component_param(odds_component, "1.1", "1.2");
