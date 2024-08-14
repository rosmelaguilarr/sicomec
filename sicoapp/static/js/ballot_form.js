document.addEventListener("DOMContentLoaded", function() {

    // START AJAX
    const plateSelect = document.getElementById('id_plate');
    const brandField = document.getElementById('id_vehicle_brand');
    const vehicleField = document.getElementById('id_vehicle_name');

    const driverSelect = document.getElementById('id_driver');
    const licenseField = document.getElementById('id_driver_license');
    const categoryField = document.getElementById('id_driver_category');

    plateSelect.addEventListener('change', function() {
        const selectedValue = plateSelect.value;
        if (selectedValue) {
            fetch(`/sicomec/get_vehicle_details/${selectedValue}`)
                .then(response => response.json())
                .then(data => {
                    brandField.value = data.brand;
                    vehicleField.value = data.vehicle;
                });
        } else {
            brandField.value = '';
            vehicleField.value = '';
        }
    });

    driverSelect.addEventListener('change', function() {
        const selectedValue = driverSelect.value;
        if (selectedValue) {
            fetch(`/sicomec/get_driver_details/${selectedValue}`)
                .then(response => response.json())
                .then(data => {
                    licenseField.value = data.license;
                    categoryField.value = data.category;
                });
        } else {
            licenseField.value = '';
            categoryField.value = '';
        }
    });
    // END AJAX 
    
    // START FIELD UPPERCASE AND HANDLE FOCUS
    function setFieldReadonly(fieldId) {
        var field = document.getElementById(fieldId);
        var instanceId = document.getElementById('form-instance-id').dataset.instanceId;
        if (field && instanceId) {
            field.setAttribute("readonly", "readonly");
            field.style.backgroundColor = "#e9ecef";
            field.style.pointerEvents = "none";
        }
    }

    setFieldReadonly("id_driver_license");
    setFieldReadonly("id_driver_category");
    setFieldReadonly("id_vehicle_name");
    setFieldReadonly("id_vehicle_brand");
    
    
    var fields = [
        { id: "id_drive_to", transform: "toUpperCase" },
        { id: "id_place", transform: "toUpperCase" },
        { id: "id_reason", transform: "toUpperCase" },
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