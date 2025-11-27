"""
無人機蜂群模塊：干擾優化策略
UAV Swarm module: jamming optimization strategy
"""
import numpy as np
from constants import (UAV_ALTITUDE, UAV_JAM_POWER_DBW,
                       UAV_JAM_GAIN_DB, UAV_FREQ)
from utils import geo_to_ecef


class UAVSwarm:
    """無人機蜂群類別"""
    
    def __init__(self, num_uavs, initial_lat_range=(22.0, 25.0),
                 initial_lon_range=(119.0, 122.0), deployment_pattern='grid'):
        """
        初始化無人機蜂群
        Initialize UAV swarm
        
        :param num_uavs: 無人機數量
        :param initial_lat_range: 初始緯度範圍 (台灣附近)
        :param initial_lon_range: 初始經度範圍 (台灣附近)
        :param deployment_pattern: 部署模式 ('grid', 'random', 'line')
        """
        self.num_uavs = num_uavs
        
        # 狀態：每架無人機的 (緯度, 經度) - 簡化優化空間
        lat_min, lat_max = initial_lat_range
        lon_min, lon_max = initial_lon_range
        
        if deployment_pattern == 'grid':
            # 網格部署：在台灣海峽形成規律陣型
            # 計算網格尺寸
            grid_size = int(np.ceil(np.sqrt(num_uavs)))
            lat_step = (lat_max - lat_min) / (grid_size + 1)
            lon_step = (lon_max - lon_min) / (grid_size + 1)
            
            positions = []
            count = 0
            for i in range(grid_size):
                for j in range(grid_size):
                    if count >= num_uavs:
                        break
                    lat = lat_min + (i + 1) * lat_step
                    lon = lon_min + (j + 1) * lon_step
                    positions.append([lat, lon])
                    count += 1
                if count >= num_uavs:
                    break
            
            self.uav_positions_geo = np.array(positions)
            
        elif deployment_pattern == 'line':
            # 線性部署：沿台灣西海岸形成防線
            lat_step = (lat_max - lat_min) / (num_uavs + 1)
            positions = []
            for i in range(num_uavs):
                lat = lat_min + (i + 1) * lat_step
                lon = lon_min + (lon_max - lon_min) * 0.3  # 靠近台灣西海岸
                positions.append([lat, lon])
            self.uav_positions_geo = np.array(positions)
            
        else:  # 'random'
            # 隨機部署
            np.random.seed(42)  # 固定種子以確保可重現性
            self.uav_positions_geo = np.random.rand(num_uavs, 2) * [
                lat_max - lat_min, lon_max - lon_min
            ] + [lat_min, lon_min]
        
        # 輔助：存儲無人機在 ECEF 座標下的位置
        self.uav_positions_ecef = self._geo_to_ecef(self.uav_positions_geo)
    
    def _geo_to_ecef(self, geo_coords):
        """將地理座標 (lat, lon) 轉換為 ECEF 座標 (x, y, z)"""
        ecef_coords = []
        for lat, lon in geo_coords:
            coord = geo_to_ecef(lat, lon, UAV_ALTITUDE)
            ecef_coords.append(coord)
        return np.array(ecef_coords)
    
    def get_jammer_coord(self, uav_index):
        """返回特定無人機的 ECEF 座標"""
        return self.uav_positions_ecef[uav_index]
    
    def get_jammer_params(self):
        """返回無人機的發射參數，假設所有無人機參數相同"""
        return UAV_JAM_POWER_DBW, UAV_JAM_GAIN_DB, UAV_FREQ
    
    def update_formation(self, ground_terminals, satellite_positions,
                         satellite_params, channel_module):
        """
        根據當前環境，使用簡化優化策略調整無人機的位置，以最大化干擾效果
        Update UAV formation using simplified optimization strategy
        
        :param ground_terminals: 地面終端列表
        :param satellite_positions: 衛星位置列表 (ECEF)
        :param satellite_params: 衛星參數元組 (tx_power, tx_gain, freq)
        :param channel_module: Channel 模塊實例
        :return: 被阻斷的地面終端數量
        """
        # 1. 計算當前適應度 (被阻斷的終端數量)
        current_fitness = self._calculate_fitness(
            ground_terminals, satellite_positions,
            satellite_params, channel_module
        )
        
        # 2. 簡化的優化策略：在當前位置附近隨機搜索
        # 嘗試小幅調整位置
        step_size = 0.1  # 度
        new_geo_positions = self.uav_positions_geo + (
            np.random.rand(self.num_uavs, 2) - 0.5
        ) * step_size
        
        # 限制在合理範圍內
        new_geo_positions[:, 0] = np.clip(
            new_geo_positions[:, 0], 20.0, 26.0)
        new_geo_positions[:, 1] = np.clip(
            new_geo_positions[:, 1], 118.0, 123.0)
        
        # 臨時更新位置以測試適應度
        temp_ecef = self._geo_to_ecef(new_geo_positions)
        old_ecef = self.uav_positions_ecef.copy()
        self.uav_positions_ecef = temp_ecef
        
        new_fitness = self._calculate_fitness(
            ground_terminals, satellite_positions,
            satellite_params, channel_module
        )
        
        # 3. 如果新位置更好，則接受；否則恢復原位置
        if new_fitness >= current_fitness:
            self.uav_positions_geo = new_geo_positions
            # 位置已更新
        else:
            self.uav_positions_ecef = old_ecef
            new_fitness = current_fitness
        
        return new_fitness
    
    def _calculate_fitness(self, ground_terminals, satellite_positions,
                           satellite_params, channel_module):
        """
        計算適應度函數：被阻斷的地面終端數量
        Calculate fitness: number of jammed terminals
        """
        tx_power_sat, tx_gain_sat, freq_sat = satellite_params
        jammed_count = 0
        
        for gt in ground_terminals:
            # a. 計算衛星訊號 P_rx (選擇最近的衛星)
            P_rx_sat_list = []
            for sat_pos in satellite_positions:
                P_rx, _ = channel_module.calculate_link_budget(
                    tx_coord=sat_pos,
                    rx_coord=gt.get_ecef_coord(),
                    tx_power_dbw=tx_power_sat,
                    tx_gain_db=tx_gain_sat,
                    rx_gain_db=gt.G_R_dB,
                    frequency_hz=freq_sat
                )
                P_rx_sat_list.append(P_rx)
            
            P_rx = max(P_rx_sat_list)  # 假設終端鎖定最強的衛星訊號
            
            # b. 計算總干擾 J_total
            J_total_W = 0.0
            jam_power, jam_gain, jam_freq = self.get_jammer_params()
            
            for uav_coord in self.uav_positions_ecef:
                P_rx_uav, _ = channel_module.calculate_link_budget(
                    tx_coord=uav_coord,
                    rx_coord=gt.get_ecef_coord(),
                    tx_power_dbw=jam_power,
                    tx_gain_db=jam_gain,
                    rx_gain_db=gt.G_R_dB,
                    frequency_hz=jam_freq
                )
                # 轉換為 W 後累加
                J_total_W += 10**(P_rx_uav / 10)
            
            # c. 計算 SINR
            if J_total_W > 0:
                J_total_dbw = 10 * np.log10(J_total_W)
            else:
                J_total_dbw = -float('inf')
            sinr = gt.calculate_sinr(P_rx, J_total_dbw)
            
            if gt.is_jammed(sinr):
                jammed_count += 1
        
        return jammed_count

