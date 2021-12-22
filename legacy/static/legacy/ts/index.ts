import { clearModal, courseClick } from './course.js';

import type { GetUserTriosCourses, courseModes } from './graphql';

export const GRAPHQL_URL = '/graphql';

const MEDIA_URL = '/static/legacy/media/';
const COURSE_URL = MEDIA_URL + 'courses/';
export const CLASS_URL = MEDIA_URL + 'classes/';

export let USER_ID: number | null;

async function getCourses(option: keyof courseModes) {
	// Create the query and body
	let query: string;
	let body: BodyInit;

	try {
		USER_ID = JSON.parse(document.getElementById('user_id').textContent);
	} catch {
		USER_ID = null;
	}

	if ((window.location.href.split('/')[4] === '#done' || window.location.href.split('/')[4] === '#ongoing') && option === 'initial')
		option = <keyof courseModes>window.location.href.split('/')[4].replace('#', '');

	if (option === 'initial') option = 'all';

	if (USER_ID) {
		query = `
				query GetUserTriosCourses($id: ID, $option: String!) {
					user(id: $id) {
						usertrioSet {
							trio {
								module {
									course {
										id 
									}
								}
							}
							done
						}
					}
					
					courses(id: $id, option: $option) {
						id
						name
						img
						modules {
							trios {
								id
							}
						}
					}
				}
			`;

		body = JSON.stringify({ query, variables: { id: USER_ID, option: option } });
	} else {
		if (option !== 'all') return displayError('Error de sesión', 'Inicie sesión para acceder a los cursos.');
		query = `
			query GetCourses($option: String!) {
				courses(option: $option) {
					id
					name
					img
				}
			}
		`;
		body = JSON.stringify({ query, variables: { option: 'all' } });
	}

	// Fetch
	await fetch(GRAPHQL_URL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: body,
		credentials: 'include',
	})
		.then((response) => {
			if (!response.ok) throw Error(`${response.statusText} - ${response.status}`);
			return response.json();
		})
		.then((data: GetUserTriosCourses) => {
			// Get the container
			const container = document.querySelector('#index > div.container');
			container.innerHTML = '';

			if (data.data.courses.length === 0) {
				displayError('No hay cursos', 'Te mandaremos a la página principal.');
				return getCourses('all');
			}

			// Render each course
			data.data.courses.forEach((course, i) => {
				// Create card
				const card = document.createElement('a');
				card.dataset.id = course.id.toString();
				card.classList.add('card');

				// Create img
				const img = document.createElement('img');
				img.classList.add('card-image');
				img.style.content = `url('${COURSE_URL}${course.img}')`;

				// Create text container
				const text = document.createElement('div');
				text.classList.add('card-text');

				// Create title and progress
				const h2 = document.createElement('h2');
				h2.innerHTML = course.name;
				const prog = document.createElement('progress');

				// Set the progress bar
				let max = 0;
				if (course.modules) {
					course.modules.forEach((trio, i) => {
						max += trio.trios.length * 3;
					});
				}
				prog.max = max;

				if (!data.data.user) {
					prog.value = 0;
				} else {
					let value = 0;
					data.data.user.usertrioSet.forEach((usertrio) => {
						if (usertrio.trio.module.course.id == card.dataset.id) {
							usertrio.done.forEach((val) => {
								if (val) {
									value++;
								}
							});
						}
					});
					prog.value = value;
				}

				// Add title and prog to text
				text.append(h2, prog);

				// Add img and text to container
				card.append(img, text);

				// Append new card to container
				container.append(card);
			});

			if (window.location.href.split('/')[4] === `#${option}`) return;
			if ((history.state?.option === 'all' || history.state?.option === null || history.state === null) && option === 'all') {
				history.replaceState({ option }, '', './');
				return;
			}
			history.pushState(option === 'all' ? null : { option }, '', option === 'all' ? '' : `./#${option}`);
		})
		.catch((error: Error) => {
			displayError('Error', error.message);
		});
}

await getCourses('initial');

// Run functions after main script
courseClick();

export function getCookie(name: string): string {
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

/* Event listeners for other courses options */
Array.from(document.getElementsByClassName('course')).forEach((el: HTMLElement) => {
	el.addEventListener('click', async () => {
		// Get selected courses
		await getCourses(el.classList.contains('ongoing') ? 'ongoing' : 'done');

		// Run functions after main script
		courseClick();
	});
});

window.addEventListener('popstate', (event) => {
	if (event.state === null) return;
	if (!event.state?.option) return getCourses('all');
	getCourses(event.state.option);
});

// Function to use the modal to display errors
export function displayError(title: string, text: string) {
	clearModal();

	const modal = document.getElementById('modal');

	// Open modal
	modal.style.display = 'block';

	// Set the title
	const m_title = document.getElementById('modal-title');
	m_title.innerText = title;

	const m_body = <HTMLElement>document.getElementsByClassName('modal-body')[0];
	m_body.insertAdjacentHTML('afterbegin', `<span class="modal-error-text">${text}</h2>`);
}
