export {};

// Add event listner to add
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
	if (el.parentElement.dataset.module === 'true') {
		addModule(el);

		const last_trio = document.getElementsByClassName('trio-container')[document.getElementsByClassName('trio-container').length - 1];

		// Get the last add el
		const last_add = last_trio.getElementsByClassName('add')[0];
		last_add.addEventListener('click', () => {
			add(<HTMLElement>last_add);
		});

		// Get last remove el
		const last_remove = last_trio.getElementsByClassName('remove')[0];
		last_remove.addEventListener('click', () => {
			remove(<HTMLElement>last_remove);
		});
	}

	// Case for answer
	else {
		addTrio(el);
	}
}

function addTrio(el: HTMLElement) {
	// Get the trio container
	const trio_container = el.parentElement.parentElement.parentElement;

	// Get the index of the module
	const i = parseInt(trio_container.parentElement.dataset.index);

	// Get the index of the last trio
	const j = parseInt((<HTMLElement>trio_container.children[trio_container.children.length - 1]).dataset.index);

	trio_container.insertAdjacentHTML(
		'beforeend',
		`<!-- Trio -->
		<div class="trio" data-index="${j + 1}">
			<!-- File -->
			<div class="form_group field">
				<input class="form_field" type="text" name="file-${i}" id="trio-${i}-${j + 1}-input" placeholder="Nombre del archivo" />
				<label class="form_label" for="trio-${i}-${j + 1}-input">Nombre del archivo</label>
			</div>

			<div class="form_group field">
				<input class="form_field" type="url" name="file-url-${i}" id="trio-${i}-${j + 1}-input" placeholder="URL del archivo" />
				<label class="form_label" for="trio-${i}-${j + 1}-input">URL del archivo</label>
			</div>

			<!-- Video -->
			<div class="form_group field">
				<input class="form_field" type="url" name="video-${i}" id="trio-${i}-${j + 1}-input" placeholder="Video" />
				<label class="form_label" for="trio-${i}-${j + 1}-input">Video</label>
			</div>

			<!-- Quiz -->
			<div class="form_group field">
				<input class="form_field" type="url" name="quiz-${i}" id="trio-${i}-${j + 1}-input" placeholder="Quiz" />
				<label class="form_label" for="trio-${i}-${j + 1}-input">Quiz</label>
			</div>
		</div>`
	);

	// Check (for validation) if there is more that 1 trio to remove .disabled
	if (trio_container.children.length > 2) trio_container.querySelector('span.remove').classList.remove('disabled');

	return;
}

function addModule(el: HTMLElement) {
	// Get the container
	const module_container = document.getElementsByClassName('modules')[0];

	// Get the last module to get it's index
	const last_module = module_container.getElementsByClassName('module')[module_container.getElementsByClassName('module').length - 1];
	const i = parseInt((<HTMLDivElement>last_module).dataset.index);

	// Append to it
	module_container.insertAdjacentHTML(
		'beforeend',
		`<div class="module" data-index="${i + 1}">
			<input type="text" class="readonly" name="module" value="Módulo ${i + 1}" placeholder="Módulo ${i + 1}" readonly disabled aria-readonly="true" />

			<!-- Trios -->
			<div class="trio-container">
				<div class="add-remove">
					<h4>Tríos</h4>
					<div>
						<span class="add">&plus;</span>
						<span class="remove disabled">&minus;</span>
					</div>
				</div>

				<!-- Trio -->
				<div class="trio" data-index="1">
					<!-- File -->
					<div class="form_group field">
						<input class="form_field" type="text" name="file-${i + 1}" id="trio-${i + 1}-1-input" placeholder="Nombre del archivo" />
						<label class="form_label" for="trio-${i + 1}-1-input">Nombre del archivo</label>
					</div>

					<div class="form_group field">
						<input class="form_field" type="url" name="file-url-1" id="trio-${i + 1}-1-input" placeholder="URL del archivo" />
						<label class="form_label" for="trio-${i + 1}-1-input">URL del archivo</label>
					</div>

					<!-- Video -->
					<div class="form_group field">
						<input class="form_field" type="url" name="video-${i + 1}" id="trio-${i + 1}-1-input" placeholder="Video" />
						<label class="form_label" for="trio-${i + 1}-1-input">Video</label>
					</div>

					<!-- Quiz -->
					<div class="form_group field">
						<input class="form_field" type="url" name="quiz-${i + 1}" id="trio-${i + 1}-1-input" placeholder="Quiz" />
						<label class="form_label" for="trio-${i + 1}-1-input">Quiz</label>
					</div>
				</div>
			</div>
		</div>`
	);

	if (module_container.children.length > 1) {
		el.nextElementSibling.classList.remove('disabled');
	}
	return;
}

function remove(el: HTMLElement) {
	// Check if disabled
	if (el.classList.contains('disabled')) return;

	// Case for module
	if (el.parentElement.dataset.module === 'true') return removeModule(el);

	// Case for trio
	removeTrio(el);
}

function removeModule(el: HTMLElement) {
	// Get last module
	let last_module: HTMLCollection | HTMLElement = document.getElementsByClassName('module');
	last_module = <HTMLElement>last_module[last_module.length - 1];

	// Remove it
	last_module.remove();

	// Check if there is only 1 question to add disabled to the remove btn
	if (document.getElementsByClassName('modules')[0].children.length <= 1) el.classList.add('disabled');

	return;
}

function removeTrio(el: HTMLElement) {
	// Get the trio container
	const trio_container = el.parentElement.parentElement.parentElement;

	// Get last trio
	const last_trio = trio_container.children[trio_container.children.length - 1];

	// Remove it
	last_trio.remove();

	// Check if there is only 1 trio to add disabled to the remove btn
	if (trio_container.children.length <= 2) el.classList.add('disabled');

	return;
}
