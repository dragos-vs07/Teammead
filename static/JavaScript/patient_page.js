
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
     [{   /* data */
          x: consultation_dates ,
          y: health_states ,
          type: "scatter" ,
          mode: "lines+markers",
          name: "Weight" ,
          line:{
               shape: "spline" ,
               smoothing: 1.3 ,
               width: 3 ,
               color: "#4FA1FF"
          } , 
          fill: "tozeroy" ,
          fillcolor: "rgba(143,221,255,0.2)"
     }] ,
     {
          xaxis : {
               showgrid: false
          } ,

          yaxis : {
               showgrid: false ,
               dtick: 2 ,
          }
     }
)