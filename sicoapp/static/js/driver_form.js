document.addEventListener("DOMContentLoaded", function() {

// START READONLY FIELD
function setFieldReadonly(fieldId) {
    var field = document.getElementById(fieldId);
    var instanceId = document.getElementById('form-instance-id').dataset.instanceId;
    if (field && instanceId) {
        field.setAttribute("readonly", "readonly");
        field.style.backgroundColor = "#e9ecef";
        field.style.pointerEvents = "none";
    }
}

setFieldReadonly("id_dni");
// END READONLY FIELD

// START FIELD UPPERCASE AND HANDLE FOCUS
    var fields = [
        { id: "id_name", transform: "toUpperCase" },
        { id: "id_last_name", transform: "toUpperCase" },
        { id: "id_license", transform: "toUpperCase" },
        { id: "id_justify", transform: "toUpperCase" },
    ];

    function transformInput(event, transform) {
        if (transform === "toUpperCase") {
            event.target.value = event.target.value.toUpperCase();
        }
    }

    fields.forEach(function(field) {
        var element = document.getElementById(field.id);

        if (field.transform === "toUpperCase") {
            element.addEventListener("input", function(event) {
                transformInput(event, field.transform);
            });
        }
    });
// END FIELD UPPERCASE AND HANDLE FOCUS

// START TOOGLE JUSTIFY
    function toggleJustify() {
        var available = document.getElementById('id_available').checked;
        var justifyField = document.getElementById('id_justify');

        if (available) {
            justifyField.readOnly = true;
            justifyField.style.backgroundColor = '#f0f0f0';
            justifyField.style.cursor = 'not-allowed';
            justifyField.value = '';
        } else {
            justifyField.readOnly = false;
            justifyField.style.backgroundColor = '';
            justifyField.style.cursor = '';
        }
    }

    toggleJustify();
    document.getElementById('id_available').addEventListener('change', function() {
        toggleJustify();
    });
// END TOOGLE JUSTIFY

});
