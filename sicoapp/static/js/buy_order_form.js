
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

    setFieldReadonly("id_order");
    setFieldReadonly("id_stock");
// END READONLY FIELD

// START FIELD UPPERCASE AND HANDLE FOCUS
    var fields = [
        { id: "id_user_area",  defaultValue: "", transform: "toUpperCase" },
        { id: "id_stock",  defaultValue: "0", transform: null },
        { id: "id_order",  defaultValue: "", transform: "toUpperCase" },
    ];

    function handleFocus(event, defaultValue) {
        var element = event.target;
        if (element.value === defaultValue) {
            element.value = "";
        }
    }

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

        element.addEventListener("focus", function(event) {
            handleFocus(event, field.defaultValue);
        });

        element.addEventListener("blur", function(event) {
            if (event.target.value === "") {
                event.target.value = field.defaultValue;
            }
        });
    });
// END FIELD UPPERCASE AND HANDLE FOCUS

});
