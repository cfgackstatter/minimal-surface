import numpy as np
from pyweierstrass.weierstrass import wp, wpprime, wzeta, omega_from_g
from scipy.special import beta

def chen_gackstatter_surface(r, theta):
    """
    Chen-Gackstatter minimal surface.
    
    Parameters
    ----------
    r : float
        Parameter for the Chen-Gackstatter surface.
    theta : float
        Parameter for the Chen-Gackstatter surface.
        
    Returns
    -------
    tuple
        Coordinates of the Chen-Gackstatter surface.
    """
    # Define parameters for the Weierstrass elliptic functions
    g2 = (beta(1/4, 1/4) / 2)**4
    g3 = 0.0
    omega = omega_from_g(g2, g3)

    # Initialize arrays for X, Y, Z
    X = np.zeros_like(r)
    Y = np.zeros_like(r)
    Z = np.zeros_like(r)

    # Calculate Weierstrass functions for each point
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            z = r[i, j] * np.exp(1j * theta[i, j])
            w_p = wp(z, omega)
            w_p_prime = wpprime(z, omega)
            w_zeta = wzeta(z, omega)

            X[i, j] = np.real(np.pi * z - w_zeta - np.pi / g2 * w_p_prime)
            Y[i, j] = np.imag(np.pi * z + w_zeta - np.pi / g2 * w_p_prime)
            Z[i, j] = np.sqrt(6 * np.pi / g2) * np.real(w_p)

    return X, Y, Z