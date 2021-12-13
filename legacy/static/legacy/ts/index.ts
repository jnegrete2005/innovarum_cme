import { courseClick } from './course.js';

import type { GetUserTriosCourses, courseModes } from './graphql';

export const GRAPHQL_URL = '/graphql';

async function getCourses(option: keyof courseModes) {
	// Create the query and body
	let query: string;
	let body: BodyInit;
	let user_id: number | null;

	try {
		user_id = JSON.parse(document.getElementById('user_id').textContent);
	} catch {
		user_id = null;
	}

	if ((window.location.href.split('/')[4] === '#done' || window.location.href.split('/')[4] === '#ongoing') && option === 'initial')
		option = <keyof courseModes>window.location.href.split('/')[4].replace('#', '');

	if (option === 'initial') option = 'all';

	if (user_id) {
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

		body = JSON.stringify({ query, variables: { id: user_id, option: option } });
	} else {
		if (option !== 'all') return alert('Inicie sesión para acceder a los cursos.');
		query = `
		{
			courses {
				id
				name
				img
			}
		}
		`;
		body = JSON.stringify({ query });
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
				alert('No hay cursos. Te mandaremos a la página principal');
				return getCourses('all');
			}

			// Render each course
			data.data.courses.forEach((course, i) => {
				// Create card
				const card = document.createElement('a');
				card.dataset.id = course.id.toString();
				card.classList.add('card');

				// Create img
				const img = document.createElement('div');
				img.classList.add('card-image');
				img.style.backgroundImage = `url('/media/${course.img}')`;

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
						prog.value = value;
					});
				}

				// Add title and prog to text
				text.append(h2, prog);

				// Add img and text to container
				card.append(img, text);

				// Append new card to container
				container.append(card);
			});

			if (window.location.pathname.split('/')[2] === option) return;
			if ((history.state?.option === 'all' || history.state?.option === null || history.state === null) && option === 'all') return;
			history.pushState(option === 'all' ? null : { option }, '', option === 'all' ? '' : `./${option}`);
		})
		.catch((error: Error) => {
			alert(error.message);
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
	if (!event.state?.option) return getCourses('all');
	getCourses(event.state.option);
});
