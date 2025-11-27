"""
主執行文件：無人機蜂群對 LEO 衛星的電磁壓制模擬
Main execution file: UAV Swarm Electronic Warfare Simulation
"""
from satellite import Satellite
from uav_swarm import UAVSwarm
from ground_terminal import GroundTerminal
from simulation import Simulation
from visualization import (
    visualize_3d_simulation, visualize_2d_performance,
    visualize_time_series, animate_3d_simulation,
    animate_2d_performance, animate_time_series)


def create_sample_satellites():
    """
    創建台灣相關衛星 (使用模擬的 TLE 數據)
    Create Taiwan-related satellites with simulated TLE data
    
    參考：福衛系列衛星、商業通訊衛星等
    """
    # 使用更符合實際的 LEO 軌道參數
    # 軌道高度約 550-650 km，傾角約 97-98 度（太陽同步軌道）
    
    # 福衛五號類似的軌道參數（簡化版）
    # 高度約 720 km，傾角 98.28 度
    tle_formosat5_line1 = '1 42920U 17049A   25001.35787037  .00000000  00000+0  00000+0 0  9990'
    tle_formosat5_line2 = '2 42920  98.2800 100.0000 0001000 00000 00000 14.20000000 99999'
    
    # 商業通訊衛星（類似 Starlink 的 LEO 軌道）
    # 高度約 550 km，傾角 53 度
    tle_commsat_line1 = '1 44715U 19074F   25001.35787037  .00000000  00000+0  00000+0 0  9990'
    tle_commsat_line2 = '2 44715  53.0000 350.0000 0001000 00000 00000 15.00000000 99999'
    
    satellites = [
        Satellite("FORMOSAT-5 (福衛五號)", tle_formosat5_line1,
                  tle_formosat5_line2),
        Satellite("Commercial-LEO-1 (商業通訊衛星)", tle_commsat_line1,
                  tle_commsat_line2)
    ]
    
    return satellites


def create_sample_ground_terminals():
    """
    創建台灣實際位置的地面終端
    Create ground terminals at actual Taiwan locations
    
    包括：主要城市、政府機構、軍事設施、通訊基地台等
    """
    # 台灣主要城市和重要設施的實際座標
    # 格式：(ID, 名稱, 緯度, 經度, 接收增益 dB, 類型)
    terminal_locations = [
        # 主要城市 - 政府/商業終端
        (1, "台北市政府", 25.0375, 121.5637, 45.0, "政府"),
        (2, "新北市政府", 25.0120, 121.4656, 45.0, "政府"),
        (3, "桃園市政府", 24.9936, 121.3010, 45.0, "政府"),
        (4, "台中市政府", 24.1477, 120.6736, 45.0, "政府"),
        (5, "台南市政府", 22.9999, 120.2269, 45.0, "政府"),
        (6, "高雄市政府", 22.6273, 120.3014, 45.0, "政府"),
        
        # 重要軍事設施
        (7, "空軍松山基地", 25.0697, 121.5519, 50.0, "軍事"),
        (8, "海軍左營基地", 22.6961, 120.2806, 50.0, "軍事"),
        (9, "空軍清泉崗基地", 24.2647, 120.6200, 50.0, "軍事"),
        
        # 通訊基礎設施
        (10, "中華電信總部", 25.0330, 121.5654, 40.0, "通訊"),
        (11, "遠傳電信總部", 25.0479, 121.5310, 40.0, "通訊"),
        (12, "台灣大哥大總部", 25.0330, 121.5654, 40.0, "通訊"),
        
        # 重要港口和機場
        (13, "基隆港", 25.1276, 121.7395, 42.0, "基礎設施"),
        (14, "高雄港", 22.6149, 120.2819, 42.0, "基礎設施"),
        (15, "桃園國際機場", 25.0797, 121.2342, 42.0, "基礎設施"),
        
        # 其他重要城市
        (16, "新竹科學園區", 24.8038, 120.9687, 40.0, "商業"),
        (17, "嘉義市", 23.4871, 120.4418, 40.0, "政府"),
        (18, "屏東市", 22.6819, 120.4889, 40.0, "政府"),
        (19, "花蓮市", 23.9739, 121.6014, 40.0, "政府"),
        (20, "台東市", 22.7554, 121.1473, 40.0, "政府"),
    ]
    
    terminals = []
    for terminal_id, name, lat, lon, rx_gain, terminal_type in terminal_locations:
        terminal = GroundTerminal(
            id=terminal_id,
            latitude=lat,
            longitude=lon,
            rx_gain_db=rx_gain
        )
        # 可以添加名稱和類型屬性（如果需要）
        terminal.name = name
        terminal.type = terminal_type
        terminals.append(terminal)
    
    return terminals


