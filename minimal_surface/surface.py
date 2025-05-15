"""
Surface calculation module for minimal surfaces.

This module provides functions to calculate coordinates for various
minimal surfaces using Weierstrass-type representations.
"""

import numpy as np
from typing import Tuple, Union, Optional
from pyweierstrass.weierstrass import wp, wpprime, wzeta, omega_from_g
from scipy.special import beta
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor

# Vectorized version of Weierstrass functions for better performance
def vectorized_wp(z, omega):
    return np.vectorize(lambda z_val: wp(z_val, omega))(z)

def vectorized_wpprime(z, omega):
    return np.vectorize(lambda z_val: wpprime(z_val, omega))(z)

def vectorized_wzeta(z, omega):
    return np.vectorize(lambda z_val: wzeta(z_val, omega))(z)

def chen_gackstatter_surface(
    r: np.ndarray, 
    theta: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the Chen-Gackstatter minimal surface coordinates.
    
    The Chen-Gackstatter surface is a complete minimal surface of finite total
    curvature with genus 1 and 3 embedded flat ends. It can be viewed as a
    generalization of Enneper's surface with a handle.
    
    Parameters
    ----------
    r : np.ndarray
        Radial distance parameter for the Chen-Gackstatter surface.
    theta : np.ndarray
        Angular parameter for the Chen-Gackstatter surface.
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        X, Y, Z coordinates of the Chen-Gackstatter surface.
    """
    # Define parameters for the Weierstrass elliptic functions
    g2 = (beta(1/4, 1/4) / 2)**4
    g3 = 0.0  # For the Chen-Gackstatter surface, g₃ = 0
    
    # Calculate the half-periods of the elliptic functions
    omega = omega_from_g(g2, g3)
    
    # Initialize arrays for X, Y, Z coordinates
    X = np.zeros_like(r, dtype=float)  # Explicitly use float type
    Y = np.zeros_like(r, dtype=float)
    Z = np.zeros_like(r, dtype=float)
    
    # Calculate Weierstrass functions for each point in the grid
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            # Convert polar to complex coordinates
            z = r[i, j] * np.exp(1j * theta[i, j])
            
            # Calculate Weierstrass functions at point z
            w_p = wp(z, omega)  # Weierstrass p-function
            w_p_prime = wpprime(z, omega)  # Derivative of p-function
            w_zeta = wzeta(z, omega)  # Weierstrass zeta function
            
            # Calculate surface coordinates using the Chen-Gackstatter parametrization
            # Explicitly take real/imaginary parts to ensure we have float values
            X[i, j] = float(np.real(np.pi * z - w_zeta - np.pi / g2 * w_p_prime))
            Y[i, j] = float(np.imag(np.pi * z + w_zeta - np.pi / g2 * w_p_prime))
            Z[i, j] = float(np.real(w_p) * np.sqrt(6 * np.pi / g2))
    
    return X, Y, Z

def process_chunk(chunk_data):
    r_chunk, theta_chunk, omega, g2 = chunk_data
    result_X = np.zeros_like(r_chunk)
    result_Y = np.zeros_like(r_chunk)
    result_Z = np.zeros_like(r_chunk)
    
    for i in range(r_chunk.shape[0]):
        for j in range(r_chunk.shape[1]):
            z = r_chunk[i, j] * np.exp(1j * theta_chunk[i, j])
            w_p = wp(z, omega)
            w_p_prime = wpprime(z, omega)
            w_zeta = wzeta(z, omega)
            
            result_X[i, j] = np.real(np.pi * z - w_zeta - np.pi / g2 * w_p_prime)
            result_Y[i, j] = np.imag(np.pi * z + w_zeta - np.pi / g2 * w_p_prime)
            result_Z[i, j] = np.sqrt(6 * np.pi / g2) * np.real(w_p)
    
    return (result_X, result_Y, result_Z)

def chen_gackstatter_surface_parallel(r, theta, num_processes=4):
    g2 = (beta(1/4, 1/4) / 2)**4
    g3 = 0.0
    omega = omega_from_g(g2, g3)
    
    # Split the grid into chunks
    chunks = []
    chunk_size = r.shape[0] // num_processes
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else r.shape[0]
        chunks.append((r[start:end], theta[start:end], omega, g2))
    
    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(process_chunk, chunks))
    
    # Combine results
    X = np.vstack([res[0] for res in results])
    Y = np.vstack([res[1] for res in results])
    Z = np.vstack([res[2] for res in results])
    
    return X, Y, Z

def enneper_surface(
    u: np.ndarray, 
    v: np.ndarray, 
    n: int = 1
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate Enneper's minimal surface coordinates.
    
    Parameters
    ----------
    u : np.ndarray
        First parameter for the surface.
    v : np.ndarray
        Second parameter for the surface.
    n : int, optional
        Order of the surface, by default 1.
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        X, Y, Z coordinates of Enneper's surface.
    """
    # Calculate the coordinates for Enneper's surface (vectorized)
    X = u - (u**(2*n+1))/(2*n+1) + u*(v**2)
    Y = v - (v**(2*n+1))/(2*n+1) + v*(u**2)
    Z = u**2 - v**2
    
    return X, Y, Z