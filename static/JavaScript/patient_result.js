let xValues = consultations_list.map(c => c.consultation_date)
let yValues = consultations_list.map(c => c.weight)

const weight_canvas = document.getElementById("weight_chart");

new Chart(weight_canvas, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      label: "Weight",
      data: yValues,
      borderColor: "red",
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
      borderColor: "red",
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