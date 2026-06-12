let xValues = consultations_list.map(c => {
  const d = new Date(c.consultation_date);
  return d.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
});

let yValues = consultations_list.map(c => c.weight)

const weight_canvas = document.getElementById("weight_chart");

new Chart(weight_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Weight",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

yValues = consultations_list.map(c => c.health_state)

const health_state_canvas = document.getElementById("health_state_chart");

new Chart(health_state_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Health state",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

yValues = consultations_list.map(c => c.blood_pressure_systolic)

const blood_pressure_systolic_canvas = document.getElementById("blood_pressure_systolic_chart");

new Chart(blood_pressure_systolic_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Blood pressure systolic",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

yValues = consultations_list.map(c => c.blood_pressure_diastolic)

const blood_pressure_diastolic_canvas = document.getElementById("blood_pressure_diastolic_chart");

new Chart(blood_pressure_diastolic_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Blood pressure diastolic",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

yValues = consultations_list.map(c => c.heart_rate)

const heart_rate_canvas = document.getElementById("heart_rate_chart");

new Chart(heart_rate_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Heart rate",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

yValues = consultations_list.map(c => c.heart_rate)

const blood_oxygen_saturation_canvas = document.getElementById("blood_oxygen_saturation_chart");

new Chart(blood_oxygen_saturation_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "SpO2",
      data: yValues,
      borderColor: "#30E4FF",
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});


