
document.addEventListener("DOMContentLoaded", function() {

// START AJAX
    const plateSelect = document.getElementById('id_plate');
    const brandField = document.getElementById('id_brand');
    const vehicleField = document.getElementById('id_vehicle');
    const orderSelect = document.getElementById('id_order');
    const userAreaField = document.getElementById('id_user_area');
    const fuelTapField = document.getElementById('id_fueltap');
    const fuelField = document.getElementById('id_fuel');
    const residueBuyOrderField = document.getElementById('id_residue_buy_order');

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

    orderSelect.addEventListener('change', function() {
        const selectedValue = orderSelect.value;
        if (selectedValue) {
            fetch(`/sicomec/get_buy_order_details/${selectedValue}`)
                .then(response => response.json())
                .then(data => {
                    userAreaField.value = data.user_area;
                    fuelTapField.value = data.fueltap;
                    fuelField.value = data.fuel;
                    residueBuyOrderField.value = data.residue.replace(/,/g, '');
                    
                });
        } else {
            userAreaField.value = '';
            fuelTapField.value = '';
            fuelField.value = '';
            residueBuyOrderField.value = '';
        }
    });
// END AJAX 

// START READONLY FIELD
    // function setFieldReadonly(fieldId) {
    //     var field = document.getElementById(fieldId);
    //     var instanceId = document.getElementById('form-instance-id').dataset.instanceId;
    //     if (field && instanceId) {
    //         if (field.type === 'checkbox') {
    //             field.setAttribute("disabled", "disabled");
    //         } else {
    //             field.setAttribute("readonly", "readonly");
    //         }

    //         field.style.backgroundColor = "#e9ecef";
    //         field.style.pointerEvents = "none";
    //     }
    // }

    // setFieldReadonly("id_order");
    // setFieldReadonly("id_brand");
    // setFieldReadonly("id_vehicle");
    // setFieldReadonly("id_fueltap");
    // setFieldReadonly("id_fuel");
    // setFieldReadonly("id_quantity");
    // setFieldReadonly("id_fuel_loan");
    // setFieldReadonly("id_fuel_return");
// END READONLY FIELD

// START FIELD UPPERCASE AND HANDLE FOCUS
    var fields = [
        { id: "id_place",  defaultValue: "", transform: "toUpperCase" },
        { id: "id_reason",  defaultValue: "", transform: "toUpperCase" },
        { id: "id_quantity",  defaultValue: "0", transform: null },
        { id: "id_detail",  defaultValue: "", transform: "toUpperCase" },
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

// START TOOGLE FUEL_LOAN
function toggleFuelLoan() {
    var fuel_loan = document.getElementById('id_fuel_loan').checked;
    var fuel_return = document.getElementById('id_fuel_return').checked;

    var driverField = document.getElementById('id_driver');
    var plateField = document.getElementById('id_plate');
    var brandField = document.getElementById('id_brand');
    var vehicleField = document.getElementById('id_vehicle');

    const placeContainer = document.querySelector('.place-container');
    const reasonContainer = document.querySelector('.reason-container');
    const detailContainer = document.querySelector('.detail-container');

    if (fuel_loan || fuel_return) {
        driverField.disabled = true;
        plateField.disabled = true;
        brandField.disabled = true
        vehicleField.disabled = true;
        placeContainer.style.display = 'none';
        reasonContainer.style.display = 'none';
        detailContainer.style.display = 'block';

        driverField.value = '';
        plateField.value = ''
        brandField.value = ''
        vehicleField.value = '';
        placeContainer.value = ''
        reasonContainer.value = '';
        detailContainer.value = '';
    } else {
        driverField.disabled = false;
        plateField.disabled = false
        brandField.disabled = false
        vehicleField.disabled = false;
        detailContainer.style.display = 'none';
        placeContainer.style.display = 'block';
        reasonContainer.style.display = 'block';
    }
}

toggleFuelLoan();

document.getElementById('id_fuel_loan').addEventListener('change', function() {
    toggleFuelLoan();
});
document.getElementById('id_fuel_return').addEventListener('change', function() {
    toggleFuelLoan();
});

// END TOOGLE FUEL_LOAN

});
