// START PRINT BUTTON
const ballotScheduledCheckbox = document.getElementById('id_ballot_scheduled');
const ballotCompleteCheckbox = document.getElementById('id_ballot_complete');
const printButton = document.getElementById('printButton');
const baseUrl = printButton.getAttribute('data-base-url');

function updatePrintButtonHref() {
    let urlWithParams = baseUrl;

    const ballotScheduled = ballotScheduledCheckbox.checked;
    const ballotComplete = ballotCompleteCheckbox.checked;

    if (ballotScheduled) {
        urlWithParams += '?ballot_scheduled=on';
    }

    if (ballotComplete) {
        if (urlWithParams.includes('?')) {
            urlWithParams += '&ballot_complete=on';
        } else {
            urlWithParams += '?ballot_complete=on';
        }
    }

    if (urlWithParams !== baseUrl) {
        if (urlWithParams.includes('?')) {
            urlWithParams += '&generate_pdf=1';
        } else {
            urlWithParams += '?generate_pdf=1';
        }
    }

    if (urlWithParams === baseUrl) {
        printButton.href = '#';  
        printButton.classList.add('disabled');  
    } else {
        printButton.href = urlWithParams;  
        printButton.classList.remove('disabled');  
    }
}

ballotScheduledCheckbox.addEventListener('change', updatePrintButtonHref);
ballotCompleteCheckbox.addEventListener('change', updatePrintButtonHref);

updatePrintButtonHref();
// END PRINT BUTTON