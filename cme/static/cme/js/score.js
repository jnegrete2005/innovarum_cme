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
//# sourceMappingURL=score.js.map