def main():
    """主函數"""
    print("\n" + "="*60)
    print("無人機蜂群對 LEO 衛星的電磁壓制模擬系統")
    print("UAV Swarm Electronic Warfare Simulation System")
    print("="*60 + "\n")
    
    # 1. 初始化系統組件
    print("正在初始化系統組件...")
    
    # 創建衛星
    satellites = create_sample_satellites()
    print(f"✓ 已創建 {len(satellites)} 顆衛星")
    
    # 創建無人機蜂群（部署在台灣海峽，靠近台灣西海岸）
    # 台灣海峽位置：緯度約 23.5-25.0°N，經度約 119.5-120.5°E
    num_uavs = 8  # 增加無人機數量以模擬更真實的軍事部署
    uav_swarm = UAVSwarm(
        num_uavs,
        initial_lat_range=(23.5, 25.0),  # 台灣海峽緯度範圍
        initial_lon_range=(119.5, 120.5),  # 靠近台灣西海岸
        deployment_pattern='grid')  # 使用網格部署模式
    print(f"✓ 已創建 {num_uavs} 架無人機（部署在台灣海峽，網格陣型）")
    
    # 創建地面終端（使用實際台灣位置）
    ground_terminals = create_sample_ground_terminals()
    print(f"✓ 已創建 {len(ground_terminals)} 個地面終端（台灣實際位置）")
    
    # 2. 創建並運行模擬
    print("\n開始運行模擬...\n")
    
    simulation = Simulation(
        satellites=satellites,
        uav_swarm=uav_swarm,
        ground_terminals=ground_terminals,
        t_start=0.0,
        t_end=1800.0,  # 模擬 30 分鐘
        dt=60.0  # 每 60 秒一個時間步
    )
    
    results = simulation.run(enable_optimization=True)
    
    # 3. 顯示統計摘要
    stats = simulation.get_summary_statistics()
    if stats:
        print("\n" + "="*60)
        print("模擬統計摘要")
        print("="*60)
        print(f"總時間步數: {stats['total_steps']}")
        print(f"平均 SINR: {stats['avg_sinr_mean']:.2f} ± {stats['avg_sinr_std']:.2f} dB")
        print(f"SINR 範圍: [{stats['avg_sinr_min']:.2f}, {stats['avg_sinr_max']:.2f}] dB")
        print(f"平均阻斷率: {stats['jammed_rate_mean']*100:.1f}%")
        print(f"最大阻斷率: {stats['jammed_rate_max']*100:.1f}%")
        print("="*60)
    
    # 4. 視覺化結果
    print("\n正在生成視覺化圖表...")
    
    # 4.1 3D 空間視覺化 (使用最後一個時間步的數據)
    if results:
        last_result = results[-1]
        sat_positions = last_result['satellite_positions']
        uav_positions = last_result['uav_positions'].tolist()
        gt_positions = [gt.get_ecef_coord() for gt in ground_terminals]
        gt_status = [r['is_jammed'] for r in last_result['gt_results']]
        
        print("  - 生成 3D 空間視覺化...")
        fig_3d = visualize_3d_simulation(
            sat_positions, uav_positions, gt_positions, gt_status
        )
        fig_3d.savefig('simulation_3d.png', dpi=150, bbox_inches='tight')
        print("    ✓ 已保存: simulation_3d.png")
    
    # 4.2 2D 性能分佈圖
    if results:
        gt_lon = [gt.longitude for gt in ground_terminals]
        gt_lat = [gt.latitude for gt in ground_terminals]
        sinr_values = [r['sinr'] for r in last_result['gt_results']]
        
        print("  - 生成 2D 性能分佈圖...")
        fig_2d = visualize_2d_performance(gt_lon, gt_lat, sinr_values)
        fig_2d.savefig('simulation_2d.png', dpi=150, bbox_inches='tight')
        print("    ✓ 已保存: simulation_2d.png")
    
    # 4.3 時間序列圖
    if results:
        time_steps = [r['time'] for r in results]
        avg_sinr = [r['avg_sinr'] for r in results]
        jammed_rate = [r['jammed_rate'] for r in results]
        
        print("  - 生成時間序列圖...")
        fig_ts = visualize_time_series(time_steps, avg_sinr, jammed_rate)
        fig_ts.savefig('simulation_timeseries.png', dpi=150, bbox_inches='tight')
        print("    ✓ 已保存: simulation_timeseries.png")
    
    print("\n" + "="*60)
    print("所有視覺化圖表已生成完成！")
    print("="*60 + "\n")
    
    # 5. 生成動畫
    print("正在生成動畫...")
    if results:
        # 5.1 3D 空間動畫
        print("  - 生成 3D 空間動畫...")
        # 5.1 3D 空間動畫
        print("  - 生成 3D 空間動畫...")
        try:
            animate_3d_simulation(
                results, ground_terminals,
                save_path='simulation_3d_animation.gif',
                interval=300)  # 300ms per frame
            print("    ✓ 已保存: simulation_3d_animation.gif")
        except Exception as e:
            print(f"    ⚠ 3D 動畫生成失敗: {e}")
        
        # 5.2 2D 性能分佈動畫
        print("  - 生成 2D 性能分佈動畫...")
        try:
            animate_2d_performance(
                results, ground_terminals,
                save_path='simulation_2d_animation.gif',
                interval=300)
            print("    ✓ 已保存: simulation_2d_animation.gif")
        except Exception as e:
            print(f"    ⚠ 2D 動畫生成失敗: {e}")
        
        # 5.3 時間序列動畫
        print("  - 生成時間序列動畫...")
        try:
            animate_time_series(
                results,
                save_path='simulation_timeseries_animation.gif',
                interval=300)
            print("    ✓ 已保存: simulation_timeseries_animation.gif")
        except Exception as e:
            print(f"    ⚠ 時間序列動畫生成失敗: {e}")
    
    print("\n" + "="*60)
    print("所有動畫已生成完成！")
    print("="*60 + "\n")
    
    # 6. 導出數據供 Web 視覺化使用
    print("正在導出數據供 Web 視覺化...")
    try:
        from export_data import export_simulation_data
        export_simulation_data(results, satellites, uav_swarm, ground_terminals,
                             output_file='simulation_data.json')
        print("  ✓ 數據已導出，可用於 Web 視覺化")
    except Exception as e:
        print(f"  ⚠ 數據導出失敗: {e}")
    
    # 顯示圖表
    try:
        import matplotlib.pyplot as plt
        plt.show()
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"\n❌ 錯誤：缺少必要的庫。請運行: pip install -r requirements.txt")
        print(f"詳細錯誤: {e}\n")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}\n")
        import traceback
        traceback.print_exc()

