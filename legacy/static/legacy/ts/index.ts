import type { CoursesQuery } from './graphql';

const GRAPHQL_URL = 'graphql';

function getCourses() {
	// Create the query
	const query = `
    {
      courses {
        id
        name
        img
      }
    }
  `;

	// Fetch
	fetch(`/${GRAPHQL_URL}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: JSON.stringify({ query }),
		credentials: 'include',
	})
		.then((response) => {
			if (!response.ok) throw Error(`${response.statusText} - ${response.status}`);
			return response.json();
		})
		.then((data: CoursesQuery) => {
			// Get the container
			const container = document.querySelector('#index > div.container');

			// Render each course
			data.data.courses.forEach((course) => {
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
				/* TODO: Add max and value to progress */

				// Add title and prog to text
				text.append(h2, prog);

				// Add img and text to container
				card.append(img, text);

				// Append new card to container
				container.append(card);
			});
		});
}

getCourses();

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
