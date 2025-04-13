import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_surface(X, Y, Z, title="Minimal Surface", save_path=None, view_angles=(20, -20)):
    """
    Create a 3D plot of a surface.
    
    Parameters
    ----------
    X, Y, Z : numpy.ndarray
        Coordinates of the surface.
    title : str, optional
        Title of the plot.
    save_path : str, optional
        Path to save the figure. If None, the figure is not saved.
    view_angles : tuple, optional
        (elevation, azimuth) viewing angles.
        
    Returns
    -------
    fig, ax
        Figure and axis objects.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(X, Y, Z, color='white', edgecolor='black', shade=False)

    # Customize the plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes

    # Remove axes and grid
    ax.set_axis_off()

    # Change the view angle
    ax.view_init(elev=view_angles[0], azim=view_angles[1])

    # Save the figure if a path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, transparent=False, 
                   bbox_inches='tight', pad_inches=0.1)
        print(f"Surface visualization saved to '{save_path}'")
        
    return fig, ax