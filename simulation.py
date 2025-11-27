"""
主模擬循環模塊
Main simulation loop module
"""
import numpy as np
from constants import DT, SINR_THRESHOLD_DB
from channel import Channel
from ground_terminal import GroundTerminal
from satellite import Satellite
from uav_swarm import UAVSwarm


class Simulation:
    """模擬主類別"""
    
    def __init__(self, satellites, uav_swarm, ground_terminals, 
                 t_start=0.0, t_end=3600.0, dt=DT):
        """
        初始化模擬
        Initialize simulation
        
        :param satellites: 衛星列表
        :param uav_swarm: 無人機蜂群實例
        :param ground_terminals: 地面終端列表
        :param t_start: 模擬開始時間 (秒)
        :param t_end: 模擬結束時間 (秒)
        :param dt: 時間步長 (秒)
        """
        self.satellites = satellites
        self.uav_swarm = uav_swarm
        self.ground_terminals = ground_terminals
        self.t_start = t_start
        self.t_end = t_end
        self.dt = dt
        
        self.channel = Channel()
        self.results = []
    
    def run(self, enable_optimization=True):
        """
        運行模擬主循環
        Run main simulation loop
        
        :param enable_optimization: 是否啟用無人機優化
        :return: 模擬結果列表
        """
        print("=" * 60)
        print("開始模擬：無人機蜂群對 LEO 衛星的電磁壓制")
        print("=" * 60)
        print(f"模擬時間範圍: {self.t_start:.0f} - {self.t_end:.0f} 秒")
        print(f"時間步長: {self.dt:.0f} 秒")
        print(f"衛星數量: {len(self.satellites)}")
        print(f"無人機數量: {self.uav_swarm.num_uavs}")
        print(f"地面終端數量: {len(self.ground_terminals)}")
        print("=" * 60)
        
        time_steps = np.arange(self.t_start, self.t_end, self.dt)
        
        for step_idx, current_time in enumerate(time_steps):
            # --- 運動更新 ---
            satellite_positions = []
            satellite_params_list = []
            
            for sat in self.satellites:
                sat_pos = sat.update_position(current_time)
                satellite_positions.append(sat_pos)
                satellite_params_list.append(sat.get_tx_parameters())
            
            # 假設所有衛星參數相同，取第一個
            satellite_params = satellite_params_list[0] if satellite_params_list else None
            
            # --- 蜂群策略 (移動和優化) ---
            # 每步都更新位置（飛行或優化）
            jammed_count = self.uav_swarm.update_formation(
                self.ground_terminals,
                satellite_positions,
                satellite_params,
                self.channel,
                dt=self.dt
            )
            if step_idx % 10 == 0:
                print(f"時間 {current_time:.0f}s: {jammed_count}/{len(self.ground_terminals)} 個終端被阻斷")
            
            # --- 鏈路計算 ---
            step_results = {
                'time': current_time,
                'satellite_positions': satellite_positions.copy(),
                'uav_positions': self.uav_swarm.uav_positions_ecef.copy(),
                'gt_results': []
            }
            
            avg_sinr = 0.0
            jammed_count = 0
            
            for gt in self.ground_terminals:
                # a. 衛星訊號計算 (P_rx)
                P_rx_list = []
                for sat_pos in satellite_positions:
                    P_rx, _ = self.channel.calculate_link_budget(
                        tx_coord=sat_pos,
                        rx_coord=gt.get_ecef_coord(),
                        tx_power_dbw=satellite_params[0],
                        tx_gain_db=satellite_params[1],
                        rx_gain_db=gt.G_R_dB,
                        frequency_hz=satellite_params[2]
                    )
                    P_rx_list.append(P_rx)
                
                P_rx = max(P_rx_list)  # 假設終端鎖定最強的衛星訊號
                
                # b. 干擾訊號計算 (J_total)
                J_total_W = 0.0
                jam_power, jam_gain, jam_freq = self.uav_swarm.get_jammer_params()
                
                for uav_coord in self.uav_swarm.uav_positions_ecef:
                    P_rx_uav, _ = self.channel.calculate_link_budget(
                        tx_coord=uav_coord,
                        rx_coord=gt.get_ecef_coord(),
                        tx_power_dbw=jam_power,
                        tx_gain_db=jam_gain,
                        rx_gain_db=gt.G_R_dB,
                        frequency_hz=jam_freq
                    )
                    J_total_W += 10**(P_rx_uav / 10)
                
                J_total_dbw = 10 * np.log10(J_total_W) if J_total_W > 0 else -float('inf')
                
                # c. 性能評估
                sinr = gt.calculate_sinr(P_rx, J_total_dbw)
                is_jammed = gt.is_jammed(sinr, SINR_THRESHOLD_DB)
                
                avg_sinr += sinr
                if is_jammed:
                    jammed_count += 1
                
                step_results['gt_results'].append({
                    'gt_id': gt.id,
                    'sinr': sinr,
                    'p_rx': P_rx,
                    'j_total': J_total_dbw,
                    'is_jammed': is_jammed
                })
            
            avg_sinr /= len(self.ground_terminals)
            jammed_rate = jammed_count / len(self.ground_terminals)
            
            step_results['avg_sinr'] = avg_sinr
            step_results['jammed_count'] = jammed_count
            step_results['jammed_rate'] = jammed_rate
            
            self.results.append(step_results)
            
            # 進度顯示
            if step_idx % 10 == 0:
                print(f"時間 {current_time:6.0f}s | 平均 SINR: {avg_sinr:6.2f} dB | "
                     f"阻斷率: {jammed_rate*100:5.1f}% ({jammed_count}/{len(self.ground_terminals)})")
        
        print("=" * 60)
        print("模擬完成！")
        print("=" * 60)
        
        return self.results
    
    def get_summary_statistics(self):
        """獲取模擬統計摘要"""
        if not self.results:
            return None
        
        avg_sinr_list = [r['avg_sinr'] for r in self.results]
        jammed_rate_list = [r['jammed_rate'] for r in self.results]
        
        return {
            'avg_sinr_mean': np.mean(avg_sinr_list),
            'avg_sinr_std': np.std(avg_sinr_list),
            'avg_sinr_min': np.min(avg_sinr_list),
            'avg_sinr_max': np.max(avg_sinr_list),
            'jammed_rate_mean': np.mean(jammed_rate_list),
            'jammed_rate_max': np.max(jammed_rate_list),
            'total_steps': len(self.results)
        }

