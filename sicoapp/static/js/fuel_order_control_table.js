    document.addEventListener("DOMContentLoaded", function() {
        const orderSelect = document.getElementById('id_buy_order');
        const userAreaField = document.getElementById('id_user_area');
        const fueltapField = document.getElementById('id_fueltap');
        const fuelField = document.getElementById('id_fuel');
        const stockField = document.getElementById('id_stock');
        const residueField = document.getElementById('id_residue');
        const tableBody = document.querySelector('.table tbody');

        orderSelect.addEventListener('change', function() {
            const selectedValue = orderSelect.value;
            if (selectedValue) {
                fetch(`/sicomec/get_buy_order_details/${selectedValue}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        userAreaField.value = data.user_area || '';
                        fueltapField.value = data.fueltap || '';
                        fuelField.value = data.fuel || '';
                        stockField.value = data.stock || '';
                        residueField.value = data.residue || '';
                    })
                    .catch(error => console.error('Error fetching buy order details:', error));

                fetch(`/sicomec/get_fuel_orders/${selectedValue}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        tableBody.innerHTML = '';

                        if (data.fuel_orders) {
                            data.fuel_orders.forEach(fuel_order => {
                                const row = document.createElement('tr');

                                const isCanceled = fuel_order.canceled ? 'border-danger' : '';
                                const isFuelLoan = fuel_order.fuel_loan ? 'border-warning' : '';
                                const isFuelReturn = fuel_order.fuel_return ? 'border-success' : '';
                                const borderClass = [isCanceled, isFuelLoan, isFuelReturn].filter(Boolean).join(' ');

                                row.innerHTML = `
                                    <td class="align-middle" style="user-select: none;">${fuel_order.date}</td>
                                    <td class="align-middle ${borderClass}" style="user-select: none;">${fuel_order.fuel_return ? "+": "-" }${fuel_order.quantity}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.residue}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.plate__plate ? fuel_order.plate__plate : ""}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.vehicle ? fuel_order.vehicle : ""}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.brand ? fuel_order.brand : ""}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.driver__name ? fuel_order.driver__name : ""} ${fuel_order.driver__last_name ? fuel_order.driver__last_name : ""}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.voucher}</td>
                                    <td class="align-middle" style="user-select: none;">${fuel_order.code}</td>
                                `;

                                tableBody.appendChild(row);
                            });
                        }

                    })
                    .catch(error => console.error('Error fetching fuel orders:', error));
            } else {
                userAreaField.value = '';
                fueltapField.value = '';
                fuelField.value = '';
                stockField.value = '';
                tableBody.innerHTML = '';
            }
        });


        // START PRINT BUTTON
        const selectElement = document.getElementById('id_buy_order');
        const printButton = document.getElementById('printButton');
        const baseUrl = printButton.getAttribute('data-base-url');

        selectElement.addEventListener('change', function () {
            const selectedOrderId = selectElement.value;

            if (selectedOrderId) {
                const urlWithOrderId = baseUrl + selectedOrderId;
                printButton.href = urlWithOrderId;

            } else {
                printButton.href = '#'; 
            }
        });
        // END PRINT BUTTON

    });
