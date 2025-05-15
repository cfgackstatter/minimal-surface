document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const form = document.getElementById('surface-form');
    const surfaceTypeSelect = document.getElementById('surface_type');
    const resolutionSlider = document.getElementById('resolution');
    const resolutionValue = document.getElementById('resolution_value');
    const enneperOptions = document.getElementById('enneper-options');
    const generateBtn = document.getElementById('generate-btn');
    const surfaceDisplay = document.getElementById('surface-display');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Update resolution value display
    if (resolutionSlider && resolutionValue) {
        resolutionSlider.addEventListener('input', function() {
            resolutionValue.textContent = this.value;
        });
    }
    
    // Show/hide Enneper options based on surface type selection
    if (surfaceTypeSelect && enneperOptions) {
        surfaceTypeSelect.addEventListener('change', function() {
            if (this.value === 'enneper') {
                enneperOptions.style.display = 'block';
            } else {
                enneperOptions.style.display = 'none';
            }
        });
    }
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading indicator
            loadingIndicator.style.display = 'flex';
            
            // Get form data
            const formData = new FormData(form);
            
            // Send AJAX request
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(html => {
                // Extract the image from the response
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const imgSrc = doc.querySelector('img').src;
                
                // Create and display the image
                const img = document.createElement('img');
                img.src = imgSrc;
                img.alt = 'Generated Minimal Surface';
                img.onload = function() {
                    // Hide loading indicator
                    loadingIndicator.style.display = 'none';
                    
                    // Update the display
                    surfaceDisplay.innerHTML = '';
                    surfaceDisplay.appendChild(img);
                };
            })
            .catch(error => {
                console.error('Error:', error);
                loadingIndicator.style.display = 'none';
                surfaceDisplay.innerHTML = '<p class="error">An error occurred. Please try again.</p>';
            });
        });
    }
});