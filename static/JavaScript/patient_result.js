const consultation_dates = consultations_list.map(c => {
  const d = new Date(c.consultation_date);
  return d.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
});

const health_states = consultations_list.map(c => c.health_state)

Plotly.newPlot(
    "health_state_chart" ,
    [{
        x : consultation_dates,
        y : health_states,
        type: "scatter" ,
        mode: "lines+markers",
        name: "HealthState" 
    }]
)

const weights = consultations_list.map(c => c.weight)

Plotly.newPlot(
    "weight_chart" ,
    [{
        x : consultation_dates,
        y : weights,
        type: "scatter" ,
        mode: "lines+markers",
        name: "Weight" 
    }]
)