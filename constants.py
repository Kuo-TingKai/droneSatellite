"""
物理常數和系統參數定義
Physical constants and system parameters
"""
import numpy as np

# --- 物理常數 (SI 單位) ---
K_BOLTZMANN = 1.380649e-23  # 玻爾茲曼常數 (J/K)
C_LIGHT = 299792458.0      # 光速 (m/s)
EARTH_RADIUS = 6371000.0   # 地球平均半徑 (m)

# --- 標準通訊參數 ---
SYSTEM_BANDWIDTH = 10e6    # 系統頻寬 B (10 MHz)
NOISE_TEMP = 290.0         # 系統噪聲溫度 T_sys (開爾文)

# --- 衛星參數 ---
SAT_TX_POWER_DBW = 20.0    # 衛星發射功率 (100W, 20 dBW)
SAT_TX_GAIN_DB = 30.0      # 衛星發射天線增益
SAT_FREQ = 12e9            # 衛星頻率 (12 GHz, Ku-band)
SAT_ALTITUDE = 550e3       # LEO 衛星高度 (550 km)

# --- 無人機參數 ---
UAV_ALTITUDE = 20e3        # 無人機飛行高度 (20 km)
UAV_JAM_POWER_DBW = 10.0   # 無人機干擾功率 (10W, 10 dBW)
UAV_JAM_GAIN_DB = 25.0     # 無人機干擾天線增益
UAV_FREQ = 12e9            # 無人機干擾頻率 (假設在相同頻段)

# --- 地面終端參數 ---
GT_RX_GAIN_DB = 40.0       # 地面終端接收增益

# --- 性能閾值 ---
SINR_THRESHOLD_DB = -5.0   # SINR 阻斷閾值 (低於此值視為被阻斷)

# --- 模擬參數 ---
SIM_START_TIME = "2025-01-01 00:00:00"  # 模擬開始時間 (UTC)
DT = 60.0                  # 時間步長 (秒)

