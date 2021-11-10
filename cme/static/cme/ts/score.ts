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
