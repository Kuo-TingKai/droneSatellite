# Matplotlib Cheat Sheet
## 數據視覺化庫

### 基本導入
```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
```

### 基本繪圖

| 函數 | 說明 | 範例 |
|------|------|------|
| `plt.plot()` | 線圖 | `plt.plot(x, y)` |
| `plt.scatter()` | 散點圖 | `plt.scatter(x, y)` |
| `plt.bar()` | 柱狀圖 | `plt.bar(x, height)` |
| `plt.hist()` | 直方圖 | `plt.hist(data, bins=30)` |
| `plt.imshow()` | 圖像顯示 | `plt.imshow(array)` |

### 圖表設置

| 函數 | 說明 | 範例 |
|------|------|------|
| `plt.title()` | 標題 | `plt.title("Title", fontsize=14)` |
| `plt.xlabel()` | X軸標籤 | `plt.xlabel("X Label")` |
| `plt.ylabel()` | Y軸標籤 | `plt.ylabel("Y Label")` |
| `plt.xlim()` | X軸範圍 | `plt.xlim(0, 10)` |
| `plt.ylim()` | Y軸範圍 | `plt.ylim(0, 100)` |
| `plt.grid()` | 網格 | `plt.grid(True, alpha=0.3)` |
| `plt.legend()` | 圖例 | `plt.legend(loc='upper left')` |
| `plt.tight_layout()` | 緊湊佈局 | `plt.tight_layout()` |

### 3D 繪圖

| 函數 | 說明 | 範例 |
|------|------|------|
| `fig = plt.figure()` | 創建圖形 | `fig = plt.figure(figsize=(12, 10))` |
| `ax = fig.add_subplot(111, projection='3d')` | 3D 子圖 | `ax = fig.add_subplot(111, projection='3d')` |
| `ax.scatter()` | 3D 散點 | `ax.scatter(x, y, z, s=100, c='red')` |
| `ax.plot()` | 3D 線圖 | `ax.plot(x, y, z, 'r-', linewidth=2)` |
| `ax.plot_surface()` | 3D 表面 | `ax.plot_surface(X, Y, Z, alpha=0.5)` |
| `ax.view_init()` | 視角設置 | `ax.view_init(elev=30, azim=45)` |
| `ax.set_xlabel()` | 軸標籤 | `ax.set_xlabel("X (m)")` |

### 顏色和樣式

| 參數 | 說明 | 選項 |
|------|------|------|
| `c` 或 `color` | 顏色 | `'red'`, `'blue'`, `'#FF0000'`, `cmap` |
| `s` | 點大小 | `s=100` |
| `marker` | 標記樣式 | `'o'`, `'s'`, `'^'`, `'X'`, `'*'` |
| `linestyle` | 線型 | `'-'`, `'--'`, `'-.'`, `':'` |
| `linewidth` | 線寬 | `linewidth=2` |
| `alpha` | 透明度 | `alpha=0.5` (0-1) |
| `edgecolors` | 邊框顏色 | `edgecolors='black'` |

### 顏色映射 (Colormap)

| 函數 | 說明 | 範例 |
|------|------|------|
| `plt.cm.RdYlGn` | 紅-黃-綠 | `cmap=plt.cm.RdYlGn` |
| `plt.cm.viridis` | Viridis | `cmap=plt.cm.viridis` |
| `plt.cm.plasma` | Plasma | `cmap=plt.cm.plasma` |
| `plt.Normalize()` | 正規化 | `norm=plt.Normalize(vmin=0, vmax=100)` |
| `plt.colorbar()` | 顏色條 | `plt.colorbar(sm, label="Value")` |

### 子圖

| 函數 | 說明 | 範例 |
|------|------|------|
| `plt.subplot()` | 創建子圖 | `plt.subplot(2, 2, 1)` |
| `fig, axes = plt.subplots()` | 多子圖 | `fig, axes = plt.subplots(2, 2)` |
| `ax1.twinx()` | 雙Y軸 | `ax2 = ax1.twinx()` |

### 圖形保存

| 函數 | 說明 | 範例 |
|------|------|------|
| `plt.savefig()` | 保存圖形 | `plt.savefig('plot.png', dpi=150, bbox_inches='tight')` |
| `plt.show()` | 顯示圖形 | `plt.show()` |
| `plt.close()` | 關閉圖形 | `plt.close(fig)` |

### 在本專案中的應用

| 用途 | 代碼範例 |
|------|----------|
| 3D 空間視覺化 | `ax.scatter(sat_pos[:, 0], sat_pos[:, 1], sat_pos[:, 2], c='blue', marker='o', s=200)` |
| 2D 性能分佈 | `plt.scatter(lon, lat, c=sinr_values, cmap=plt.cm.RdYlGn_r, s=100)` |
| 時間序列 | `plt.plot(time_steps, avg_sinr, color='blue', linewidth=2, marker='o')` |
| 雙Y軸圖 | `ax2 = ax1.twinx(); ax2.plot(time, rate, color='red', linestyle='--')` |
| 顏色條 | `plt.colorbar(sm, label="SINR (dB)")` |

### 常用模式

```python
# 創建 3D 圖形
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='red', marker='o', s=100)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.view_init(elev=30, azim=45)
plt.savefig('3d_plot.png', dpi=150)
plt.show()

# 雙Y軸時間序列
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(time, sinr, color='blue', label='SINR')
ax1.set_ylabel('SINR (dB)', color='blue')
ax2 = ax1.twinx()
ax2.plot(time, rate, color='red', linestyle='--', label='Rate')
ax2.set_ylabel('Rate (%)', color='red')
plt.tight_layout()
plt.show()

# 顏色映射散點圖
norm = plt.Normalize(vmin=min_val, vmax=max_val)
cmap = plt.cm.RdYlGn_r
plt.scatter(x, y, c=values, cmap=cmap, norm=norm, s=100)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, label="Value")
plt.show()
```

