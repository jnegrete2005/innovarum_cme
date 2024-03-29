// Score display
const q_group = Array.from(document.getElementsByClassName('question-group'));
q_group.forEach((ol: HTMLOListElement) => {
	// The score for each block
	Array.from(ol.getElementsByClassName('radio')).forEach((el: HTMLInputElement) => {
		el.addEventListener('change', (event: Event) => {
			let block_score = 0;
			Array.from(ol.getElementsByClassName('si')).forEach((yes: HTMLInputElement) => {
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

function saveScores(event: Event) {
	event.preventDefault();

	const MODULE = window.location.pathname.split('/')[2];
	const TYPE = window.location.pathname.split('/')[3];
	let overall = 0;
	let scores: Array<number> = [];

	// Get the scores from all the blocks
	Array.from(document.getElementsByClassName('score')).forEach((score: HTMLSpanElement) => {
		overall += parseInt(score.innerHTML);
		scores.push(parseInt(score.innerHTML));
	});

	fetch(`/cme/${MODULE}/${TYPE}/graph/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: JSON.stringify({ overall, scores }),
	})
		.then((response) => {
			if (!response.ok) throw Error(`${response.statusText} - ${response.status}`);
			return response.json();
		})
		.then((data: Data) => {
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
				s2.innerHTML = data.scores[data.scores.length - 1][i].toString();
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
			h.append('Tu calificación: ', s2, '/100');

			// Add all
			div.append(s1, h);
			ol.append(div);

			document.querySelector('title').innerHTML = 'Gráfico';

			/* Append to history */
			history.pushState({ graph: true }, '', './graph');

			createGraph(data.scores, data.blocks_for_graph, data.dates, data.survey);
		})
		.catch((err: Error) => {
			alert(err);
		});
}

function getCookie(name: string): string {
	let cookieValue: null | string = null;

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

function createGraph(scores: Array<Array<number>>, blocks: string, dates: Array<string>, survey: string) {
	document.getElementById('results').innerHTML = survey;

	let datasets = [];
	scores.forEach((score, i) => {
		const current_color = '#' + Math.floor(Math.random() * 16777215).toString(16);

		datasets.push({
			label: dates[i],
			data: score,
			fill: true,
			backgroundColor: `${current_color}33`,
			hoverBackgroundColor: `darken(${current_color}33, 5%)`,
			borderColor: current_color,
			pointBackgroundColor: current_color,
			pointBorderColor: '#fff',
			pointHoverBackgroundColor: '#fff',
			pointHoverBorderColor: current_color,
		});
	});

	const data = {
		labels: blocks,
		datasets: datasets,
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

window.addEventListener('popstate', (event) => {
	if (event?.state?.graph) {
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

type Data = {
	blocks: Array<string>;
	scores: Array<Array<number>>;
	overall: number;
	dates: Array<string>;
	survey: string;
	blocks_for_graph: string;
};
