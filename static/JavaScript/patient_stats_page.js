
/* helper */

function getMean(arr, field) {
    const values = arr.map(c => c[field]).filter(v => v !== null && v !== '' && v !== undefined);
    if (values.length === 0) return "N/A";
    return (values.reduce((sum, v) => sum + v, 0) / values.length).toFixed(2);
}

/* color helper - returns the color matching the chart band for a given value */

function getColorForValue(value, thresholds) {
    for (const t of thresholds) {
        if (value >= t.min) return t.color;
    }
    return thresholds[thresholds.length - 1].color;
}

/* color thresholds matching each chart's shapes */

const healthStateThresholds = [
    { min: 9, color: 'rgb(0, 200, 7)' },
    { min: 7, color: 'rgb(222, 189, 0)' },
    { min: 5, color: 'rgb(222, 130, 0)' },
    { min: 3, color: 'rgb(222, 0, 0)' },
    { min: 0, color: 'rgb(10, 0, 0)' }
];

const bpsThresholds = [
    { min: 140, color: 'rgb(200, 0, 0)' },
    { min: 130, color: 'rgb(200, 100, 0)' },
    { min: 120, color: 'rgb(200, 200, 0)' },
    { min: 90,  color: 'rgb(0, 200, 7)' },
    { min: 0,   color: 'rgb(200, 0, 0)' }
];

const bpdThresholds = [
    { min: 90, color: 'rgb(200, 27, 0)' },
    { min: 80, color: 'rgb(200, 123, 0)' },
    { min: 60, color: 'rgb(0, 200, 7)' },
    { min: 0,  color: 'rgb(200, 27, 0)' }
];

const heartRateThresholds = [
    { min: 100, color: 'rgb(220, 48, 1)' },
    { min: 85,  color: 'rgb(200, 197, 0)' },
    { min: 70,  color: 'rgb(0, 200, 7)' },
    { min: 60,  color: 'rgb(0, 57, 4)' },
    { min: 40,  color: 'rgb(0, 200, 7)' },
    { min: 0,   color: 'rgb(220, 48, 1)' }
];

const spo2Thresholds = [
    { min: 94, color: 'rgb(0, 235, 16)' },
    { min: 92, color: 'rgb(193, 200, 0)' },
    { min: 90, color: 'rgb(200, 147, 0)' },
    { min: 60, color: 'rgb(200, 20, 0)' },
    { min: 0,  color: 'rgb(10, 0, 0)' }
];

/* shared field config */

const statFields = [
    { key: "health_state", thresholds: healthStateThresholds },
    { key: "weight",       thresholds: null },
    { key: "blood_pressure_systolic",  thresholds: bpsThresholds },
    { key: "blood_pressure_diastolic", thresholds: bpdThresholds },
    { key: "heart_rate",   thresholds: heartRateThresholds },
    { key: "blood_oxygen_saturation",  thresholds: spo2Thresholds }
];

const idSuffix = {
    health_state: "health_state",
    weight: "weight",
    blood_pressure_systolic: "blood_pressure_systolic",
    blood_pressure_diastolic: "blood_pressure_diastolic",
    heart_rate: "heart_rate",
    blood_oxygen_saturation: "blood_oxygen_saturation"
};

const unitSuffix = {
    health_state: " " ,
    weight: " kg" ,
    blood_pressure_systolic: " mm/Hg" ,
    blood_pressure_diastolic: " mm/Hg" ,
    heart_rate : " BPM" ,
    blood_oxygen_saturation : " %"
};

/* updates the max/min/mean cards (values + colors) for a given dataset */

