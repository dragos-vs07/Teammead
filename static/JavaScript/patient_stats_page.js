

/* INITIALISE CHARTS */

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

const bps = consultations_list.map(c => c.blood_pressure_systolic)

Plotly.newPlot(
    "blood_pressure_systolic_chart" ,
    [{
        x : consultation_dates,
        y : bps,
        type: "scatter" ,
        mode: "lines+markers",
        name: "BPS" 
    }]
)

const bpd = consultations_list.map(c => c.blood_pressure_diastolic)

Plotly.newPlot(
    "blood_pressure_diastolic_chart" ,
    [{
        x : consultation_dates,
        y : bpd,
        type: "scatter" ,
        mode: "lines+markers",
        name: "BPD" 
    }]
)

const heart_rates = consultations_list.map(c => c.heart_rate)

Plotly.newPlot(
    "heart_rate_chart" ,
    [{
        x : consultation_dates,
        y : heart_rates,
        type: "scatter" ,
        mode: "lines+markers",
        name: "HeartRate" 
    }]
)

const SpO2s = consultations_list.map(c => c.blood_oxygen_saturation)

Plotly.newPlot(
    "blood_oxygen_saturation_chart" ,
    [{
        x : consultation_dates,
        y : SpO2s,
        type: "scatter" ,
        mode: "lines+markers",
        name: "SpO2" 
    }]
)

/* APPLY FILTERS ON TIME RANGE */

const FilterButton = document.getElementById("timerange")

FilterButton.addEventListener(
    "change" ,
    function(){

        console.log("filter changed", FilterButton.value);  // add this

        const cutoff = new Date();
        const days = FilterButton.value;
        let filtered;

        if( days === "-1" )
            filtered = consultations_list;
        else
        {
            
            if( days === "365" ) cutoff.setDate(cutoff.getDate() - 365);
            if( days === "180" ) cutoff.setDate(cutoff.getDate() - 180);
            if( days === "90" ) cutoff.setDate(cutoff.getDate() - 90);
            if( days === "30" ) cutoff.setDate(cutoff.getDate() - 30);
            if( days === "7" ) cutoff.setDate(cutoff.getDate() - 7);

            filtered = consultations_list.filter(c => new Date(c.consultation_date) >= cutoff);

            const new_consultation_dates = filtered.map(c => {
                const d = new Date(c.consultation_date);
                return d.toLocaleDateString('en-GB', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                });
            });
    
            const health_states = filtered.map(c => c.health_state)

            Plotly.react(
                "health_state_chart" ,
                [{
                    x : new_consultation_dates,
                    y : health_states,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "HealthState" 
                }]
            )

            const weights = filtered.map(c => c.weight)

            Plotly.react(
                "weight_chart" ,
                [{
                    x : new_consultation_dates,
                    y : weights,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "Weight" 
                }]
            )

            const bps = filtered.map(c => c.blood_pressure_systolic)

            Plotly.react(
                "blood_pressure_systolic_chart" ,
                [{
                    x : new_consultation_dates,
                    y : bps,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "BPS" 
                }]
            )

            const bpd = filtered.map(c => c.blood_pressure_diastolic)

            Plotly.react(
                "blood_pressure_diastolic_chart" ,
                [{
                    x : new_consultation_dates,
                    y : bpd,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "BPD" 
                }]
            )

            const heart_rates = filtered.map(c => c.heart_rate)

            Plotly.react(
                "heart_rate_chart" ,
                [{
                    x : new_consultation_dates,
                    y : heart_rates,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "HeartRate" 
                }]
            )

            const SpO2s = filtered.map(c => c.blood_oxygen_saturation)

            Plotly.react(
                "blood_oxygen_saturation_chart" ,
                [{
                    x : new_consultation_dates,
                    y : SpO2s,
                    type: "scatter" ,
                    mode: "lines+markers",
                    name: "SpO2" 
                }]
            )
        }

})
