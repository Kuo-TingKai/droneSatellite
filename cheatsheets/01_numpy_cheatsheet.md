# NumPy Cheat Sheet
## 數值計算核心庫

### 基本導入
```python
import numpy as np
```

### 數組創建

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.array()` | 從列表創建數組 | `np.array([1, 2, 3])` |
| `np.zeros()` | 創建全零數組 | `np.zeros((3, 3))` |
| `np.ones()` | 創建全一數組 | `np.ones((2, 2))` |
| `np.random.rand()` | 隨機數組 [0, 1) | `np.random.rand(5, 2)` |
| `np.random.uniform()` | 均勻分佈隨機數 | `np.random.uniform(0, 10, size=(3,))` |
| `np.linspace()` | 等間距數組 | `np.linspace(0, 10, 100)` |
| `np.arange()` | 等差數組 | `np.arange(0, 10, 0.5)` |

### 數組操作

| 操作 | 語法 | 說明 |
|------|------|------|
| 形狀 | `arr.shape` | 獲取數組維度 |
| 大小 | `arr.size` | 獲取元素總數 |
| 重塑 | `arr.reshape(m, n)` | 改變數組形狀 |
| 轉置 | `arr.T` 或 `arr.transpose()` | 矩陣轉置 |
| 展平 | `arr.flatten()` | 展平為一維數組 |
| 複製 | `arr.copy()` | 深複製數組 |

### 數學運算

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.sqrt()` | 平方根 | `np.sqrt(arr)` |
| `np.exp()` | 指數函數 | `np.exp(arr)` |
| `np.log10()` | 以10為底對數 | `np.log10(arr)` |
| `np.sin()`, `np.cos()` | 三角函數 | `np.sin(arr)` |
| `np.deg2rad()` | 度轉弧度 | `np.deg2rad(90)` |
| `np.rad2deg()` | 弧度轉度 | `np.rad2deg(np.pi/2)` |
| `np.power()` | 冪運算 | `np.power(10, arr/10)` |

### 統計函數

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.mean()` | 平均值 | `np.mean(arr)` |
| `np.std()` | 標準差 | `np.std(arr)` |
| `np.min()`, `np.max()` | 最小/最大值 | `np.min(arr)` |
| `np.sum()` | 求和 | `np.sum(arr)` |
| `np.argmin()`, `np.argmax()` | 最小/最大索引 | `np.argmax(arr)` |

### 線性代數

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.linalg.norm()` | 向量範數（距離） | `np.linalg.norm(vec1 - vec2)` |
| `np.dot()` | 點積 | `np.dot(a, b)` |
| `np.cross()` | 叉積 | `np.cross(a, b)` |
| `np.linalg.inv()` | 矩陣求逆 | `np.linalg.inv(A)` |
| `np.linalg.solve()` | 解線性方程組 | `np.linalg.solve(A, b)` |

### 數組索引與切片

| 操作 | 語法 | 說明 |
|------|------|------|
| 單元素 | `arr[i, j]` | 訪問元素 |
| 切片 | `arr[start:end:step]` | 數組切片 |
| 布林索引 | `arr[arr > 5]` | 條件篩選 |
| 花式索引 | `arr[[0, 2, 4]]` | 指定索引 |

### 數組合併與分割

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.concatenate()` | 連接數組 | `np.concatenate([a, b])` |
| `np.vstack()` | 垂直堆疊 | `np.vstack([a, b])` |
| `np.hstack()` | 水平堆疊 | `np.hstack([a, b])` |
| `np.split()` | 分割數組 | `np.split(arr, 3)` |

### 條件與邏輯運算

| 函數 | 說明 | 範例 |
|------|------|------|
| `np.where()` | 條件選擇 | `np.where(condition, x, y)` |
| `np.clip()` | 限制範圍 | `np.clip(arr, min, max)` |
| `np.all()`, `np.any()` | 全部/任一為真 | `np.all(arr > 0)` |

### 在本專案中的應用

| 用途 | 代碼範例 |
|------|----------|
| 座標計算 | `np.array([x, y, z])` |
| 距離計算 | `np.linalg.norm(coord1 - coord2)` |
| 功率轉換 | `10**(power_dbw / 10)` |
| 隨機位置生成 | `np.random.rand(num, 2) * range + offset` |
| 數組限制 | `np.clip(positions, min_val, max_val)` |

### 常用模式

```python
# 創建隨機座標
coords = np.random.rand(10, 2) * [lat_range, lon_range] + [lat_min, lon_min]

# 計算距離矩陣
distances = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2)

# 條件篩選
valid = coords[coords[:, 0] > threshold]

# 數組廣播運算
result = arr1[:, None] + arr2[None, :]
```

