"""
衛星模塊：LEO 衛星軌道計算 (SGP4)
Satellite module: LEO satellite orbit calculation using SGP4
"""
import datetime
import numpy as np
from skyfield.api import load, EarthSatellite
from constants import (SAT_TX_POWER_DBW, SAT_TX_GAIN_DB, SAT_FREQ,
                       SIM_START_TIME)


class Satellite:
    """LEO 衛星類別"""
    
    def __init__(self, name, tle_line1, tle_line2,
                 tx_power_dbw=SAT_TX_POWER_DBW,
                 tx_gain_db=SAT_TX_GAIN_DB,
                 frequency_hz=SAT_FREQ):
        """
        使用 TLE 數據初始化衛星實例
        Initialize satellite with TLE data
        
        :param name: 衛星名稱
        :param tle_line1: TLE 第一行
        :param tle_line2: TLE 第二行
        :param tx_power_dbw: 發射功率 (dBW)
        :param tx_gain_db: 發射天線增益 (dB)
        :param frequency_hz: 頻率 (Hz)
        """
        self.name = name
        
        # 載入時間刻度數據，並創建衛星物件
        ts = load.timescale()
        self.sat = EarthSatellite(tle_line1, tle_line2, name, ts)
        
        # 通訊參數
        self.tx_power_dbw = tx_power_dbw
        self.tx_gain_db = tx_gain_db
        self.frequency_hz = frequency_hz
        
        # 解析模擬開始時間
        self.t0 = datetime.datetime.strptime(
            SIM_START_TIME, "%Y-%m-%d %H:%M:%S")
        self.t0 = self.t0.replace(tzinfo=datetime.timezone.utc)
    
    def update_position(self, current_time):
        """
        根據當前時間計算衛星的 ECEF 座標
        Calculate satellite ECEF coordinates at current time
        
        :param current_time: 從模擬開始經過的秒數 (float)
        :return: ECEF 座標 (x, y, z) in meters
        """
        # 1. 創建時間物件
        current_dt = self.t0 + datetime.timedelta(seconds=current_time)
        
        # 載入 skyfield 的時間刻度
        ts = load.timescale()
        t = ts.utc(current_dt.year, current_dt.month, current_dt.day,
                   current_dt.hour, current_dt.minute, current_dt.second)
        
        # 2. 計算衛星在該時間的 ECEF 位置
        geocentric = self.sat.at(t)
        
        # 轉換為 ECEF 座標 (x, y, z) 和單位 (米)
        # ITRF (International Terrestrial Reference Frame) 就是 ECEF 座標系
        # itrf_xyz 返回的是 Distance 對象，需要轉換為米
        x_m, y_m, z_m = geocentric.itrf_xyz().m
        
        return np.array([x_m, y_m, z_m])
    
    def get_tx_parameters(self):
        """返回衛星的發射參數，供 Channel 模塊使用"""
        return self.tx_power_dbw, self.tx_gain_db, self.frequency_hz

