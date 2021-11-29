var downloadPdf = document.getElementById('download-pdf');
var submitForm = document.getElementById('submit-form');
downloadPdf.addEventListener('click', function () {
    if (!validateEmail(document.getElementById('emailInput').value)) {
        document.querySelector('.alert.alert-danger').innerHTML = 'Error: La dirección de email no es válida, intente otra vez.';
        return;
    }
    var el = document.createElement('a');
    el.href = '/static/cme/brochure.pdf';
    el.download = 'CME.pdf';
    document.documentElement.appendChild(el);
    el.click();
    document.documentElement.removeChild(el);
    submitForm.click();
});
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase().trim());
}
//# sourceMappingURL=capture.js.map