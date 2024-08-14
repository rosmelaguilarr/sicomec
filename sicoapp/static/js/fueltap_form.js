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

setFieldReadonly("id_ruc");
// END READONLY FIELD

// START FIELD UPPERCASE AND HANDLE FOCUS
    var fields = [
        { id: "id_business_name", transform: "toUpperCase" },
        { id: "id_address", transform: "toUpperCase" },
        { id: "id_email", transform: "toUpperCase" },
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

});
