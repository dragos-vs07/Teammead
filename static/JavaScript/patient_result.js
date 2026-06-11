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