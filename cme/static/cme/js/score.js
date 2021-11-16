// Score display
const q_group = Array.from(document.getElementsByClassName('question-group'));
q_group.forEach((ol) => {
    // The score for each block
    Array.from(ol.getElementsByClassName('radio')).forEach((el) => {
        el.addEventListener('change', (event) => {
            let block_score = 0;
            Array.from(ol.getElementsByClassName('si')).forEach((yes) => {
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
document.getElementById('survey').addEventListener('submit', (event) => saveScores(event));
function saveScores(event) {
    event.preventDefault();
    const MODULE = window.location.pathname.split('/')[1];
    const TYPE = window.location.pathname.split('/')[2];
    let overall = 0;
    let scores = [];
    // Get the scores from all the blocks
    Array.from(document.getElementsByClassName('score')).forEach((score) => {
        overall += parseInt(score.innerHTML);
        scores.push(parseInt(score.innerHTML));
    });
    fetch(`/${MODULE}/${TYPE}/graph/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ overall, scores }),
    })
        .then((response) => {
        if (!response.ok)
            throw Error(`${response.statusText} - ${response.status}`);
        return response.json();
    })
        .then((data) => {
        // Display correct views
        document.getElementById('survey').style.display = 'none';
        const result = document.getElementById('result');
        result.style.display = 'flex';
        const ol = result.querySelector('ol');
        data.blocks.forEach((block, i) => {
            // Block container
            const div = document.createElement('div');
            div.classList.add('block');
            // Block name
            const li = document.createElement('li');
            li.innerHTML = block + ':';
            // Block score
            const s1 = document.createElement('span');
            const s2 = document.createElement('span');
            s2.classList.add('block-score');
            s2.innerHTML = data.scores[i].toString();
            s1.append(s2, '/20');
            // Add to page
            div.append(li, s1);
            ol.append(div);
        });
        // Final score
        const div = document.createElement('div');
        div.id = 'final-container';
        // Span
        const s1 = document.createElement('span');
        // Final score text
        const h = document.createElement('h2');
        h.id = 'final-h2';
        const s2 = document.createElement('span');
        s2.id = 'final-score';
        s2.innerHTML = data.overall.toString();
        h.append(s2, '/100');
        // Add all
        div.append(s1, h);
        ol.append(div);
        document.querySelector('title').innerHTML = 'Gráfico';
        /* Append to history */
        history.pushState(null, '', './graph');
        createGraph(data.scores, data.blocks, data.date, data.survey);
    })
        .catch((err) => {
        alert(err);
    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
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
    let labels = [];
    blocks.forEach((b, i) => {
        labels.push(`Bloque ${i}`);
    });
    const data = {
        labels: labels,
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
    const config = {
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
                    suggestedMin: 0,
                    suggestedMax: 20,
                },
            },
        },
    };
    // @ts-expect-error
    new Chart(document.getElementById('graph'), config);
}
//# sourceMappingURL=score.js.map