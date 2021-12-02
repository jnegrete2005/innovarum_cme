const GRAPHQL_URL = 'graphql';
function getCourses() {
    // Create the query and body
    let query;
    let body;
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    if (user_id) {
        query = `
			query GetUserTriosCourses($id: ID!) {
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
				
				courses {
					id
					name
					img
				}
			}
		`;
        body = JSON.stringify({ query, variables: { id: user_id } });
    }
    else {
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
    fetch(`/${GRAPHQL_URL}`, {
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
        // Render each course
        data.data.courses.forEach((course, i) => {
            // Create card
            const card = document.createElement('a');
            card.dataset.id = course.id.toString();
            card.classList.add('card');
            // Create img
            const img = document.createElement('div');
            img.classList.add('card-image');
            img.style.backgroundImage = `url('/media/legacy/courses/${course.img}')`;
            // Create text container
            const text = document.createElement('div');
            text.classList.add('card-text');
            // Create title and progress
            const h2 = document.createElement('h2');
            h2.innerHTML = course.name;
            const prog = document.createElement('progress');
            // Set the progress bar
            let max = 0;
            if (data.data.courses[i].modules) {
                data.data.courses[i].modules.forEach((trio, i) => {
                    max += trio.trios.length * 3;
                });
                prog.max = max;
            }
            if (!data.data.user) {
                prog.value = 0;
            }
            else {
                data.data.user.usertrioSet.forEach((usertrio) => {
                    if (usertrio.trio.module.course.id == card.dataset.id) {
                        let value = 0;
                        usertrio.done.forEach((val) => {
                            if (val) {
                                value++;
                            }
                        });
                        prog.value = value;
                    }
                });
            }
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
//# sourceMappingURL=index.js.map