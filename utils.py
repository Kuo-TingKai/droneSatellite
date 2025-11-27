"""
工具函數：座標轉換和輔助計算
Utility functions: coordinate conversion and helper calculations
"""
import numpy as np
from constants import EARTH_RADIUS, UAV_ALTITUDE


def geo_to_ecef(latitude, longitude, altitude=0.0):
    """
    將地理座標 (緯度, 經度, 高度) 轉換為 ECEF 座標 (x, y, z)
    Convert geographic coordinates to ECEF coordinates
    
    :param latitude: 緯度 (度)
    :param longitude: 經度 (度)
    :param altitude: 高度 (米)
    :return: ECEF 座標 (x, y, z) in meters
    """
    lat_rad = np.deg2rad(latitude)
    lon_rad = np.deg2rad(longitude)
    
    R = EARTH_RADIUS + altitude
    
    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)
    
    return np.array([x, y, z])


def ecef_to_geo(x, y, z):
    """
    將 ECEF 座標轉換為地理座標 (簡化版本)
    Convert ECEF coordinates to geographic coordinates (simplified)
    
    :param x, y, z: ECEF 座標 (米)
    :return: (latitude, longitude, altitude) in degrees and meters
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    altitude = r - EARTH_RADIUS
    
    latitude = np.rad2deg(np.arcsin(z / r))
    longitude = np.rad2deg(np.arctan2(y, x))
    
    return latitude, longitude, altitude


def calculate_noise_power_dbw(T_sys, B):
    """
    計算系統熱噪聲功率 N (單位：dBW)
    Calculate thermal noise power
    
    :param T_sys: 系統噪聲溫度 (K)
    :param B: 頻寬 (Hz)
    :return: 噪聲功率 (dBW)
    """
    from constants import K_BOLTZMANN
    
    noise_power_W = K_BOLTZMANN * T_sys * B
    noise_power_dBW = 10 * np.log10(noise_power_W) if noise_power_W > 0 else -float('inf')
    return noise_power_dBW

