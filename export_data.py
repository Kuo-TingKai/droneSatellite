"""
數據導出模塊：將模擬結果導出為 JSON 格式供 Web 視覺化使用
Data export module: Export simulation results to JSON for web visualization
"""
import json
import numpy as np
from datetime import datetime


def export_simulation_data(results, satellites, uav_swarm, ground_terminals,
                         output_file='simulation_data.json'):
    """
    導出模擬數據為 JSON 格式
    Export simulation data to JSON format
    
    :param results: 模擬結果列表
    :param satellites: 衛星列表
    :param uav_swarm: 無人機蜂群實例
    :param ground_terminals: 地面終端列表
    :param output_file: 輸出文件名
    """
    # 準備導出數據結構
    export_data = {
        'metadata': {
            'export_time': datetime.now().isoformat(),
            'num_satellites': len(satellites),
            'num_uavs': uav_swarm.num_uavs,
            'num_ground_terminals': len(ground_terminals),
            'num_time_steps': len(results),
            'time_range': {
                'start': results[0]['time'] if results else 0,
                'end': results[-1]['time'] if results else 0,
                'dt': results[1]['time'] - results[0]['time'] if len(results) > 1 else 0
            }
        },
        'satellites': [],
        'ground_terminals': [],
        'time_steps': []
    }
    
    # 導出衛星信息
    for i, sat in enumerate(satellites):
        export_data['satellites'].append({
            'id': i + 1,
            'name': sat.name,
            'tx_power_dbw': sat.tx_power_dbw,
            'tx_gain_db': sat.tx_gain_db,
            'frequency_hz': sat.frequency_hz
        })
    
    # 導出地面終端信息
    for gt in ground_terminals:
        gt_info = {
            'id': gt.id,
            'latitude': float(gt.latitude),
            'longitude': float(gt.longitude),
            'rx_gain_db': float(gt.G_R_dB),
            'ecef': gt.get_ecef_coord().tolist()
        }
        # 添加名稱和類型（如果存在）
        if hasattr(gt, 'name'):
            gt_info['name'] = gt.name
        if hasattr(gt, 'type'):
            gt_info['type'] = gt.type
        export_data['ground_terminals'].append(gt_info)
    
    # 導出每個時間步的數據
    for result in results:
        time_step_data = {
            'time': float(result['time']),
            'satellite_positions': [
                pos.tolist() if isinstance(pos, np.ndarray) else pos
                for pos in result['satellite_positions']
            ],
            'uav_positions': result['uav_positions'].tolist(),
            'avg_sinr': float(result['avg_sinr']),
            'jammed_rate': float(result['jammed_rate']),
            'jammed_count': int(result['jammed_count']),
            'ground_terminal_results': []
        }
        
        # 導出每個地面終端的結果
        for gt_result in result['gt_results']:
            time_step_data['ground_terminal_results'].append({
                'gt_id': int(gt_result['gt_id']),
                'sinr': float(gt_result['sinr']),
                'p_rx': float(gt_result['p_rx']),
                'j_total': float(gt_result['j_total']),
                'is_jammed': bool(gt_result['is_jammed'])
            })
        
        export_data['time_steps'].append(time_step_data)
    
    # 保存為 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 數據已導出到: {output_file}")
    print(f"  - 時間步數: {len(results)}")
    print(f"  - 文件大小: {len(json.dumps(export_data)) / 1024:.2f} KB")
    
    return output_file

