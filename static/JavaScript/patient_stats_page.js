/* helper */

function getMean(arr, field) {
    const values = arr.map(c => c[field]).filter(v => v !== null && v !== '' && v !== undefined);
    if (values.length === 0) return "N/A";
    return (values.reduce((sum, v) => sum + v, 0) / values.length).toFixed(2);
}

function getColorForValue(value, thresholds) {
    for (const t of thresholds) {
        if (value >= t.min) return t.color;
    }
    return thresholds[thresholds.length - 1].color;
}

/* thresholds */

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

/* layouts — defined once, reused in both newPlot and react */

const LAYOUTS = {
    health_state_chart: {
        title: "Health State",
        yaxis: { title: "score" },
        shapes: [
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 9,  y1: 10,  fillcolor: 'rgba(0, 200, 7, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 7,  y1: 9,   fillcolor: 'rgba(222, 189, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 5,  y1: 7,   fillcolor: 'rgba(222, 130, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 3,  y1: 5,   fillcolor: 'rgba(222, 0, 0, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 0,  y1: 3,   fillcolor: 'rgba(10, 0, 0, 0.15)',    line: { width: 0 } }
        ]
    },
    weight_chart: {
        title: "Weight",
        yaxis: { ticksuffix: " kg" }
    },
    blood_pressure_systolic_chart: {
        title: "Blood Pressure Systolic",
        yaxis: { ticksuffix: " mm/Hg" },
        shapes: [
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 90,  y1: 120, fillcolor: 'rgba(0, 200, 7, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 120, y1: 130, fillcolor: 'rgba(200, 200, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 130, y1: 140, fillcolor: 'rgba(200, 100, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 140, y1: 200, fillcolor: 'rgba(200, 0, 0, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 0,   y1: 90,  fillcolor: 'rgba(200, 0, 0, 0.15)',   line: { width: 0 } }
        ]
    },
    blood_pressure_diastolic_chart: {
        title: "Blood Pressure Diastolic",
        yaxis: { ticksuffix: " mm/Hg" },
        shapes: [
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 60, y1: 80,  fillcolor: 'rgba(0, 200, 7, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 80, y1: 90,  fillcolor: 'rgba(200, 123, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 90, y1: 200, fillcolor: 'rgba(200, 27, 0, 0.15)',  line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 0,  y1: 60,  fillcolor: 'rgba(200, 27, 0, 0.15)',  line: { width: 0 } }
        ]
    },
    heart_rate_chart: {
        title: "Heart Rate",
        yaxis: { ticksuffix: " bpm" },
        shapes: [
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 60,  y1: 70,  fillcolor: 'rgba(0, 57, 4, 0.3)',     line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 40,  y1: 60,  fillcolor: 'rgba(0, 200, 7, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 70,  y1: 85,  fillcolor: 'rgba(0, 200, 7, 0.15)',   line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 85,  y1: 100, fillcolor: 'rgba(200, 197, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 100, y1: 200, fillcolor: 'rgba(220, 48, 1, 0.15)',  line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 0,   y1: 40,  fillcolor: 'rgba(220, 48, 1, 0.15)',  line: { width: 0 } }
        ]
    },
    blood_oxygen_saturation_chart: {
        title: "Blood Oxygen Saturation",
        yaxis: { ticksuffix: " %" },
        shapes: [
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 94, y1: 100, fillcolor: 'rgba(0, 235, 16, 0.15)',  line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 92, y1: 94,  fillcolor: 'rgba(193, 200, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 90, y1: 92,  fillcolor: 'rgba(200, 147, 0, 0.15)', line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 60, y1: 90,  fillcolor: 'rgba(200, 20, 0, 0.15)',  line: { width: 0 } },
            { type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: 0,  y1: 60,  fillcolor: 'rgba(10, 0, 0, 0.15)',   line: { width: 0 } }
        ]
    }
};

/* field config */

const statFields = [
    { key: "health_state",             thresholds: healthStateThresholds },
    { key: "weight",                   thresholds: null },
    { key: "blood_pressure_systolic",  thresholds: bpsThresholds },
    { key: "blood_pressure_diastolic", thresholds: bpdThresholds },
    { key: "heart_rate",               thresholds: heartRateThresholds },
    { key: "blood_oxygen_saturation",  thresholds: spo2Thresholds }
];

const unitSuffix = {
    health_state:             " ",
    weight:                   " kg",
    blood_pressure_systolic:  " mm/Hg",
    blood_pressure_diastolic: " mm/Hg",
    heart_rate:               " BPM",
    blood_oxygen_saturation:  " %"
};

/* updateStats */

function updateStats(data) {
    statFields.forEach(({ key, thresholds }) => {
        const values = data.map(c => c[key]).filter(v => v !== null && v !== '' && v !== undefined);

        const maxEl  = document.getElementById(`max_${key}`);
        const minEl  = document.getElementById(`min_${key}`);
        const meanEl = document.getElementById(`mean_${key}`);

        if (values.length === 0) {
            maxEl.textContent = minEl.textContent = meanEl.textContent = "N/A";
            if (thresholds) maxEl.style.color = minEl.style.color = meanEl.style.color = "";
            return;
        }

        const maxVal  = Math.max(...values);
        const minVal  = Math.min(...values);
        const meanVal = Math.round(getMean(data, key));
        const unit    = unitSuffix[key];

        maxEl.textContent  = maxVal  + unit;
        minEl.textContent  = minVal  + unit;
        meanEl.textContent = meanVal + unit;

        if (thresholds) {
            maxEl.style.color  = getColorForValue(maxVal,  thresholds);
            minEl.style.color  = getColorForValue(minVal,  thresholds);
            meanEl.style.color = getColorForValue(meanVal, thresholds);
        }
    });
}

/* chart render helper — same call for both init and filter update */

function renderCharts(data) {

    const dates = data.map(c => {
        const d = new Date(c.consultation_date);
        return d.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
    });

    const fields = [
        { id: "health_state_chart",             field: "health_state" },
        { id: "weight_chart",                   field: "weight" },
        { id: "blood_pressure_systolic_chart",  field: "blood_pressure_systolic" },
        { id: "blood_pressure_diastolic_chart", field: "blood_pressure_diastolic" },
        { id: "heart_rate_chart",               field: "heart_rate" },
        { id: "blood_oxygen_saturation_chart",  field: "blood_oxygen_saturation" }
    ];

    fields.forEach(({ id, field }) => {
        Plotly.react(
            id,
            [{ x: dates, y: data.map(c => c[field]), type: "scatter", mode: "lines+markers", name: field }],
            LAYOUTS[id]
        );
    });
}

/* initial render */

renderCharts(consultations_list);
updateStats(consultations_list);

/* filter */

document.getElementById("timerange").addEventListener("change", function () {

    const days = parseInt(this.value);
    let filtered;

    if (days === -1) {
        filtered = consultations_list;
    } else {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - days);
        filtered = consultations_list.filter(c => new Date(c.consultation_date) >= cutoff);
    }

    renderCharts(filtered);
    updateStats(filtered);
});