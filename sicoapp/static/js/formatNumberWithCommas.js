document.addEventListener("DOMContentLoaded", function() {
    function formatNumberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    document.querySelectorAll('.number').forEach(function(element) {
        let stock = element.dataset.stock;
        let residue = element.dataset.residue;

        if (stock) {
            element.textContent = formatNumberWithCommas(parseInt(stock, 10));
        }

        if (residue) {
            element.textContent = formatNumberWithCommas(parseInt(residue, 10));
        }
    });
});
