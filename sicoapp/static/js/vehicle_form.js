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

setFieldReadonly("id_plate");
setFieldReadonly("id_type");
// END READONLY FIELD

// START FIELD UPPERCASE AND HANDLE FOCUS
    var fields = [
        { id: "id_plate", defaultValue: "", transform: "toUpperCase" },
        { id: "id_name", defaultValue: "", transform: "toUpperCase" },
        { id: "id_brand", defaultValue: "", transform: "toUpperCase" },
        { id: "id_model", defaultValue: "", transform: "toUpperCase" },
        { id: "id_chassis", defaultValue: "", transform: "toUpperCase" },
        { id: "id_justify", defaultValue: "", transform: "toUpperCase" },
        { id: "id_mileage", defaultValue: "0", transform: "toUpperCase" },
        { id: "id_hourometer", defaultValue: "0", transform: "toUpperCase" },
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

// START TOOGLE TYPE VEHICLE
    const typeField = document.getElementById('id_type');
    const mileageField = document.getElementById('id_mileage');
    const hourometerField = document.getElementById('id_hourometer');

    function toggleFields() {
        const selectedOption = typeField.options[typeField.selectedIndex];
        const selectedText = selectedOption.text;

        if (selectedText === 'VEHICULO') {  
            mileageField.disabled = false;
            hourometerField.disabled = true;
            hourometerField.value = '';
        } else if (selectedText === 'MAQUINARIA') {  
            mileageField.disabled = true;
            hourometerField.disabled = false;
            mileageField.value = '';
        } else {
            mileageField.disabled = false;
            hourometerField.disabled = false;
        }
    }

    toggleFields();
    typeField.addEventListener('change', toggleFields);
// END TOOGLE TYPE VEHICLE

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
