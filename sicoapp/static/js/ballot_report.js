// START PRINT BUTTON
const printButton = document.getElementById('printButton');
const baseUrl = printButton.getAttribute('data-base-url');

function updatePrintButtonHref() {
    const startDate = document.getElementById('id_start_date').value;
    const endDate = document.getElementById('id_end_date').value;

    let urlWithParams = baseUrl;

    if (startDate) {
        urlWithParams += `?start_date=${startDate}`;
    }

    if (endDate) {
        if (urlWithParams.includes('?')) {
            urlWithParams += `&end_date=${endDate}`;
        } else {
            urlWithParams += `?end_date=${endDate}`;
        }
    }

    if (startDate || endDate) {
        if (urlWithParams.includes('?')) {
            urlWithParams += '&generate_pdf=1';
        } else {
            urlWithParams += '?generate_pdf=1';
        }
        printButton.href = urlWithParams;
        printButton.classList.remove('disabled');
    } else {
        printButton.href = '#';
        printButton.classList.add('disabled');
    }
}

document.getElementById('id_start_date').addEventListener('change', updatePrintButtonHref);
document.getElementById('id_end_date').addEventListener('change', updatePrintButtonHref);

updatePrintButtonHref();
// END PRINT BUTTON