import { clearModal, courseClick } from './course.js';
export const GRAPHQL_URL = '/graphql';
const MEDIA_URL = '/static/training/media/';
export let USER_ID;
async function getCourses(option) {
    // Create the query and body
    let query;
    let body;
    try {
        USER_ID = JSON.parse(document.getElementById('user_id').textContent);
    }
    catch {
        USER_ID = null;
    }
    if ((window.location.href.split('/')[4] === '#done' || window.location.href.split('/')[4] === '#ongoing') && option === 'initial')
        option = window.location.href.split('/')[4].replace('#', '');
    if (option === 'initial')
        option = 'all';
    if (USER_ID) {
        query = `
			query GetUserFileCourses($id: ID, $option: String!) {
				user(id: $id) {
					userfileSet {
						file {
							module {
								course {
									id
								}
							}
						}
						
						done
					}
				}
				
				trainingCourses(option: $option, id: $id) {
					id
					name
					img
					modules {
						files {
							id
						}
					}
				}
			}`;
        body = JSON.stringify({ query, variables: { id: USER_ID, option: option } });
    }
    else {
        if (option !== 'all')
            return displayError('Error de sesión', 'Inicie sesión para acceder a los cursos.');
        query = `
			{
				trainingCourses(option: "all") {
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
        if (!response.ok)
            throw Error(`${response.statusText} - ${response.status}`);
        return response.json();
    })
        .then((data) => {
        // Get the container
        const container = document.querySelector('#index > div.container');
        container.innerHTML = '';
        if (data.data.trainingCourses.length === 0) {
            displayError('No hay cursos', 'Te mandaremos a la página principal.');
            return getCourses('all');
        }
        // Render each course
        data.data.trainingCourses.forEach((course, i) => {
            // Create card
            const card = document.createElement('a');
            card.dataset.id = course.id.toString();
            card.classList.add('card');
            // Create img
            const img = document.createElement('div');
            img.classList.add('card-image');
            img.style.backgroundImage = `url('${MEDIA_URL}${course.img}')`;
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
                course.modules.forEach((file, i) => {
                    max += file.files.length;
                });
            }
            prog.max = max;
            if (!data.data.user) {
                prog.value = 0;
            }
            else {
                let value = 0;
                data.data.user.userfileSet.forEach((userfile) => {
                    if (userfile.file.module.course.id == card.dataset.id) {
                        if (userfile.done)
                            value++;
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
        if (window.location.href.split('/')[4] === `#${option}`)
            return;
        if ((history.state?.option === 'all' || history.state?.option === null || history.state === null) && option === 'all') {
            history.replaceState({ option }, '', './');
            return;
        }
        history.pushState(option === 'all' ? null : { option }, '', option === 'all' ? '' : `./#${option}`);
    })
        .catch((error) => {
        displayError('Error', error.message);
    });
}
await getCourses('initial');
// Run functions after main script
courseClick();
export function getCookie(name) {
    let cookieValue = null;
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
Array.from(document.getElementsByClassName('course')).forEach((el) => {
    el.addEventListener('click', async () => {
        // Get selected courses
        await getCourses(el.classList.contains('ongoing') ? 'ongoing' : 'done');
        // Run functions after main script
        courseClick();
    });
});
window.addEventListener('popstate', (event) => {
    if (event.state === null)
        return;
    if (!event.state?.option)
        return getCourses('all');
    getCourses(event.state.option);
});
// Function to use the modal to display errors
export function displayError(title, text) {
    clearModal();
    const modal = document.getElementById('modal');
    // Open modal
    modal.style.display = 'block';
    // Set the title
    const m_title = document.getElementById('modal-title');
    m_title.innerText = title;
    const m_body = document.getElementsByClassName('modal-body')[0];
    m_body.insertAdjacentHTML('afterbegin', `<span class="modal-error-text">${text}</h2>`);
}
//# sourceMappingURL=index.js.map