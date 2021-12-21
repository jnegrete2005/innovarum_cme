import { displayError, getCookie, GRAPHQL_URL } from './index.js';
export function updateUserfile() {
    // Select all the checkboxes
    Array.from(document.querySelectorAll('input[type=checkbox]')).forEach((checkbox) => {
        // Add event listener to individual checkbox
        checkbox.addEventListener('click', async () => {
            // Get the trio wrapper
            const wrapper = checkbox.parentElement.parentElement;
            // Get trio checkboxes values
            const done = checkbox.checked;
            // Create query
            const query = `
				mutation UpdateUserFile($file_id: ID!, $user_id: ID!, $done: Boolean!) {
					updateUserfile(fileId: $file_id, userId: $user_id, done: $done) {
						file {
							id
							done
						}
					}
				}
      `;
            // Get user
            let user_id;
            try {
                user_id = JSON.parse(document.getElementById('user_id').textContent);
            }
            catch {
                user_id = null;
            }
            // Body for fetch
            const body = JSON.stringify({
                query,
                variables: {
                    file_id: wrapper.dataset.id,
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
                if (!response.ok)
                    throw Error(`No se pudo actualizar lo completado.\n${response.statusText} - ${response.status}`);
                return response.json();
            })
                .catch((error) => {
                displayError('Error', error.message);
            });
        });
    });
}
//# sourceMappingURL=trios.js.map