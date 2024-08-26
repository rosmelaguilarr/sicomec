// static/js/datatables.js

$(document).ready(function() {
    $('.datatable').DataTable({
        "language": {
            // "url": "//cdn.datatables.net/plug-ins/2.1.4/i18n/es-ES.json"
            "url": "/sicomec/static/js/es-ES.json"
        },
        "paging": true,
        "searching": true,
        "ordering": true,
        "info": true
    });
});
