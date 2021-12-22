import { displayError, getCookie, GRAPHQL_URL, USER_ID } from './index.js';
import { updateUserfile } from './trios.js';
const modal = document.getElementById('modal');
const span = document.getElementsByClassName('close')[0];
const query = `
	query GetCourse($id: ID!) {
		trainingCourse(id: $id) {
			id
			name
			modules {
				name
				files {
					userfileSet {
						user {
							id
						}
						done
					}
					id
					name
					url
					fileType
				}
			}
		}
	}
`;
export function courseClick() {
    Array.from(document.getElementsByClassName('card')).forEach((card) => {
        card.addEventListener('click', () => {
            // If not logged in, put an error
            try {
                JSON.parse(document.getElementById('user_id').textContent);
            }
            catch {
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
                if (!response.ok)
                    throw Error(`${response.statusText} - ${response.status}`);
                return response.json();
            })
                .then((data) => {
                fillCourse(data);
            })
                .catch((error) => {
                displayError('Error', error.message);
            });
        });
    });
}
// Will fill the modal with the course info
function fillCourse(data) {
    modal.dataset.id = data.data.trainingCourse.id;
    // Get the modal
    const mBody = modal.getElementsByClassName('modal-body')[0];
    // Get modal title
    const title = document.getElementById('modal-title');
    title.innerText = data.data.trainingCourse.name;
    // Create ul for modules
    const ml = mBody.getElementsByClassName('course-module-list')[0];
    // Create modules
    if (data.data.trainingCourse.modules) {
        data.data.trainingCourse.modules.forEach((module, i) => {
            // Create li for module
            const li = document.createElement('li');
            // Create module heading
            const mT = document.createElement('h2');
            mT.innerText = module.name;
            // If trios, create them
            // Create ul for trios
            const ul = document.createElement('ul');
            ul.classList.add('trios');
            if (module.files) {
                module.files.forEach((file) => {
                    // Create file
                    const file_el = createTrio(file);
                    // Create a wrapper div for trio
                    const wrapper_trio = document.createElement('div');
                    wrapper_trio.ariaRoleDescription = 'Wrap a trio';
                    wrapper_trio.dataset.id = file.id;
                    wrapper_trio.append(file_el);
                    // Append wrapper
                    ul.append(wrapper_trio);
                });
            }
            // Join everything
            li.append(mT, ul);
            ml.append(li);
        });
    }
    updateUserfile();
}
function createTrio(file, new_tab = false) {
    // Create li for file
    const tLi = document.createElement('li');
    // Create the link
    const a = document.createElement('a');
    a.href = file.url;
    a.innerText = file.name;
    a.target = new_tab ? '_blank' : a.target;
    // Create icon
    const svg = document.createElement('img');
    svg.src = `/static/legacy/icons/${file.fileType === 'A_1' ? 'file.svg' : 'play.svg'}`;
    svg.alt = 'Ícono';
    svg.setAttribute('aria-details', 'By fontawesome. https://fontawesome.com/license');
    // Create wrapper for icon and link
    const div = document.createElement('div');
    div.append(svg, a);
    // Create the checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = file.id;
    // Check the checkbox
    checkbox.checked = check(file);
    // Append the anchor tags to the li, and the li to the ul
    tLi.append(div, checkbox);
    return tLi;
}
function check(file) {
    let answer = false;
    file.userfileSet.forEach((userfile) => {
        if (parseInt(userfile?.user.id) === USER_ID) {
            answer = userfile.done;
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
            if (el.lastElementChild.checked) {
                val++;
            }
        });
        // Find the course it closed from
        Array.from(document.querySelectorAll('a.card')).forEach((card) => {
            if (card.dataset.id === modal.dataset.id) {
                card.querySelector('progress').value = val;
            }
        });
        modal.dataset.id = null;
    }
    catch { }
    const m_body = document.getElementsByClassName('modal-body')[0];
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
//# sourceMappingURL=course.js.map