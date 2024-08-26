
document.addEventListener('DOMContentLoaded', function() {

    const notificationButtonContainer = document.getElementById('notificationButtonContainer');
    const notificationBadge = document.getElementById('notificationBadge');

    function updateNotificationCount() {
        fetch('/sicomec/notification/count')
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            notificationBadge.textContent = count;
            if (count > 0) {
            notificationButtonContainer.style.display = 'block'; 
            } else {
            notificationButtonContainer.style.display = 'none';  
            }
        })
        .catch(error => console.error('Error fetching notification count:', error));
    }

    updateNotificationCount();

    // Update every 60 seconds
    // setInterval(updateNotificationCount, 60000); 

});
