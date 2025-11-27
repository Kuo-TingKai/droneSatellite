# Web 3D 視覺化系統

基於 Three.js 的互動式 3D 視覺化系統，用於展示無人機蜂群對 LEO 衛星的電磁壓制模擬結果。

## 功能特點

- 🌍 **真實地球渲染**：3D 地球模型，支持旋轉和縮放
- 🛰️ **衛星軌跡**：顯示 LEO 衛星的軌道和位置
- 🚁 **無人機蜂群**：3D 無人機模型，顯示部署位置和移動軌跡
- 📡 **地面終端**：顯示台灣各地面終端的狀態（正常/被阻斷）
- 🔗 **干擾鏈路**：可視化無人機對地面終端的干擾鏈路
- ⏯️ **時間控制**：支持播放、暫停、快進、回放
- 📊 **實時統計**：顯示當前時間步的 SINR、阻斷率等統計信息

## 使用方法

### 1. 生成模擬數據

首先運行 Python 模擬程序生成數據：

```bash
python main.py
```

這會生成 `simulation_data.json` 文件。

### 2. 啟動 Web 服務器

由於瀏覽器的安全限制，需要通過 HTTP 服務器訪問。可以使用以下方法之一：

#### 方法 1：使用 Python 內建服務器

```bash
cd web_visualization
python -m http.server 8000
```

然後在瀏覽器中打開：`http://localhost:8000`

#### 方法 2：使用 Node.js http-server

```bash
npm install -g http-server
cd web_visualization
http-server -p 8000
```

#### 方法 3：使用 VS Code Live Server

如果使用 VS Code，可以安裝 "Live Server" 擴展，然後右鍵點擊 `index.html` 選擇 "Open with Live Server"。

### 3. 複製數據文件

將生成的 `simulation_data.json` 文件複製到 `web_visualization` 目錄：

```bash
cp simulation_data.json web_visualization/
```

## 控制說明

### 控制面板（左上角）

- **時間滑塊**：手動調整模擬時間
- **播放/暫停**：開始或暫停自動播放
- **重置**：回到模擬開始
- **播放速度**：調整播放速度（0.1x - 5x）
- **顯示干擾鏈路**：開關干擾鏈路的顯示
- **顯示軌跡**：開關衛星和無人機的軌跡線

### 3D 視圖控制

- **鼠標左鍵拖動**：旋轉視角
- **鼠標右鍵拖動**：平移視角
- **滾輪**：縮放視角

### 信息面板（右上角）

顯示當前時間步的統計信息：
- 時間步數
- 平均 SINR
- 阻斷率
- 被阻斷/正常終端數量

## 技術架構

- **Three.js**：3D 圖形渲染庫
- **ES6 Modules**：模塊化 JavaScript
- **JSON 數據格式**：Python 計算結果導出

## 文件結構

```
web_visualization/
├── index.html          # 主 HTML 文件
├── visualization.js    # Three.js 視覺化邏輯
├── README.md           # 本文件
└── simulation_data.json # 模擬數據（需要從根目錄複製）
```

## 注意事項

1. 確保 `simulation_data.json` 文件在 `web_visualization` 目錄中
2. 必須通過 HTTP 服務器訪問，不能直接打開 HTML 文件
3. 首次載入可能需要一些時間，取決於數據文件大小
4. 建議使用現代瀏覽器（Chrome、Firefox、Edge、Safari）

## 故障排除

### 數據載入失敗

- 檢查 `simulation_data.json` 是否存在
- 檢查文件路徑是否正確
- 查看瀏覽器控制台的錯誤信息

### 3D 渲染問題

- 確保瀏覽器支持 WebGL
- 嘗試更新瀏覽器到最新版本
- 檢查顯卡驅動是否最新

### 性能問題

- 減少顯示的軌跡線數量
- 關閉干擾鏈路顯示
- 降低播放速度

