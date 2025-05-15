document.addEventListener('DOMContentLoaded', function() {
    // Update resolution value display
    const resolutionSlider = document.getElementById('resolution');
    const resolutionValue = document.getElementById('resolution_value');
    
    if (resolutionSlider && resolutionValue) {
        resolutionSlider.addEventListener('input', function() {
            resolutionValue.textContent = this.value;
        });
    }
});