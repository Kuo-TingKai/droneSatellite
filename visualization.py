"""
視覺化模塊：3D 空間、2D 地圖和時間序列圖表
Visualization module: 3D space, 2D map, and time series plots
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from constants import EARTH_RADIUS

# 配置中文字體支持
# Configure Chinese font support
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題


def visualize_3d_simulation(sat_positions, uav_positions, gt_positions, 
                            gt_status, title="無人機蜂群對 LEO 衛星的干擾空間示意圖"):
    """
    繪製衛星、無人機和地面終端的 3D 空間關係圖
    Draw 3D spatial relationship diagram
    
    :param sat_positions: 衛星位置列表 (ECEF)
    :param uav_positions: 無人機位置列表 (ECEF)
    :param gt_positions: 地面終端位置列表 (ECEF)
    :param gt_status: 地面終端狀態列表 (True=被阻斷, False=正常)
    :param title: 圖表標題
    """
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # 設置座標軸標籤
    ax.set_xlabel("X (m)", fontsize=10)
    ax.set_ylabel("Y (m)", fontsize=10)
    ax.set_zlabel("Z (m)", fontsize=10)
    
    # 轉換為 numpy 數組
    if len(sat_positions) > 0:
        sat_pos = np.array(sat_positions)
    else:
        sat_pos = np.array([]).reshape(0, 3)
    
    if len(uav_positions) > 0:
        uav_pos = np.array(uav_positions)
    else:
        uav_pos = np.array([]).reshape(0, 3)
    
    if len(gt_positions) > 0:
        gt_pos = np.array(gt_positions)
    else:
        gt_pos = np.array([]).reshape(0, 3)
    
    # 設置合理的軸範圍
    all_coords = []
    if len(sat_pos) > 0:
        all_coords.append(sat_pos)
    if len(uav_pos) > 0:
        all_coords.append(uav_pos)
    if len(gt_pos) > 0:
        all_coords.append(gt_pos)
    
    if len(all_coords) > 0:
        all_coords = np.concatenate(all_coords)
        max_coord = np.max(np.abs(all_coords)) * 1.1
        ax.set_xlim([-max_coord, max_coord])
        ax.set_ylim([-max_coord, max_coord])
        ax.set_zlim([-max_coord, max_coord])
    
    # A. 繪製地球表面 (簡化為一個球體的一部分)
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x_earth = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y_earth = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z_earth = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_earth, y_earth, z_earth, color='lightblue', 
                   alpha=0.1, label='地球表面')
    
    # B. 繪製衛星
    if len(sat_pos) > 0:
        ax.scatter(sat_pos[:, 0], sat_pos[:, 1], sat_pos[:, 2], 
                  c='blue', marker='o', s=200, label='LEO 衛星群', 
                  edgecolors='darkblue', linewidths=1)
    
    # C. 繪製無人機蜂群
    if len(uav_pos) > 0:
        ax.scatter(uav_pos[:, 0], uav_pos[:, 1], uav_pos[:, 2], 
                  c='orange', marker='^', s=150, label='無人機蜂群 (20km)', 
                  edgecolors='darkorange', linewidths=1)
    
    # D. 繪製地面終端及干擾鏈路
    if len(gt_pos) > 0:
        for i in range(len(gt_pos)):
            color = 'red' if gt_status[i] else 'green'
            marker = 'X' if gt_status[i] else 'o'
            label_text = '地面終端 (被阻斷)' if (i == 0 and gt_status[i]) else \
                        ('地面終端 (正常)' if (i == 0 and not gt_status[i]) else "")
            
            ax.scatter(gt_pos[i, 0], gt_pos[i, 1], gt_pos[i, 2], 
                      c=color, marker=marker, s=200, linewidths=2, 
                      label=label_text, edgecolors='black')
            
            # 繪製干擾鏈路 (從每個無人機到這個地面終端)
            if len(uav_pos) > 0:
                for uav in uav_pos:
                    ax.plot([uav[0], gt_pos[i, 0]], 
                           [uav[1], gt_pos[i, 1]], 
                           [uav[2], gt_pos[i, 2]], 
                           color='red', linestyle='--', alpha=0.2, linewidth=1)
    
    # 設置視角
    ax.view_init(elev=30, azim=45)
    ax.legend(loc='upper left', fontsize=9)
    
    plt.tight_layout()
    return fig


def visualize_2d_performance(gt_lon, gt_lat, sinr_values, 
                            title="地面終端 SINR 性能分佈"):
    """
    繪製 SINR 結果在地圖上的分佈圖
    Draw SINR distribution on map
    
    :param gt_lon: 地面終端經度列表
    :param gt_lat: 地面終端緯度列表
    :param sinr_values: SINR 值列表
    :param title: 圖表標題
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("經度 (Longitude)", fontsize=11)
    ax.set_ylabel("緯度 (Latitude)", fontsize=11)
    
    # 設置 SINR 顏色映射
    sinr_array = np.array(sinr_values)
    vmin, vmax = np.min(sinr_array), np.max(sinr_array)
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.RdYlGn_r  # 紅色代表低 SINR (被阻斷), 綠色代表高 SINR (良好)
    
    # 繪製每個終端
    for lon, lat, sinr in zip(gt_lon, gt_lat, sinr_values):
        color = cmap(norm(sinr))
        marker_style = 'X' if sinr < -5.0 else 'o'  # 低於 -5 dB 則用 X 標記為阻斷
        size = 200 if sinr < -5.0 else 100
        ax.scatter(lon, lat, c=[color], s=size, marker=marker_style, 
                   edgecolors='black', linewidths=1)
    
    # 添加顏色條
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label="SINR (dB)")
    cbar.ax.tick_params(labelsize=9)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def visualize_time_series(time_steps, avg_sinr, jammed_rate, 
                          title="蜂群干擾效果隨時間變化"):
    """
    繪製平均 SINR 和阻斷率隨時間的變化圖
    Draw time series of average SINR and jammed rate
    
    :param time_steps: 時間步長列表 (秒)
    :param avg_sinr: 平均 SINR 列表 (dB)
    :param jammed_rate: 阻斷率列表 (0-1)
    :param title: 圖表標題
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_title(title, fontsize=14, fontweight='bold')
    
    color = 'tab:blue'
    ax1.set_xlabel('時間 (秒)', fontsize=11)
    ax1.set_ylabel('平均 SINR (dB)', color=color, fontsize=11)
    line1 = ax1.plot(time_steps, avg_sinr, color=color, label='平均 SINR', 
                    linewidth=2, marker='o', markersize=4)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # 添加 SINR 閾值線
    ax1.axhline(y=-5.0, color='red', linestyle='--', alpha=0.5, 
               label='阻斷閾值 (-5 dB)')
    
    # 創建第二個 Y 軸來繪製阻斷率
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('阻斷率 (%)', color=color, fontsize=11)
    line2 = ax2.plot(time_steps, np.array(jammed_rate) * 100, 
                    color=color, linestyle='--', label='阻斷率', 
                    linewidth=2, marker='s', markersize=4)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 100)  # 阻斷率範圍 0% 到 100%
    
    # 合併圖例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=9)
    
    fig.tight_layout()
    return fig


def animate_3d_simulation(results, ground_terminals, 
                          title="無人機蜂群對 LEO 衛星的干擾空間動畫",
                          interval=200, save_path='simulation_3d_animation.gif'):
    """
    生成 3D 空間動畫，顯示整個模擬過程
    Generate 3D spatial animation showing the entire simulation process
    
    :param results: 模擬結果列表（每個元素包含一個時間步的數據）
    :param ground_terminals: 地面終端列表
    :param title: 動畫標題
    :param interval: 動畫幀間隔（毫秒）
    :param save_path: 保存路徑
    :return: 動畫對象
    """
    # 計算所有時間步的座標範圍
    all_positions = []
    for result in results:
        all_positions.extend(result['satellite_positions'])
        all_positions.extend(result['uav_positions'].tolist())
        all_positions.extend([gt.get_ecef_coord() for gt in ground_terminals])
    
    if len(all_positions) == 0:
        return None
    
    all_positions = np.array(all_positions)
    max_coord = np.max(np.abs(all_positions)) * 1.1
    
    # 創建圖形和軸
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-max_coord, max_coord])
    ax.set_ylim([-max_coord, max_coord])
    ax.set_zlim([-max_coord, max_coord])
    ax.set_xlabel("X (m)", fontsize=10)
    ax.set_ylabel("Y (m)", fontsize=10)
    ax.set_zlabel("Z (m)", fontsize=10)
    
    # 繪製地球表面（只繪製一次）
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x_earth = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y_earth = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z_earth = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_earth, y_earth, z_earth, color='lightblue', alpha=0.1)
    
    # 初始化繪圖對象
    sat_scatter = None
    uav_scatter = None
    gt_scatters = []
    gt_lines = []
    time_text = ax.text2D(0.02, 0.98, '', transform=ax.transAxes, 
                          fontsize=12, verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def animate(frame):
        nonlocal sat_scatter, uav_scatter, gt_scatters, gt_lines
        
        # 清除之前的繪圖對象
        if sat_scatter is not None:
            sat_scatter.remove()
        if uav_scatter is not None:
            uav_scatter.remove()
        for scatter in gt_scatters:
            scatter.remove()
        for line_group in gt_lines:
            for line in line_group:
                line.remove()
        gt_scatters.clear()
        gt_lines.clear()
        
        # 獲取當前幀的數據
        result = results[frame]
        sat_positions = np.array(result['satellite_positions'])
        uav_positions = result['uav_positions']
        gt_positions = np.array([gt.get_ecef_coord() for gt in ground_terminals])
        gt_status = [r['is_jammed'] for r in result['gt_results']]
        
        # 繪製衛星
        sat_scatter = None
        if len(sat_positions) > 0:
            sat_scatter = ax.scatter(sat_positions[:, 0], sat_positions[:, 1], 
                                    sat_positions[:, 2], c='blue', marker='o', 
                                    s=200, edgecolors='darkblue', linewidths=1,
                                    label='LEO 衛星群')
        
        # 繪製無人機
        uav_scatter = None
        if len(uav_positions) > 0:
            uav_scatter = ax.scatter(uav_positions[:, 0], uav_positions[:, 1], 
                                    uav_positions[:, 2], c='orange', marker='^', 
                                    s=150, edgecolors='darkorange', linewidths=1,
                                    label='無人機蜂群 (20km)')
        
        # 繪製地面終端和干擾鏈路
        for i in range(len(gt_positions)):
            color = 'red' if gt_status[i] else 'green'
            marker = 'X' if gt_status[i] else 'o'
            scatter = ax.scatter(gt_positions[i, 0], gt_positions[i, 1], 
                               gt_positions[i, 2], c=color, marker=marker, 
                               s=200, linewidths=2, edgecolors='black')
            gt_scatters.append(scatter)
            
            # 繪製干擾鏈路
            line_group = []
            if len(uav_positions) > 0:
                for uav in uav_positions:
                    line, = ax.plot([uav[0], gt_positions[i, 0]], 
                                   [uav[1], gt_positions[i, 1]], 
                                   [uav[2], gt_positions[i, 2]], 
                                   color='red', linestyle='--', alpha=0.2, linewidth=1)
                    line_group.append(line)
            gt_lines.append(line_group)
        
        # 更新時間文本
        time_text.set_text(f'時間: {result["time"]:.0f} s\n'
                          f'平均 SINR: {result["avg_sinr"]:.2f} dB\n'
                          f'阻斷率: {result["jammed_rate"]*100:.1f}%')
        
        # 設置視角（可選：讓視角緩慢旋轉）
        ax.view_init(elev=30, azim=45 + frame * 0.5)
        
        # 返回所有可用的繪圖對象
        return_items = [time_text]
        if sat_scatter is not None:
            return_items.append(sat_scatter)
        if uav_scatter is not None:
            return_items.append(uav_scatter)
        return_items.extend(gt_scatters)
        return return_items
    
    # 創建動畫
    anim = FuncAnimation(fig, animate, frames=len(results), 
                       interval=interval, blit=False, repeat=True)
    
    # 保存動畫
    print(f"    正在保存動畫到 {save_path}...")
    anim.save(save_path, writer=PillowWriter(fps=1000//interval))
    print(f"    ✓ 動畫已保存")
    
    return anim


def animate_2d_performance(results, ground_terminals,
                          title="地面終端 SINR 性能分佈動畫",
                          interval=200, save_path='simulation_2d_animation.gif'):
    """
    生成 2D 性能分佈動畫，顯示 SINR 值隨時間的變化
    Generate 2D performance distribution animation showing SINR changes over time
    
    :param results: 模擬結果列表
    :param ground_terminals: 地面終端列表
    :param title: 動畫標題
    :param interval: 動畫幀間隔（毫秒）
    :param save_path: 保存路徑
    :return: 動畫對象
    """
    gt_lon = [gt.longitude for gt in ground_terminals]
    gt_lat = [gt.latitude for gt in ground_terminals]
    
    # 計算所有時間步的 SINR 範圍
    all_sinr = []
    for result in results:
        all_sinr.extend([r['sinr'] for r in result['gt_results']])
    all_sinr = np.array(all_sinr)
    vmin, vmax = np.min(all_sinr), np.max(all_sinr)
    
    # 創建圖形和軸
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlabel("經度 (Longitude)", fontsize=11)
    ax.set_ylabel("緯度 (Latitude)", fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # 設置顏色映射
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.RdYlGn_r
    
    # 初始化繪圖對象
    scatter_plots = []
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 添加顏色條
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label="SINR (dB)")
    cbar.ax.tick_params(labelsize=9)
    
    def animate(frame):
        nonlocal scatter_plots
        
        # 清除之前的散點圖
        for scatter in scatter_plots:
            scatter.remove()
        scatter_plots.clear()
        
        # 獲取當前幀的數據
        result = results[frame]
        sinr_values = [r['sinr'] for r in result['gt_results']]
        
        # 繪製每個終端
        for lon, lat, sinr in zip(gt_lon, gt_lat, sinr_values):
            color = cmap(norm(sinr))
            marker_style = 'X' if sinr < -5.0 else 'o'
            size = 200 if sinr < -5.0 else 100
            scatter = ax.scatter(lon, lat, c=[color], s=size, marker=marker_style,
                               edgecolors='black', linewidths=1)
            scatter_plots.append(scatter)
        
        # 更新時間文本
        time_text.set_text(f'時間: {result["time"]:.0f} s\n'
                          f'平均 SINR: {result["avg_sinr"]:.2f} dB\n'
                          f'阻斷率: {result["jammed_rate"]*100:.1f}%')
        
        ax.set_title(f'{title} - 時間: {result["time"]:.0f} s', 
                    fontsize=14, fontweight='bold')
        
        return scatter_plots + [time_text]
    
    # 創建動畫
    anim = FuncAnimation(fig, animate, frames=len(results), 
                       interval=interval, blit=False, repeat=True)
    
    # 保存動畫
    print(f"    正在保存動畫到 {save_path}...")
    anim.save(save_path, writer=PillowWriter(fps=1000//interval))
    print(f"    ✓ 動畫已保存")
    
    return anim


def animate_time_series(results, 
                       title="蜂群干擾效果隨時間變化動畫",
                       interval=200, save_path='simulation_timeseries_animation.gif'):
    """
    生成時間序列動畫，顯示 SINR 和阻斷率隨時間的變化
    Generate time series animation showing SINR and jammed rate changes
    
    :param results: 模擬結果列表
    :param title: 動畫標題
    :param interval: 動畫幀間隔（毫秒）
    :param save_path: 保存路徑
    :return: 動畫對象
    """
    time_steps = [r['time'] for r in results]
    avg_sinr = [r['avg_sinr'] for r in results]
    jammed_rate = [r['jammed_rate'] for r in results]
    
    # 創建圖形和軸
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('時間 (秒)', fontsize=11)
    ax1.set_ylabel('平均 SINR (dB)', color='tab:blue', fontsize=11)
    ax1.set_xlim([min(time_steps), max(time_steps)])
    ax1.set_ylim([min(avg_sinr) * 1.1, max(avg_sinr) * 0.9])
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=-5.0, color='red', linestyle='--', alpha=0.5, 
               label='阻斷閾值 (-5 dB)')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('阻斷率 (%)', color='tab:red', fontsize=11)
    ax2.set_ylim(0, 100)
    
    # 初始化繪圖對象
    line1 = None
    line2 = None
    marker1 = None
    marker2 = None
    
    def animate(frame):
        nonlocal line1, line2, marker1, marker2
        
        # 清除之前的線條和標記
        if line1 is not None:
            line1.remove()
        if line2 is not None:
            line2.remove()
        if marker1 is not None:
            marker1.remove()
        if marker2 is not None:
            marker2.remove()
        
        # 獲取當前幀之前的數據
        current_time = time_steps[frame]
        time_data = time_steps[:frame+1]
        sinr_data = avg_sinr[:frame+1]
        rate_data = [r * 100 for r in jammed_rate[:frame+1]]
        
        # 繪製線條
        line1, = ax1.plot(time_data, sinr_data, color='tab:blue', 
                         label='平均 SINR', linewidth=2, marker='o', markersize=4)
        line2, = ax2.plot(time_data, rate_data, color='tab:red', 
                         linestyle='--', label='阻斷率', linewidth=2, 
                         marker='s', markersize=4)
        
        # 繪製當前點的高亮標記
        marker1 = ax1.scatter([current_time], [avg_sinr[frame]], 
                            color='tab:blue', s=200, zorder=5, 
                            edgecolors='black', linewidths=2)
        marker2 = ax2.scatter([current_time], [rate_data[-1]], 
                            color='tab:red', s=200, zorder=5, 
                            edgecolors='black', linewidths=2, marker='s')
        
        # 更新標題
        result = results[frame]
        ax1.set_title(f'{title} - 時間: {result["time"]:.0f} s', 
                     fontsize=14, fontweight='bold')
        
        # 更新圖例
        lines = [line1, line2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=9)
        
        return [line1, line2, marker1, marker2]
    
    # 創建動畫
    anim = FuncAnimation(fig, animate, frames=len(results), 
                       interval=interval, blit=False, repeat=True)
    
    # 保存動畫
    print(f"    正在保存動畫到 {save_path}...")
    anim.save(save_path, writer=PillowWriter(fps=1000//interval))
    print(f"    ✓ 動畫已保存")
    
    return anim

