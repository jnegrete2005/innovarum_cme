import { displayError, getCookie, GRAPHQL_URL, USER_ID } from './index.js';
import { updateUsertrio } from './trios.js';

import type { GetCourse } from './graphql';

const modal = document.getElementById('modal');
const span = document.getElementsByClassName('close')[0];
const query = `
	query GetCourse($id: ID!) {
		course(id: $id) {
			id
			name
			modules {
				trios {
					usertrioSet {
						user {
							id
						}
						done
					}
					id
					file
					fileUrl
					video
					quiz
				}
			}
		}
	}
`;

export function courseClick() {
	Array.from(document.getElementsByClassName('card')).forEach((card: HTMLAnchorElement) => {
		card.addEventListener('click', () => {
			// If not logged in, put an error
			try {
				JSON.parse(document.getElementById('user_id').textContent);
			} catch {
				return displayError('Error de sesión', 'Inicie sesión para acceder a los cursos.');
			}

			// When the user clicks on the button, open the modal
			modal.style.display = 'block';

			// Get the course's ID
			const id = parseInt(card.dataset.id);

			// Fetch
			fetch(GRAPHQL_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json',
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify({ query, variables: { id } }),
				credentials: 'include',
			})
				.then((response) => {
					if (!response.ok) throw Error(`${response.statusText} - ${response.status}`);
					return response.json();
				})
				.then((data: GetCourse) => {
					fillCourse(data);
				})
				.catch((error: Error) => {
					displayError('Error', error.message);
				});
		});
	});
}

// Will fill the modal with the course info
function fillCourse(data: GetCourse) {
	modal.dataset.id = data.data.course.id;

	// Get the modal
	const mBody = modal.getElementsByClassName('modal-body')[0];

	// Get modal title
	const title = document.getElementById('modal-title');
	title.innerText = data.data.course.name;

	// Create ul for modules
	const ml = <HTMLUListElement>mBody.getElementsByClassName('course-module-list')[0];

	// Create modules
	if (data.data.course.modules) {
		data.data.course.modules.forEach((module, i) => {
			// Create li for module
			const li = document.createElement('li');

			// Create module heading
			const mT = document.createElement('h2');
			mT.innerText = `Módulo ${i + 1}`;

			// If trios, create them
			// Create ul for trios
			const ul = document.createElement('ul');
			ul.classList.add('trios');
			if (module.trios) {
				module.trios.reverse();

				module.trios.forEach((trio) => {
					const quiz_url = trio.quiz ? trio.quiz : '#';

					// Get trio
					const template_trio = [
						createTrio(trio, trio.fileUrl, trio.file, '/static/legacy/icons/file.svg', 0),
						createTrio(trio, trio.video, trio.video, '/static/legacy/icons/play.svg', 1),
						createTrio(trio, quiz_url, 'Autoevaluación', '/static/legacy/icons/pencil.svg', 2, true),
					];

					// Create a wrapper div for trio
					const wrapper_trio = document.createElement('div');
					wrapper_trio.ariaRoleDescription = 'Wrap a trio';
					wrapper_trio.dataset.id = trio.id;
					wrapper_trio.append(...template_trio);

					// Append wrapper
					ul.append(wrapper_trio);
				});
			}

			// Join everything
			li.append(mT, ul);
			ml.append(li);
		});
	}

	updateUsertrio();
}

function createTrio(trio: Trio, href: string, innerText: string, icon: string, i: number, new_tab = false) {
	// Create li for trio
	const tLi = document.createElement('li');

	// Create the link
	const a = document.createElement('a');
	a.href = href;
	a.innerText = innerText;
	a.target = new_tab ? '_blank' : a.target;

	// Create icon
	const svg = document.createElement('img');
	svg.src = icon;
	svg.alt = 'Ícono';
	svg.setAttribute('aria-details', 'By fontawesome. https://fontawesome.com/license');

	// Create wrapper for icon and link
	const div = document.createElement('div');
	div.append(svg, a);

	// Create the checkbox
	const checkbox = document.createElement('input');
	checkbox.type = 'checkbox';
	checkbox.name = trio.id;

	// Check the checkbox
	checkbox.checked = check(trio, i);

	// Append the anchor tags to the li, and the li to the ul
	tLi.append(div, checkbox);
	return tLi;
}

function check(trio: Trio, i: number) {
	let answer = false;

	trio.usertrioSet.forEach((usertrio) => {
		if (parseInt(usertrio?.user.id) === USER_ID) {
			answer = usertrio.done[i];
			return;
		}
	});

	return answer;
}

export function clearModal() {
	modal.style.display = 'none';

	// Try closing from a course
	try {
		// Get the progress bar value from the checkboxes
		let val = 0;
		Array.from(modal.querySelectorAll('li')).forEach((el) => {
			if ((<HTMLInputElement>el.lastElementChild).checked) {
				val++;
			}
		});

		// Find the course it closed from
		Array.from(document.querySelectorAll('a.card')).forEach((card: HTMLAnchorElement) => {
			if (card.dataset.id === modal.dataset.id) {
				card.querySelector('progress').value = val;
			}
		});

		modal.dataset.id = null;
	} catch {}

	const m_body = <HTMLElement>document.getElementsByClassName('modal-body')[0];
	m_body.innerHTML = null;
	m_body.insertAdjacentHTML('beforeend', '<ul class="course-module-list"></ul>');

	document.getElementById('modal-title').innerHTML = null;
	return;
}

// When the user clicks on <span> (x), close the modal
span.addEventListener('click', () => {
	clearModal();
});

// When the user clicks anywhere outside of the modal, close it
window.addEventListener('click', (event) => {
	if (event.target == modal) {
		clearModal();
	}
});

// When the user clicks esc, close the modal
window.addEventListener('keydown', (event) => {
	if (event.key == 'Escape' && modal.style.display == 'block') {
		clearModal();
	}
});

type Trio = {
	usertrioSet:
		| null
		| {
				user: {
					id: string;
				};
				done: [boolean, boolean, boolean];
		  }[];
	id: string;
	file: string;
	video: string;
	quiz: null | string;
};
