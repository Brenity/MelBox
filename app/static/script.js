document.addEventListener("DOMContentLoaded", function() {
    // Get the flash message container element
    const flashMessagesContainer = document.getElementById('flash-messages');
    const flashMessageCount = flashMessagesContainer.getAttribute('data-flash');

    // Check if there are flash messages
    if (flashMessageCount > 0) {
        // Show the flash messages container and fade it in
        flashMessagesContainer.style.display = 'block'; // Make the container visible
        flashMessagesContainer.style.opacity = 1; // Fade in effect
    }
});
