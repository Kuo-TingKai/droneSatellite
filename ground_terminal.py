"""
地面終端模塊：SINR 計算和性能評估
Ground Terminal module: SINR calculation and performance evaluation
"""
import numpy as np
from constants import SYSTEM_BANDWIDTH, NOISE_TEMP, SINR_THRESHOLD_DB
from utils import calculate_noise_power_dbw, geo_to_ecef


class GroundTerminal:
    """地面使用者終端類別"""
    
    def __init__(self, id, latitude, longitude, rx_gain_db,
                 system_noise_temp_k=NOISE_TEMP,
                 bandwidth_hz=SYSTEM_BANDWIDTH):
        """
        初始化地面使用者終端
        Initialize ground terminal
        
        :param id: 終端 ID
        :param latitude: 緯度 (度)
        :param longitude: 經度 (度)
        :param rx_gain_db: 接收天線增益 (dB)
        :param system_noise_temp_k: 系統噪聲溫度 (K)
        :param bandwidth_hz: 接收頻寬 (Hz)
        """
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.G_R_dB = rx_gain_db
        
        # 預計算熱噪聲功率，這是恆定的
        self.N_dBW = calculate_noise_power_dbw(
            system_noise_temp_k, bandwidth_hz)
        
        # 預計算 ECEF 座標
        self.ecef_coord = geo_to_ecef(latitude, longitude, altitude=0.0)
    
    def get_ecef_coord(self):
        """返回 ECEF 座標"""
        return self.ecef_coord
    
    def calculate_sinr(self, p_rx_dbw, j_total_dbw):
        """
        計算訊號、干擾與噪聲比 (SINR)
        Calculate Signal-to-Interference-plus-Noise Ratio
        
        :param p_rx_dbw: 接收到的有效訊號功率 (dBW)
        :param j_total_dbw: 接收到的總干擾功率 (dBW)
        :return: SINR (dB)
        """
        # 1. 轉換 dBW 到 W (線性功率)
        P_rx_W = 10**(p_rx_dbw / 10)
        J_total_W = 10**(j_total_dbw / 10)
        N_W = 10**(self.N_dBW / 10)
        
        # 2. 計算 SINR (線性)
        if (J_total_W + N_W) <= 0:
            return float('inf')
        
        sinr_linear = P_rx_W / (J_total_W + N_W)
        
        # 3. 轉換 SINR 回 dB
        if sinr_linear > 0:
            sinr_dB = 10 * np.log10(sinr_linear)
        else:
            sinr_dB = -float('inf')
        
        return sinr_dB
    
    def is_jammed(self, sinr_dB,
                  threshold_dB=SINR_THRESHOLD_DB):
        """
        判斷通訊是否被有效阻斷 (SINR 低於臨界值)
        Check if communication is effectively jammed
        
        :param sinr_dB: SINR 值 (dB)
        :param threshold_dB: 阻斷閾值 (dB)
        :return: True if jammed, False otherwise
        """
        return sinr_dB < threshold_dB

