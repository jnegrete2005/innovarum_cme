// Add event listener to add
Array.from(document.getElementsByClassName('add')).forEach((el) => {
	el.addEventListener('click', () => {
		add(<HTMLElement>el);
	});
});

// Add event listener to remove
Array.from(document.getElementsByClassName('remove')).forEach((el) => {
	el.addEventListener('click', () => {
		remove(<HTMLElement>el);
	});
});

function add(el: HTMLElement) {
	// Case for question
	if (el.parentElement.dataset.question === 'true') {
		addQuestion(el);
	} else {
		// Case for answer
		addAnswer(el);
	}

	Array.from(document.getElementsByClassName('answer-container')).forEach((el) => {
		// Add event listener to all .add inside .answer-container
		Array.from(el.getElementsByClassName('add')).forEach((el: HTMLElement) => {
			el.addEventListener('click', () => {
				add(el);
			});
		});

		// Add event listener to all .remove inside .answer-container
		Array.from(el.getElementsByClassName('remove')).forEach((el: HTMLElement) => {
			el.addEventListener('click', () => {
				remove(el);
			});
		});
	});

	return;
}

function addAnswer(el: HTMLElement) {
	// Get the index of the question
	const i = parseInt(el.parentElement.parentElement.parentElement.parentElement.dataset.index);

	// Get the answer container
	const answer_container = el.parentElement.parentElement.parentElement;

	// Get the index of the answer
	const j = parseInt((<HTMLElement>answer_container.children[answer_container.children.length - 1]).dataset.index);

	answer_container.innerHTML += `
    <div class="form_group field answer" data-index="${j + 1}">
      <input type="radio" name="answer${i}" />
      <div>
        <input class="form_field" type="text" name="answer${i}" id="answer-${i}-${j + 1}-Input" placeholder="Respuesta ${j + 1}" />
        <label class="form_label" for="answer-${i}-${j + 1}-Input">Respuesta ${j + 1}</label>
      </div>
    </div>
  `;

	// Check (for validation) if there is more that 1 answer to remove .disabled
	if (answer_container.children.length > 2) {
		answer_container.querySelector('span.remove').classList.remove('disabled');
	}

	return;
}

function addQuestion(el: HTMLElement) {
	// Get the container
	const question_container = document.getElementsByClassName('questions')[0];

	// Get the last question to get it's index
	const last_question = question_container.getElementsByClassName('question')[question_container.getElementsByClassName('question').length - 1];
	const i = parseInt((<HTMLDivElement>last_question).dataset.index);

	// Append to it
	question_container.innerHTML += `
		<div class="question" data-index="${i + 1}">
			<h3>Pregunta ${i + 1}</h3>
			<div class="form_group field">
				<input class="form_field" type="text" name="question" id="question${i + 1}Input" placeholder="Pregunta ${i + 1}" />
				<label class="form_label" for="question${i + 1}Input">Pregunta ${i + 1}</label>
			</div>

			<!-- Answers -->
			<div class="answer-container">
				<div class="add-remove">
					<h4>Respuestas</h4>
					<div>
						<span class="add">&plus;</span>
						<span class="remove disabled">&minus;</span>
					</div>
				</div>
				<div class="form_group field answer" data-index="1">
					<input type="radio" name="answer${i + 1}" />
					<div>
						<input class="form_field" type="text" name="answer${i + 1}" id="answer-${i + 1}-1-Input" placeholder="Respuesta 1" />
						<label class="form_label" for="answer-${i + 1}-1-Input">Respuesta 1</label>
					</div>
				</div>
			</div>
		</div>
  `;

	if (question_container.children.length > 1) {
		el.nextElementSibling.classList.remove('disabled');
	}
	return;
}

function remove(el: HTMLElement) {
	// Check if disabled
	if (el.classList.contains('disabled')) return;

	// Case for question
	if (el.parentElement.dataset.question === 'true') return removeQuestion(el);

	// Case for answer
	removeAnswer(el);
}

function removeAnswer(el: HTMLElement) {
	// Get answer container
	const answer_container = el.parentElement.parentElement.parentElement;

	// Get last answer
	const last_answer = answer_container.children[answer_container.children.length - 1];

	// Remove answer
	last_answer.remove();

	// Check if there is only 1 answer to add disabled to the remove btn
	if (answer_container.children.length <= 2) {
		el.classList.add('disabled');
	}

	return;
}

function removeQuestion(el: HTMLElement) {
	// Get last question
	let last_question: HTMLCollection | HTMLElement = document.getElementsByClassName('question');
	last_question = <HTMLElement>last_question[last_question.length - 1];

	// Remove it
	last_question.remove();

	// Check if there is only 1 question to add disabled to the remove btn
	if (document.getElementsByClassName('questions')[0].children.length <= 1) {
		el.classList.add('disabled');
	}

	return;
}
