"""
電磁波傳播模型模塊
Electromagnetic wave propagation model (Channel)
"""
import numpy as np
from constants import C_LIGHT, EARTH_RADIUS


class Channel:
    """電磁波傳播計算類別"""
    
    @staticmethod
    def calc_distance_3d(coord1, coord2):
        """
        計算兩個 3D 座標點之間的歐幾里得距離 (m)
        Calculate Euclidean distance between two 3D coordinates
        
        :param coord1: (x, y, z) tuple/list/array
        :param coord2: (x, y, z) tuple/list/array
        :return: 距離 (米)
        """
        coord1 = np.array(coord1)
        coord2 = np.array(coord2)
        return np.linalg.norm(coord1 - coord2)
    
    @staticmethod
    def calc_free_space_path_loss_db(distance_m, frequency_hz):
        """
        計算自由空間路徑損耗 (FSPL) (dB)
        Calculate Free-Space Path Loss
        
        FSPL = 20 * log10(4 * pi * d * f / c)
        
        :param distance_m: 距離 (米)
        :param frequency_hz: 頻率 (Hz)
        :return: 路徑損耗 (dB)
        """
        if distance_m <= 0:
            return float('inf')
        
        ratio = (4 * np.pi * distance_m * frequency_hz) / C_LIGHT
        fspl_db = 20 * np.log10(ratio)
        return fspl_db
    
    @staticmethod
    def get_atmospheric_loss_db(distance_m, altitude_m):
        """
        估算大氣衰減 (L_atm) (dB)
        Estimate atmospheric attenuation
        
        :param distance_m: 距離 (米)
        :param altitude_m: 發射源高度 (米)
        :return: 大氣衰減 (dB)
        """
        if altitude_m > 100000.0:  # 衛星到地面
            # 簡化：假設在 X/Ku 頻段，天頂方向為 1-3 dB
            base_loss = 2.0  # dB
            loss = base_loss * (distance_m / 600e3)
            return np.clip(loss, 1.0, 5.0)  # 限制在 1 dB 到 5 dB 之間
        else:  # 無人機到地面 (平流層到地面)
            # 距離短，主要損耗來自對流層底部，假設恆定小值
            return 0.5  # dB
    
    @staticmethod
    def calculate_link_budget(tx_coord, rx_coord, tx_power_dbw, tx_gain_db, 
                             rx_gain_db, frequency_hz):
        """
        計算完整的鏈路預算，得到接收功率 P_Rx (dBW)
        Calculate complete link budget
        
        P_Rx = P_Tx + G_Tx + G_Rx - L_FSPL - L_Atm
        
        :param tx_coord: 發射源座標 (x, y, z)
        :param rx_coord: 接收點座標 (x, y, z)
        :param tx_power_dbw: 發射功率 (dBW)
        :param tx_gain_db: 發射天線增益 (dB)
        :param rx_gain_db: 接收天線增益 (dB)
        :param frequency_hz: 頻率 (Hz)
        :return: (接收功率 P_Rx (dBW), 距離 (米))
        """
        # 1. 計算距離
        distance_m = Channel.calc_distance_3d(tx_coord, rx_coord)
        
        # 2. 計算路徑損耗
        fspl_db = Channel.calc_free_space_path_loss_db(distance_m, frequency_hz)
        
        # 3. 估算大氣衰減 (使用發射源高度進行判斷)
        tx_altitude = np.linalg.norm(tx_coord) - EARTH_RADIUS
        atm_loss_db = Channel.get_atmospheric_loss_db(distance_m, tx_altitude)
        
        # 4. 鏈路預算計算
        P_rx_dbw = (tx_power_dbw + 
                    tx_gain_db + 
                    rx_gain_db - 
                    fspl_db - 
                    atm_loss_db)
        
        return P_rx_dbw, distance_m

