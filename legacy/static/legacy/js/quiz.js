// Add event listener to add
Array.from(document.getElementsByClassName('add')).forEach((el) => {
    el.addEventListener('click', () => {
        add(el);
    });
});
// Add event listener to remove
Array.from(document.getElementsByClassName('remove')).forEach((el) => {
    el.addEventListener('click', () => {
        remove(el);
    });
});
function add(el) {
    // Case for question
    if (el.parentElement.dataset.question === 'true')
        return addQuestion();
    // Case for answer
    return addAnswer(el);
}
function remove(el) { }
function addAnswer(el) {
    // Get the index of the question
    const i = parseInt(el.parentElement.parentElement.parentElement.parentElement.dataset.index);
    // Get the answer container
    const answers = el.parentElement.parentElement.parentElement;
    // Get the index of the answer
    const j = parseInt(answers.children[answers.children.length - 1].dataset.index);
    answers.innerHTML += `
    <div class="form_group field" data-index="${j + 1}">
      <input class="form_field" type="text" name="answer${i}" id="answer-${i}-${j + 1}-Input" placeholder="Respuesta ${j + 1}" />
      <label class="form_label" for="answer-${i}-${j + 1}-Input">Respuesta ${j + 1}</label>
    </div>
  `;
    answers.querySelector('span.add').addEventListener('click', () => {
        add(answers.querySelector('span.add'));
    });
    return;
}
function addQuestion() {
    // Get the container
    const question_container = document.getElementsByClassName('questions')[0];
    // Get the last question to get it's index
    const last_question = question_container.getElementsByClassName('question')[question_container.getElementsByClassName('question').length - 1];
    const i = parseInt(last_question.dataset.index);
    // Append to it
    question_container.innerHTML += `
  <div class="questions">
    <div class="question" data-index="${i + 1}">
      <h3>Pregunta ${i + 1}</h3>
      <div class="form_group field">
        <input class="form_field" type="text" name="question" id="question${i + 1}Input" placeholder="Pregunta ${i + 1}" />
        <label class="form_label" for="question${i + 1}Input">Pregunta ${i + 1}</label>
      </div>

      <!-- Answers -->
      <div class="answer-container">
        <div class="add-remove">
          <h4>Respuestas</h4>
          <div>
            <span class="add">&plus;</span>
            <span class="remove">&minus;</span>
          </div>
        </div>
        <div class="form_group field" data-index="1">
          <input class="form_field" type="text" name="answer${i + 1}" id="answer-${i + 1}-1-Input" placeholder="Respuesta 1" />
          <label class="form_label" for="answer-${i + 1}-1-Input">Respuesta 1</label>
        </div>
      </div>
    </div>
  </div>
  `;
    // Add event listener to all .add inside .answer-container
    Array.from(document.getElementsByClassName('answer-container')).forEach((el) => {
        Array.from(el.getElementsByClassName('add')).forEach((el) => {
            el.addEventListener('click', () => {
                add(el);
            });
        });
    });
    return;
}
//# sourceMappingURL=quiz.js.map