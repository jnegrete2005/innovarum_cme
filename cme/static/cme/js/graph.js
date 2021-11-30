// Get scores
var scores = [];
Array.from(document.getElementsByClassName('block-score')).forEach(function (el) {
    try {
        scores.push(parseInt(el.innerHTML));
    }
    catch (TypeError) {
        alert('Ha ocurrido un error.');
    }
});
// Get blocks
var blocks = [];
Array.from(document.querySelector('ol').querySelectorAll('li')).forEach(function (el) {
    blocks.push(el.innerHTML);
});
// Get date
var date = document.getElementById('date').innerHTML;
// Get survey name
var survey = document.getElementById('results').innerHTML;
// Draw graph
createGraphGet(scores, date, survey);
// Function to create graph
function createGraphGet(scores, date, survey) {
    document.getElementById('results').innerHTML = survey;
    var blocks_graph = document.getElementById('blocks_for_graph').innerHTML.replace(/'/gi, '"');
    blocks = JSON.parse(blocks_graph);
    var data = {
        labels: blocks,
        datasets: [
            {
                label: date,
                data: scores,
                fill: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                hoverBackgroundColor: 'darken(#ff638433, 5%)',
                borderColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(255, 99, 132)',
            },
        ],
    };
    var config = {
        type: 'radar',
        data: data,
        options: {
            elements: {
                line: {
                    borderWidth: 3,
                },
            },
            scales: {
                r: {
                    min: 0,
                    max: 20,
                    ticks: { stepSize: 4 },
                    pointLabels: {
                        font: {
                            size: 14,
                        },
                    },
                },
            },
        },
    };
    // @ts-expect-error
    Chart.defaults.font.size = 16;
    // @ts-expect-error
    new Chart(document.getElementById('graph'), config);
}
//# sourceMappingURL=graph.js.map