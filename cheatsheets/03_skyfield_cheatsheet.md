# Skyfield Cheat Sheet
## 衛星軌道計算庫 (SGP4)

### 基本導入
```python
from skyfield.api import load, EarthSatellite
from skyfield.timelib import Time
import datetime
```

### 核心概念

| 概念 | 說明 |
|------|------|
| **TLE** | Two-Line Element，兩行軌道元素數據 |
| **SGP4** | Simplified General Perturbations Model 4，簡化通用攝動模型 |
| **ECEF** | Earth-Centered, Earth-Fixed，地心地固座標系 |
| **ITRS** | International Terrestrial Reference System，國際地球參考系統 |

### 基本使用流程

| 步驟 | 代碼 | 說明 |
|------|------|------|
| 1. 載入時間刻度 | `ts = load.timescale()` | 創建時間系統 |
| 2. 創建衛星 | `sat = EarthSatellite(tle_line1, tle_line2, name, ts)` | 從 TLE 創建衛星 |
| 3. 設置時間 | `t = ts.utc(year, month, day, hour, minute, second)` | 創建時間對象 |
| 4. 計算位置 | `geocentric = sat.at(t)` | 計算衛星位置 |
| 5. 轉換座標 | `x, y, z = geocentric.frame_xyz('itrs').m` | 轉換為 ECEF 座標（米） |

### 主要函數

| 函數 | 說明 | 範例 |
|------|------|------|
| `load.timescale()` | 載入時間刻度 | `ts = load.timescale()` |
| `EarthSatellite()` | 創建衛星對象 | `sat = EarthSatellite(tle1, tle2, name, ts)` |
| `sat.at(t)` | 計算位置 | `geocentric = sat.at(t)` |
| `.frame_xyz('itrs')` | 轉換為 ITRS 座標 | `coords = geocentric.frame_xyz('itrs')` |
| `.m` | 獲取米單位 | `x, y, z = coords.m` |
| `.km` | 獲取公里單位 | `x, y, z = coords.km` |

### TLE 數據格式

| 行 | 格式 | 說明 | 範例 |
|----|------|------|------|
| Line 1 | `1 NNNNNU NNNNNAAA NNNNN.NNNNNNNN +.NNNNNNNN +NNNNN-N +NNNNN-N N NNNNN` | 衛星編號、發射年份等 | `1 44715U 19074F   25001.35787037 ...` |
| Line 2 | `2 NNNNN NNN.NNNN NNN.NNNN NNNNNNN NNN.NNNN NNN.NNNN NN.NNNNNNNNNNNNNN` | 軌道參數（傾角、升交點等） | `2 44715  53.0000 350.0000 ...` |

### 時間處理

| 方法 | 說明 | 範例 |
|------|------|------|
| `ts.utc()` | UTC 時間 | `t = ts.utc(2025, 1, 1, 0, 0, 0)` |
| `ts.now()` | 當前時間 | `t = ts.now()` |
| `ts.from_datetime()` | 從 datetime 創建 | `t = ts.from_datetime(dt)` |
| `datetime.timedelta()` | 時間增量 | `dt + datetime.timedelta(seconds=3600)` |

### 座標系統轉換

| 座標系 | 說明 | 獲取方法 |
|------|------|----------|
| **ITRS** | 國際地球參考系統（ECEF） | `.frame_xyz('itrs')` |
| **GCRS** | 地心天球參考系統 | `.frame_xyz('gcrs')` |
| **ICRS** | 國際天球參考系統 | `.frame_xyz('icrs')` |

### 在本專案中的應用

| 用途 | 代碼範例 |
|------|----------|
| 初始化衛星 | `self.sat = EarthSatellite(tle_line1, tle_line2, name, ts)` |
| 計算位置 | `geocentric = self.sat.at(t)` |
| 獲取 ECEF 座標 | `x_m, y_m, z_m = geocentric.frame_xyz('itrs').m` |
| 時間轉換 | `current_dt = t0 + datetime.timedelta(seconds=current_time)` |

### 完整範例

```python
from skyfield.api import load, EarthSatellite
import datetime

# TLE 數據
tle_line1 = '1 44715U 19074F   25001.35787037  .00000000  00000+0  00000+0 0  9990'
tle_line2 = '2 44715  53.0000 350.0000 0001000 00000 00000 15.00000000 99999'

# 1. 載入時間刻度
ts = load.timescale()

# 2. 創建衛星
satellite = EarthSatellite(tle_line1, tle_line2, 'Satellite-1', ts)

# 3. 設置時間
t0 = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
current_time = 3600  # 秒

current_dt = t0 + datetime.timedelta(seconds=current_time)
t = ts.utc(current_dt.year, current_dt.month, current_dt.day,
           current_dt.hour, current_dt.minute, current_dt.second)

# 4. 計算位置
geocentric = satellite.at(t)

# 5. 轉換為 ECEF 座標（米）
x_m, y_m, z_m = geocentric.frame_xyz('itrs').m

print(f"ECEF 座標: ({x_m:.2f}, {y_m:.2f}, {z_m:.2f}) 米")
```

### 注意事項

| 項目 | 說明 |
|------|------|
| **TLE 有效期** | TLE 數據通常有效期為數天到數週，需要定期更新 |
| **時間精度** | 使用 UTC 時間，避免時區問題 |
| **座標單位** | `.m` 返回米，`.km` 返回公里 |
| **計算速度** | SGP4 計算速度很快，適合實時模擬 |
| **精度** | 對於 LEO 衛星，精度通常在數百米範圍內 |

### 獲取真實 TLE 數據

| 來源 | 說明 | 網址 |
|------|------|------|
| **CelesTrak** | 最常用的 TLE 數據源 | https://celestrak.org/ |
| **Space-Track** | 官方數據（需註冊） | https://www.space-track.org/ |
| **NORAD** | 北美防空司令部 | 通過 CelesTrak 獲取 |

### 常見問題

| 問題 | 解決方案 |
|------|----------|
| TLE 數據過期 | 定期從 CelesTrak 更新 TLE |
| 座標為 NaN | 檢查 TLE 格式是否正確 |
| 時間錯誤 | 確保使用 UTC 時間 |
| 計算結果異常 | 驗證 TLE 數據是否對應正確的衛星 |

