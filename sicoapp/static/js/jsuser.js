
(function () {
    const $current_year = document.querySelector('.year')
    const now = new Date();
    const current_year = now.getFullYear();
    $current_year.innerText = current_year;
}
)();
