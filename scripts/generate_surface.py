import numpy as np
from minimal_surface.surface import chen_gackstatter_surface
from minimal_surface.visualization import plot_surface

def main():
    # Create a grid of points in polar coordinates
    r = np.linspace(1/5, 4/5, 20)
    theta = np.linspace(-np.pi, np.pi, 20)
    r, theta = np.meshgrid(r, theta)

    # Generate the surface
    X, Y, Z = chen_gackstatter_surface(r, theta)

    # Plot and save the surface
    plot_surface(
        X, Y, Z, 
        title='Chen-Gackstatter Minimal Surface',
        save_path='chen_gackstatter_surface.png',
        view_angles=(20, -20)
    )

if __name__ == "__main__":
    main()