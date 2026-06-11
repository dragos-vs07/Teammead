function logout_user()
{
     window.location.href ="/logout";
}
function redirect_to_doctor_page( doctor_id )
{
     window.location.href ="/find_doctor/" + doctor_id;
}

let xValues = consultations_list.map(c => {
  const d = new Date(c.consultation_date);
  return d.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
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
      borderColor: "#1565C0",
      backgroundColor: "rgba(21, 101, 192, 0.08)",
      fill: true,
      tension: 0.4,
      pointRadius: 3,
      pointHoverRadius: 5,
      pointBackgroundColor: "#1565C0",
    }]
  },
  options: {
    responsive: true,
    legend: {
      display: false
    },
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: false,
          maxTicksLimit: 4
        },
        gridLines: {
          display: false,
          drawBorder: false
        }
      }],
      xAxes: [{
        gridLines: {
          display: false,
          drawBorder: false
        }
      }]
    }
  }
});