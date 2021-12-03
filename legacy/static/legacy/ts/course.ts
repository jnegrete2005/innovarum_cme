import { getCookie, GRAPHQL_URL } from './index.js';

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
					id
					file
					video
					quiz {
						name
					}
				}
			}
		}
	}
`;

export function courseClick() {
	Array.from(document.getElementsByClassName('card')).forEach((card: HTMLAnchorElement) => {
		card.addEventListener('click', () => {
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
					alert(error.message);
				});
		});
	});
}

// Will fill the modal with the course info
function fillCourse(data: GetCourse) {
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
				module.trios.forEach((trio, i) => {
					createTrio(trio, `/media/${trio.file}`, trio.file.split('/')[2], '/static/legacy/icons/file.svg', ul);
					createTrio(trio, trio.video, trio.video, '/static/legacy/icons/play.svg', ul);
					createTrio(trio, '', 'Autoevaluación', '/static/legacy/icons/pencil.svg', ul);
				});
			}

			// Join everything
			li.append(mT, ul);
			ml.append(li);
		});
	}
}

function createTrio(trio, href: string, innerText: string, icon: string, ul: HTMLUListElement) {
	// Create li for trio
	const tLi = document.createElement('li');

	// Create the link
	const a = document.createElement('a');
	a.href = href;
	a.innerText = innerText;

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

	// Append the anchor tags to the li, and the li to the ul
	tLi.append(div, checkbox);
	ul.append(tLi);
}

function clearModal() {
	modal.style.display = 'none';
	document.getElementsByClassName('course-module-list')[0].innerHTML = null;
	document.getElementsByClassName('modal-title')[0].innerHTML = null;
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
	if (event.key == 'Escape' && event.target == modal) {
		clearModal();
	}
});
