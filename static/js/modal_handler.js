// Modal handler for custom Streamlit component
(function() {
    // Listen for messages from the modal component
    window.addEventListener('message', function(event) {
        if (event.data.type === 'closeModal') {
            // Close the modal
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: { action: 'close' }
            }, '*');
        } else if (event.data.type === 'cancelForm') {
            // Cancel the form
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: { action: 'cancel' }
            }, '*');
        } else if (event.data.type === 'submitForm') {
            // Submit the form with data
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: { 
                    action: 'submit',
                    data: event.data.data
                }
            }, '*');
        }
    });
})(); 