function updateStats(data) {
    statFields.forEach(({ key, thresholds }) => {
        const suffix = idSuffix[key];
        const values = data.map(c => c[key]).filter(v => v !== null && v !== '' && v !== undefined);

        const maxEl = document.getElementById(`max_${suffix}`);
        const minEl = document.getElementById(`min_${suffix}`);
        const meanEl = document.getElementById(`mean_${suffix}`);

        if (values.length === 0) {
            maxEl.textContent = "N/A";
            minEl.textContent = "N/A";
            meanEl.textContent = "N/A";
            if (thresholds) {
                maxEl.style.color = "";
                minEl.style.color = "";
                meanEl.style.color = "";
            }
            return;
        }

        const maxVal = Math.max(...values);
        const minVal = Math.min(...values);
        const meanVal = Math.round(getMean(data, key));
        const unit = unitSuffix[key];

        maxEl.textContent = maxVal + unit;
        minEl.textContent = minVal + unit;
        meanEl.textContent = meanVal + unit;

        if (thresholds) {
            maxEl.style.color = getColorForValue(maxVal, thresholds);
            minEl.style.color = getColorForValue(minVal, thresholds);
            meanEl.style.color = getColorForValue(meanVal, thresholds);
        }
    });
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
        yaxis: {
            title: "score"
        } ,
        shapes: [
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 9, y1: 10,
                fillcolor: 'rgba(0, 200, 7, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 7, y1: 9,
                fillcolor: 'rgba(222, 189, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 5, y1: 7,
                fillcolor: 'rgba(222, 130, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 3, y1: 5,
                fillcolor: 'rgba(222, 0, 0, 0.15)', line: { width: 0 }
            },
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 0, y1: 3,
                fillcolor: 'rgba(10, 0, 0, 0.15)', line: { width: 0 }
            }
        ]
     }
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
    }] ,
     {
        title : "Weight" ,
        yaxis: {
            ticksuffix: " kg"
        }
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
        yaxis: {
            ticksuffix: " mm/Hg"
        } ,
        shapes :[
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 90, y1: 120,
                fillcolor: 'rgba(0, 200, 7, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 120, y1: 130,
                fillcolor: 'rgba(200, 200, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 130, y1: 140,
                fillcolor: 'rgba(200, 100, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 140, y1: 200,
                fillcolor: 'rgba(200, 0, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 0, y1: 90,
                fillcolor: 'rgba(200, 0, 0, 0.15)', line: { width: 0 }
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
        yaxis: {
            ticksuffix: " mm/Hg"
        } ,
        shapes :[
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 60, y1: 80,
                fillcolor: 'rgba(0, 200, 7, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 80, y1: 90,
                fillcolor: 'rgba(200, 123, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 90, y1: 200,
                fillcolor: 'rgba(200, 27, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 0, y1: 60,
                fillcolor: 'rgba(200, 27, 0, 0.15)', line: { width: 0 }
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
        yaxis: {
            ticksuffix: " bpm"
        } ,
        shapes :[
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 60, y1: 70,
                fillcolor: 'rgba(0, 57, 4, 0.3)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 40, y1: 60,
                fillcolor: 'rgba(0, 200, 7, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 70, y1: 85,
                fillcolor: 'rgba(0, 200, 7, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 85, y1: 100,
                fillcolor: 'rgba(200, 197, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 100, y1: 200,
                fillcolor: 'rgba(220, 48, 1, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 0, y1: 40,
                fillcolor: 'rgba(220, 48, 1, 0.15)', line: { width: 0 }
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
        yaxis: {
            ticksuffix: " %" 
        } ,
        shapes :[
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 94, y1: 100,
                fillcolor: 'rgba(0, 235, 16, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 92, y1: 94,
                fillcolor: 'rgba(193, 200, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 90, y1: 92,
                fillcolor: 'rgba(200, 147, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 60, y1: 90,
                fillcolor: 'rgba(200, 20, 0, 0.15)', line: { width: 0 }
            } ,
            {
                type: 'rect', xref: 'paper', yref: 'y',
                x0: 0, x1: 1, y0: 0, y1: 60,
                fillcolor: 'rgba(10, 0, 0, 0.15)', line: { width: 0 }
            } 
        ]
     }
)

/* apply stats on initial page load */
updateStats(consultations_list);

/* APPLY FILTERS ON TIME RANGE */

const FilterButton = document.getElementById("timerange")

FilterButton.addEventListener(
    "change" ,
    function(){

        console.log("filter changed", FilterButton.value);

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
                { title: "Health State" }
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
                { title: "Weight" }
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
                { title: "Blood Pressure Systolic" }
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
                { title: "Blood Pressure Diastolic" }
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
                { title: "Health Rate" }
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
                { title: "Blood Oxygen Saturation" }
            )

        /* updating min / max / mean values + colors */
        updateStats(filtered);
})