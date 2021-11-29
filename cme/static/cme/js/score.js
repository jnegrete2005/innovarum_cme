// Score display
var q_group = Array.from(document.getElementsByClassName('question-group'));
q_group.forEach(function (ol) {
    // The score for each block
    Array.from(ol.getElementsByClassName('radio')).forEach(function (el) {
        el.addEventListener('change', function (event) {
            var block_score = 0;
            Array.from(ol.getElementsByClassName('si')).forEach(function (yes) {
                // Check if it was checked
                if (yes.checked) {
                    block_score += 4;
                }
            });
            ol.querySelector('span.score').innerHTML = block_score.toString();
        });
    });
});
// Saving scores
// TODO: Make validation and error handling.
document.getElementById('survey').addEventListener('submit', function (event) { return saveScores(event); });
function saveScores(event) {
    event.preventDefault();
    var MODULE = window.location.pathname.split('/')[1];
    var TYPE = window.location.pathname.split('/')[2];
    var overall = 0;
    var scores = [];
    // Get the scores from all the blocks
    Array.from(document.getElementsByClassName('score')).forEach(function (score) {
        overall += parseInt(score.innerHTML);
        scores.push(parseInt(score.innerHTML));
    });
    fetch("/cme/" + MODULE + "/" + TYPE + "/graph/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ overall: overall, scores: scores }),
    })
        .then(function (response) {
        if (!response.ok)
            throw Error(response.statusText + " - " + response.status);
        return response.json();
    })
        .then(function (data) {
        // Display correct views
        document.getElementById('survey').style.display = 'none';
        var result = document.getElementById('result');
        result.style.display = 'flex';
        var ol = result.querySelector('ol');
        data.blocks.forEach(function (block, i) {
            // Block container
            var div = document.createElement('div');
            div.classList.add('block');
            // Block name
            var li = document.createElement('li');
            li.innerHTML = block + ':';
            // Block score
            var s1 = document.createElement('span');
            var s2 = document.createElement('span');
            s2.classList.add('block-score');
            s2.innerHTML = data.scores[i].toString();
            s1.append(s2, '/20');
            // Add to page
            div.append(li, s1);
            ol.append(div);
        });
        // Final score
        var div = document.createElement('div');
        div.id = 'final-container';
        // Span
        var s1 = document.createElement('span');
        // Final score text
        var h = document.createElement('h2');
        h.id = 'final-h2';
        var s2 = document.createElement('span');
        s2.id = 'final-score';
        s2.innerHTML = data.overall.toString();
        h.append('Tu calificación: ', s2, '/100');
        // Add all
        div.append(s1, h);
        ol.append(div);
        document.querySelector('title').innerHTML = 'Gráfico';
        /* Append to history */
        history.pushState({ graph: true }, '', './graph');
        createGraph(data.scores, data.blocks_for_graph, data.date, data.survey);
    })
        .catch(function (err) {
        alert(err);
    });
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function createGraph(scores, blocks, date, survey) {
    document.getElementById('results').innerHTML = survey;
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
    new Chart(document.getElementById('graph'), config);
}
window.addEventListener('popstate', function (event) {
    var _a;
    if ((_a = event === null || event === void 0 ? void 0 : event.state) === null || _a === void 0 ? void 0 : _a.graph) {
        showGraph();
        return;
    }
    showSurvey();
});
function showGraph() {
    document.getElementById('survey').style.display = 'none';
    document.getElementById('result').style.display = 'flex';
}
function showSurvey() {
    document.getElementById('survey').style.display = 'block';
    document.getElementById('result').style.display = 'none';
}
//# sourceMappingURL=score.js.map