

/* helper */

function getMean(arr, field) {
    const values = arr.map(c => c[field]);
    return (values.reduce((sum, v) => sum + v, 0) / values.length).toFixed(2);
}

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
    }] ,
     {
        title : "Health State" ,
        shapes: [
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 9,
                y1: 10,
                fillcolor: 'rgba(0, 200, 7, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 7,
                y1: 9,
                fillcolor: 'rgba(222, 189, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 5,
                y1: 7,
                fillcolor: 'rgba(222, 130, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 3,
                y1: 5,
                fillcolor: 'rgba(222, 0, 0, 0.15)',  
                line: { width: 0 }
            }
            ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 0,
                y1: 3,
                fillcolor: 'rgba(10, 0, 0, 0.15)',  
                line: { width: 0 }
            }
        ]
     }
    
)

const weights = consultations_list.map(c => c.weight)

Plotly.newPlot( /* healthy zones should be implemented taking into account height and sex and activy , future idea */
    "weight_chart" ,
    [{
        x : consultation_dates,
        y : weights,
        type: "scatter" ,
        mode: "lines+markers",
        name: "Weight" 
    }] ,
     {
        title : "Weight"
     }
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
    }] ,
     {
        title : "Blood pressure systolic" ,
        shapes :[
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 90,
                y1: 120,
                fillcolor: 'rgba(0, 200, 7, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 120,
                y1: 130,
                fillcolor: 'rgba(200, 200, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 130,
                y1: 140,
                fillcolor: 'rgba(200, 100, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 140,
                y1: 200,
                fillcolor: 'rgba(200, 0, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 0,
                y1: 90,
                fillcolor: 'rgba(200, 0, 0, 0.15)',  
                line: { width: 0 }
            } ,
        ]
     }
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
    }] ,
     {
        title : "Blood pressure diastolic" ,
        shapes :[
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 60,
                y1: 80,
                fillcolor: 'rgba(0, 200, 7, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 80,
                y1: 90,
                fillcolor: 'rgba(200, 123, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 90,
                y1: 200,
                fillcolor: 'rgba(200, 27, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 0,
                y1: 60,
                fillcolor: 'rgba(200, 27, 0, 0.15)',  
                line: { width: 0 }
            } ,
            
        ]
     }
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
    }] ,
     {
        title : "Heart rate" ,
        shapes :[
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 60,
                y1: 70,
                fillcolor: 'rgba(0, 57, 4, 0.3)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 40,
                y1: 60,
                fillcolor: 'rgba(0, 200, 7, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 70,
                y1: 85,
                fillcolor: 'rgba(0, 200, 7, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 85,
                y1: 100,
                fillcolor: 'rgba(200, 197, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 100,
                y1: 200,
                fillcolor: 'rgba(220, 48, 1, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 0,
                y1: 40,
                fillcolor: 'rgba(220, 48, 1, 0.15)',  
                line: { width: 0 }
            } 
            
        ]
     }
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
    }] ,
     {
        title : "Blood oxygen saturation" ,
        shapes :[
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 94,
                y1: 100,
                fillcolor: 'rgba(0, 235, 16, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 92,
                y1: 94,
                fillcolor: 'rgba(193, 200, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 90,
                y1: 92,
                fillcolor: 'rgba(200, 147, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 60,
                y1: 90,
                fillcolor: 'rgba(200, 20, 0, 0.15)',  
                line: { width: 0 }
            } ,
            {
                type: 'rect',
                xref: 'paper',  // spans full chart width regardless of x-axis values
                yref: 'y',      // uses actual y-axis values
                x0: 0,
                x1: 1,
                y0: 0,
                y1: 60,
                fillcolor: 'rgba(10, 0, 0, 0.15)',  
                line: { width: 0 }
            } 
            
            
        ]
     }
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
        }

        /* updating charts */

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
                }] , 
                {
                    title: "Health State"
                }
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
                }] , 
                {
                    title: "Weight"
                }
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
                }] , 
                {
                    title: "Blood Pressure Systolic"
                }
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
                }] , 
                {
                    title: "Blood Pressure Diastolic"
                }
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
                }] , 
                {
                    title: "Health Rate"
                }
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
                }] , 
                {
                    title: "Blood Oxygen Saturation"
                }
            )
        /* updating min / max */

            document.getElementById("max_health_state").textContent = Math.max(...filtered.map(c => c.health_state));
            document.getElementById("max_weight").textContent = Math.max(...filtered.map(c => c.weight));
            document.getElementById("max_bps").textContent = Math.max(...filtered.map(c => c.blood_pressure_systolic));
            document.getElementById("max_bpd").textContent = Math.max(...filtered.map(c => c.blood_pressure_diastolic));
            document.getElementById("max_heart_rate").textContent = Math.max(...filtered.map(c => c.heart_rate));
            document.getElementById("max_spo2").textContent = Math.max(...filtered.map(c => c.blood_oxygen_saturation));

            document.getElementById("min_health_state").textContent = Math.min(...filtered.map(c => c.health_state));
            document.getElementById("min_weight").textContent = Math.min(...filtered.map(c => c.weight));
            document.getElementById("min_bps").textContent = Math.min(...filtered.map(c => c.blood_pressure_systolic));
            document.getElementById("min_bpd").textContent = Math.min(...filtered.map(c => c.blood_pressure_diastolic));
            document.getElementById("min_heart_rate").textContent = Math.min(...filtered.map(c => c.heart_rate));
            document.getElementById("min_spo2").textContent = Math.min(...filtered.map(c => c.blood_oxygen_saturation));

         /* updating mean */

            document.getElementById("mean_health_state").textContent = getMean(filtered, "health_state");
            document.getElementById("mean_weight").textContent = getMean(filtered, "weight");
            document.getElementById("mean_bps").textContent = getMean(filtered, "blood_pressure_systolic");
            document.getElementById("mean_bpd").textContent = getMean(filtered, "blood_pressure_diastolic");
            document.getElementById("mean_heart_rate").textContent = getMean(filtered, "heart_rate");
            document.getElementById("mean_spo2").textContent = getMean(filtered, "blood_oxygen_saturation");
})
