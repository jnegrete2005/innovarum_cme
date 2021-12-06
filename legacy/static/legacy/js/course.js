import { getCookie, GRAPHQL_URL } from './index.js';
import { updateUsertrio } from './trios.js';
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
						done
					}
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
    Array.from(document.getElementsByClassName('card')).forEach((card) => {
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
                if (!response.ok)
                    throw Error(`${response.statusText} - ${response.status}`);
                return response.json();
            })
                .then((data) => {
                fillCourse(data);
            })
                .catch((error) => {
                alert(error.message);
            });
        });
    });
}
// Will fill the modal with the course info
function fillCourse(data) {
    modal.dataset.id = data.data.course.id;
    // Get the modal
    const mBody = modal.getElementsByClassName('modal-body')[0];
    // Get modal title
    const title = document.getElementById('modal-title');
    title.innerText = data.data.course.name;
    // Create ul for modules
    const ml = mBody.getElementsByClassName('course-module-list')[0];
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
                module.trios.forEach((trio) => {
                    // Get trio
                    const template_trio = [
                        createTrio(trio, `/media/${trio.file}`, trio.file.split('/')[2], '/static/legacy/icons/file.svg', 0),
                        createTrio(trio, trio.video, trio.video, '/static/legacy/icons/play.svg', 1),
                        createTrio(trio, '', 'Autoevaluación', '/static/legacy/icons/pencil.svg', 2),
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
function createTrio(trio, href, innerText, icon, i) {
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
    checkbox.checked = trio.usertrioSet[0] ? trio.usertrioSet[0].done[i] : false;
    // Append the anchor tags to the li, and the li to the ul
    tLi.append(div, checkbox);
    return tLi;
}
function clearModal() {
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
    document.getElementsByClassName('course-module-list')[0].innerHTML = null;
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