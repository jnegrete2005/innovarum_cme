// Get scores
var scores = JSON.parse(document.getElementById('scores').textContent);
// Get blocks
var blocks = [];
Array.from(document.querySelector('ol').querySelectorAll('li')).forEach(function (el) {
    blocks.push(el.innerHTML);
});
// Get date
var date = JSON.parse(document.getElementById('dates').textContent);
// Get survey name
var survey = document.getElementById('results').innerHTML;
// Draw graph
createGraphGet(scores, date, survey);
// Function to create graph
function createGraphGet(scores, dates, survey) {
    document.getElementById('results').innerHTML = survey;
    var blocks = JSON.parse(document.getElementById('blocks_for_graph').textContent);
    // Create datasets
    var datasets = [];
    scores.forEach(function (score, i) {
        var current_color = '#' + Math.floor(Math.random() * 16777215).toString(16);
        datasets.push({
            label: dates[i],
            data: score,
            fill: true,
            backgroundColor: current_color + "33",
            hoverBackgroundColor: "darken(" + current_color + "33, 5%)",
            borderColor: current_color,
            pointBackgroundColor: current_color,
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: current_color,
        });
    });
    var data = {
        labels: blocks,
        datasets: datasets,
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