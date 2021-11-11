// Score display
const q_group = Array.from(document.getElementsByClassName('question-group'));
q_group.forEach((ol) => {
    // The score for each block
    Array.from(ol.getElementsByClassName('radio')).forEach((el) => {
        el.addEventListener('change', (event) => {
            let block_score = 0;
            Array.from(ol.getElementsByClassName('si')).forEach((yes) => {
                // Check if it was checked
                if (yes.checked) {
                    block_score += 4;
                }
            });
            ol.querySelector('span.score').innerHTML = block_score.toString();
        });
    });
});
// Saving scores
// TODO: Make validation and error handling.
document.getElementById('survey').addEventListener('submit', () => {
    let overall = 0;
    let scores = [];
    // Get the scores from all the blocks
    Array.from(document.getElementsByClassName('score')).forEach((score) => {
        overall += parseInt(score.innerHTML);
        scores.push(score.innerHTML);
    });
    localStorage.setItem('overall', overall.toString());
    localStorage.setItem('scores', scores.toString());
});
//# sourceMappingURL=score.js.map