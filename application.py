"""
Minimal Surface Web Application

A Flask web application for visualizing minimal surfaces.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import numpy as np
import os

# Initialize Flask application
application = Flask(__name__)  # 'application' is required by Elastic Beanstalk

# Import surface functions from minimal_surface package
from minimal_surface.surface import chen_gackstatter_surface_parallel, enneper_surface

@application.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@application.route('/generate_data', methods=['POST'])
def generate_data():
    """Generate surface data and return as JSON for client-side rendering."""
    # Get parameters from form
    surface_type = request.json.get('surface_type', 'chen-gackstatter')
    resolution = int(request.json.get('resolution', 50))
    order = int(request.json.get('order', 1))  # For Enneper surface
    
    try:
        # Generate surface based on type
        if surface_type == 'chen-gackstatter':
            # Create a grid of points in polar coordinates
            r = np.linspace(0.2, 0.8, resolution)
            theta = np.linspace(-np.pi, np.pi, resolution)
            r, theta = np.meshgrid(r, theta)
            
            # Generate the surface
            X, Y, Z = chen_gackstatter_surface_parallel(r, theta)
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
        
        # Ensure arrays are serializable (convert to Python lists)
        # This handles complex numbers by ensuring we only send real values
        x_list = X.tolist()
        y_list = Y.tolist()
        z_list = Z.tolist()
        
        return jsonify({
            "x": x_list,
            "y": y_list,
            "z": z_list,
            "title": title
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0', port=5000)