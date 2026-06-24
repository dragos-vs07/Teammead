const MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
];

const TODAY = new Date();


// ================= FILTER =================

function getFiltered(days) {

    if (days === -1)
        return consultations_list;


    const cutoff = new Date();

    cutoff.setDate(
        cutoff.getDate() - days
    );


    return consultations_list.filter(
        c => new Date(c.consultation_date) >= cutoff
    );
}



// ================= DIAGNOSTICS CHART =================

function buildDiagnosticChart(filtered) {

    let diagnostic_frequency = {};


    for (const c of filtered) {

        diagnostic_frequency[c.diagnostic] =
            (diagnostic_frequency[c.diagnostic] || 0) + 1;
    }


    let diagnostic_array = Object.entries(diagnostic_frequency)
        .map(([diagnostic, freq]) => ({
            diagnostic,
            freq
        }));


    diagnostic_array.sort(
        (a, b) => b.freq - a.freq
    );


    let top10 = diagnostic_array.slice(0, 10);


    Plotly.react(
        "diagnose_chart",
        [
            {
                x: top10.map(d => d.diagnostic),
                y: top10.map(d => d.freq),
                type: "bar"
            }
        ],
        {
            title: "Number of diagnostics",
            yaxis: {
                dtick: 1
            }
        }
    );
}



// ================= CONSULTATIONS CHART =================

function buildConsultationsChart(filtered, days) {

    let x;
    let y;


    // ALL TIME or large ranges -> months

    if (days === -1 || days >= 60) {

        const monthCount =
            days === -1 ? 12 : Math.ceil(days / 30);


        let labels = [];
        let counts = [];


        for (let i = monthCount - 1; i >= 0; i--) {

            const d = new Date(
                TODAY.getFullYear(),
                TODAY.getMonth() - i,
                1
            );


            labels.push(
                MONTHS[d.getMonth()] +
                " " +
                d.getFullYear()
            );


            counts.push(
                filtered.filter(c => {

                    const cd = new Date(
                        c.consultation_date
                    );


                    return (
                        cd.getFullYear() === d.getFullYear() &&
                        cd.getMonth() === d.getMonth()
                    );

                }).length
            );
        }


        x = labels;
        y = counts;

    }


    // SMALL RANGES -> days

    else {

        let labels = [];
        let counts = [];


        for (let i = days - 1; i >= 0; i--) {

            const d = new Date(TODAY);

            d.setDate(
                TODAY.getDate() - i
            );


            labels.push(
                d.getDate() +
                " " +
                MONTHS[d.getMonth()]
            );


            counts.push(
                filtered.filter(c => {

                    const cd = new Date(
                        c.consultation_date
                    );


                    return (
                        cd.getFullYear() === d.getFullYear() &&
                        cd.getMonth() === d.getMonth() &&
                        cd.getDate() === d.getDate()
                    );

                }).length
            );
        }


        x = labels;
        y = counts;
    }



    Plotly.react(
        "consultations_chart",
        [
            {
                x,
                y,
                type: "bar"
            }
        ],
        {
            title: "Number of consultations",
            yaxis: {
                dtick: 1
            }
        }
    );
}



// ================= INITIAL LOAD =================


buildConsultationsChart(
    consultations_list,
    -1
);


buildDiagnosticChart(
    consultations_list
);




// ================= EVENT LISTENERS =================


const ConsultFilterButton =
    document.getElementById(
        "timerange_consultations_chart"
    );


const DiagnoseFilterButton =
    document.getElementById(
        "timerange_diagnose_chart"
    );



// consultations filter

ConsultFilterButton.addEventListener(
    "change",
    function() {

        const days = parseInt(
            this.value
        );


        const filtered =
            getFiltered(days);


        buildConsultationsChart(
            filtered,
            days
        );
    }
);



// diagnostics filter

DiagnoseFilterButton.addEventListener(
    "change",
    function() {

        const days = parseInt(
            this.value
        );


        const filtered =
            getFiltered(days);


        buildDiagnosticChart(
            filtered
        );
    }
);