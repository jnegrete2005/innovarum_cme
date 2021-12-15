// Get scores
const scores: Array<Array<number>> = JSON.parse(document.getElementById('scores').textContent);

// Get blocks
let blocks: Array<string> = [];
Array.from(document.querySelector('ol').querySelectorAll('li')).forEach((el) => {
	blocks.push(el.innerHTML);
});

// Get date
const date: Array<string> = JSON.parse(document.getElementById('dates').textContent);

// Get survey name
const survey = document.getElementById('results').innerHTML;

// Draw graph
createGraphGet(scores, date, survey);

// Function to create graph
function createGraphGet(scores: Array<Array<number>>, dates: Array<string>, survey: string) {
	document.getElementById('results').innerHTML = survey;

	const blocks = JSON.parse(document.getElementById('blocks_for_graph').textContent);

	// Create datasets
	let datasets: Array<object> = [];
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
