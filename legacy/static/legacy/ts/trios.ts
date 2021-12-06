import { getCookie, GRAPHQL_URL } from './index.js';

export function updateUsertrio() {
	// Select all the checkboxes
	Array.from(<NodeListOf<HTMLInputElement>>document.querySelectorAll('input[type=checkbox]')).forEach((checkbox) => {
		// Add event listener to individual checkbox
		checkbox.addEventListener('click', async () => {
			// Get the trio wrapper
			const wrapper = checkbox.parentElement.parentElement;

			// Get trio checkboxes values
			const done = getTrioValue(wrapper.querySelectorAll('input[type=checkbox'));

			// Create query
			const query = `
        mutation UpdateUserTrio($trio_id: ID!, $user_id: ID!, $done: [Boolean]!) {
          updateUsertrio(trioId: $trio_id, userId: $user_id, done: $done) {
            trio {
              id
              done
            }
          }
        }
      `;

			// Get user
			let user_id: number | null;
			try {
				user_id = JSON.parse(document.getElementById('user_id').textContent);
			} catch {
				user_id = null;
			}

			// Body for fetch
			const body: BodyInit = JSON.stringify({
				query,
				variables: {
					trio_id: wrapper.dataset.id,
					user_id: user_id,
					done: done,
				},
			});

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
					if (!response.ok) throw Error(`No se pudo actualizar lo completado.\n${response.statusText} - ${response.status}`);
					return response.json();
				})
				.catch((error: Error) => {
					alert(error.message);
				});
		});
	});
}

function getTrioValue(trio: NodeListOf<Element>) {
	let done: Array<boolean> = [];

	Array.from(trio).forEach((el: HTMLInputElement) => {
		done.push(el.checked);
	});

	return done;
}
