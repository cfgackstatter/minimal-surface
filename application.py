"""
Minimal Surface Web Application

A Flask web application for visualizing minimal surfaces.
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from minimal_surface.surface import chen_gackstatter_surface, enneper_surface
import matplotlib
matplotlib.use('Agg')  # Required for non-interactive backend

# Initialize Flask application
application = Flask(__name__)  # 'application' is required by Elastic Beanstalk

@application.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@application.route('/generate', methods=['POST'])
def generate_surface():
    """Generate a minimal surface based on form parameters."""
    # Get parameters from form
    surface_type = request.form.get('surface_type', 'chen-gackstatter')
    resolution = int(request.form.get('resolution', 50))
    colormap = request.form.get('colormap', '')
    order = int(request.form.get('order', 1))  # For Enneper surface
    
    if not colormap:
        colormap = None
    
    # Generate surface
    if surface_type == 'chen-gackstatter':
        # Create a grid of points in polar coordinates
        r = np.linspace(0.2, 0.8, resolution)
        theta = np.linspace(-np.pi, np.pi, resolution)
        r, theta = np.meshgrid(r, theta)
        
        # Generate the surface
        X, Y, Z = chen_gackstatter_surface(r, theta)
        title = 'Chen-Gackstatter Minimal Surface'
        
    elif surface_type == 'enneper':
        # Create a grid of points for Enneper surface
        u = np.linspace(-1.5, 1.5, resolution)
        v = np.linspace(-1.5, 1.5, resolution)
        u, v = np.meshgrid(u, v)
        
        # Generate the surface
        X, Y, Z = enneper_surface(u, v, n=order)
        title = f'Enneper Minimal Surface (Order {order})'
        
    else:
        return jsonify({"error": f"Surface type '{surface_type}' not implemented"}), 400
    
    # Create plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface with specified colormap or default style
    if colormap:
        norm = plt.Normalize(Z.min(), Z.max())
        surf = ax.plot_surface(
            X, Y, Z,
            cmap=plt.get_cmap(colormap),
            norm=norm,
            linewidth=0.5,
            antialiased=True
        )
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    else:
        surf = ax.plot_surface(
            X, Y, Z,
            color='white',
            edgecolor='black',
            shade=False
        )
    
    # Customize the plot
    ax.set_title(title, fontsize=14)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=30, azim=-30)
    
    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.1)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    
    # For AJAX requests, return just the image
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return f'<img src="data:image/png;base64,{plot_url}" alt="{title}">'
    
    # For regular requests, return the full template
    return render_template('surface.html', plot_url=plot_url)

# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0', port=5000)