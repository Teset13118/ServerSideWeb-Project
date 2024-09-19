
document.addEventListener('DOMContentLoaded', function() {
    const activityType = document.getElementById('id_activity_type');
    const platformContainer = document.getElementById('platform_container');
    const locationContainer = document.getElementById('location_container');

    function updateVisibility() {
        const selectedType = activityType.value;
        if (selectedType === 'online') {
            platformContainer.style.display = 'block';
            locationContainer.style.display = 'none';
        } else if (selectedType === 'onsite') {
            platformContainer.style.display = 'none';
            locationContainer.style.display = 'block';
        } else if (selectedType === 'hybrid') {
            platformContainer.style.display = 'block';
            locationContainer.style.display = 'block';
        }
    }

    activityType.addEventListener('change', updateVisibility);
    updateVisibility();  // Initial check on page load
});