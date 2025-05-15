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
    const colormapSelect = document.getElementById('colormap');
    
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
    
    // Handle generate button click
    if (generateBtn) {
        generateBtn.addEventListener('click', function() {
            // Show loading indicator
            loadingIndicator.style.display = 'flex';
            
            // Get form data
            const formData = {
                surface_type: surfaceTypeSelect.value,
                resolution: parseInt(resolutionSlider.value),
                order: parseInt(document.getElementById('order').value || 1)
            };
            
            // Send AJAX request to get surface data
            fetch('/generate_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                loadingIndicator.style.display = 'none';
                
                if (data.error) {
                    console.error('Error:', data.error);
                    surfaceDisplay.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                    return;
                }
                
                // Create the 3D surface plot with Plotly
                const plotData = [{
                    type: 'surface',
                    x: data.x,
                    y: data.y,
                    z: data.z,
                    colorscale: colormapSelect.value,
                    lighting: {
                        ambient: 0.8,
                        diffuse: 0.8,
                        roughness: 0.5,
                        specular: 0.8,
                        fresnel: 0.8
                    },
                    contours: {
                        x: { show: true, width: 1 },
                        y: { show: true, width: 1 },
                        z: { show: true, width: 1 }
                    }
                }];
                
                const layout = {
                    title: data.title,
                    autosize: true,
                    margin: { l: 0, r: 0, b: 0, t: 30 },
                    scene: {
                        camera: {
                            eye: { x: 1.5, y: 1.5, z: 1.5 }
                        },
                        xaxis: { showticklabels: false },
                        yaxis: { showticklabels: false },
                        zaxis: { showticklabels: false }
                    }
                };
                
                const config = {
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                    toImageButtonOptions: {
                        format: 'png',
                        filename: data.title.replace(/\s+/g, '_').toLowerCase(),
                        height: 800,
                        width: 800,
                        scale: 2
                    }
                };
                
                Plotly.newPlot(surfaceDisplay, plotData, layout, config);
            })
            .catch(error => {
                console.error('Error:', error);
                loadingIndicator.style.display = 'none';
                surfaceDisplay.innerHTML = '<p class="error">An error occurred. Please try again.</p>';
            });
        });
    }
});