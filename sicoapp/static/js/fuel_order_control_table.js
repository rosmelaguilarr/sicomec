    document.addEventListener("DOMContentLoaded", function() {
        const orderInput = document.getElementById('id_orderInput');
        const userAreaField = document.getElementById('id_user_area');
        const fueltapField = document.getElementById('id_fueltap');
        const fuelField = document.getElementById('id_fuel');
        const stockField = document.getElementById('id_stock');
        const residueField = document.getElementById('id_residue');
        const tableElement = document.querySelector('.datatable');
        const printButton = document.getElementById('printButton');
        const baseUrl = printButton.getAttribute('data-base-url');
        const searchForm = document.querySelector('form');
    
        printButton.removeAttribute('target');
    
        let dataTable;
    
        if ($.fn.DataTable.isDataTable(tableElement)) {
            dataTable = $(tableElement).DataTable();
        } else {
            dataTable = $(tableElement).DataTable({
                destroy: true,
                language: {
                    url: "/sicomec/static/js/es-ES.json"
                },
                columns: [
                    { title: "Fecha", width: "10%" },
                    { title: "Movim.", width: "10%" },
                    { title: "Saldo", width: "10%" },
                    { title: "Placa", width: "10%" },
                    { title: "Tipo", width: "10%" },
                    { title: "Marca", width: "10%" },
                    { title: "Conductor", width: "20%" },
                    { title: "N° Vale", width: "10%" },
                    { title: "Código", width: "10%" }
                ]
            });
        }
    
        function showError(message) {
            Swal.fire({
                title: message,
                icon: 'error',
                timer: 2000,
                timerProgressBar: true,
                showConfirmButton: false,
            });
        }
    
        async function fetchOrderDetails(orderNumber) {
            try {
                const response = await fetch(`/sicomec/get_buy_order_uuid/${orderNumber}/`);
    
                if (!response.ok) {
                    switch (response.status) {
                        case 404:
                            showError('Orden de compra no encontrada');
                            break;
                        default:
                            showError('Error al buscar la orden de compra');
                    }
                    return null;
                }
    
                const data = await response.json();
                return data.uuid;
            } catch (error) {
                showError('Error al buscar la orden de compra');
                return null;
            }
        }
    
        async function updateOrderDetails(orderNumber) {
            if (!/^\d{1,7}(GP|GR|DS)$/.test(orderNumber)) {
                showError('Orden de compra inválida');
                clearFields();
                return;
            }
    
            const uuid = await fetchOrderDetails(orderNumber);
    
            if (!uuid) {
                clearFields();
                return;
            }
    
            try {
                const detailsResponse = await fetch(`/sicomec/get_buy_order_details/${uuid}`);
                const details = await detailsResponse.json();
    
                userAreaField.value = details.user_area || '';
                fueltapField.value = details.fueltap || '';
                fuelField.value = details.fuel || '';
                stockField.value = details.stock || '';
                residueField.value = details.residue || '';
    
                printButton.href = `${baseUrl}${uuid}/`;
                printButton.setAttribute('target', '_blank');
    
                const fuelOrdersResponse = await fetch(`/sicomec/get_fuel_orders/${uuid}`);
                const fuelOrdersData = await fuelOrdersResponse.json();
    
                dataTable.clear();
    
                if (fuelOrdersData.fuel_orders) {
                    fuelOrdersData.fuel_orders.forEach(fuel_order => {
                        dataTable.row.add([
                            fuel_order.date,
                            `<span>${fuel_order.fuel_return ? "+" : "-"}${fuel_order.quantity}</span>`,
                            fuel_order.residue,
                            fuel_order.plate__plate || "",
                            fuel_order.vehicle || "",
                            fuel_order.brand || "",
                            `${fuel_order.driver__name || ""} ${fuel_order.driver__last_name || ""}`,
                            fuel_order.voucher,
                            fuel_order.code
                        ]).draw();
                    });
                }
            } catch (error) {
                showError('Error al procesar los detalles de la orden');
                printButton.href = '#';
                printButton.removeAttribute('target');
            }
        }
    
        function clearFields() {
            userAreaField.value = '';
            fueltapField.value = '';
            fuelField.value = '';
            stockField.value = '';
            residueField.value = '';
            dataTable.clear().draw();
            printButton.href = '#';
            printButton.removeAttribute('target');
        }
    
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const orderNumber = orderInput.value.trim();
            if (orderNumber) {
                updateOrderDetails(orderNumber);
            } else {
                clearFields();
            }
        });
    
        printButton.addEventListener('click', function(event) {
            if (printButton.href === '#') {
                event.preventDefault();
            }
        });

    });
