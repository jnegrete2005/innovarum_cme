// Get score per block
let scores: Array<string> = [];
localStorage
	.getItem('scores')
	.split(',')
	.forEach((num) => {
		scores.push(num);
	});

// Get overall score
let overall = localStorage.getItem('overall');

Array.from(document.getElementsByClassName('block-score')).forEach((el: HTMLElement, i) => {
	el.innerHTML = scores[i];
});

document.getElementById('final-score').innerHTML = overall;
