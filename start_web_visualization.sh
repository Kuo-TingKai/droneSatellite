#!/bin/bash
# 啟動 Web 視覺化服務器

echo "=========================================="
echo "無人機蜂群對 LEO 衛星電磁壓制模擬 - Web 視覺化"
echo "=========================================="
echo ""

# 檢查是否存在數據文件
if [ ! -f "simulation_data.json" ]; then
    echo "⚠ 未找到 simulation_data.json 文件"
    echo "正在運行模擬以生成數據..."
    echo ""
    
    # 激活虛擬環境並運行模擬
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    python main.py --no-animation 2>/dev/null || python main.py
    
    echo ""
fi

# 複製數據文件到 web_visualization 目錄
if [ -f "simulation_data.json" ]; then
    cp simulation_data.json web_visualization/
    echo "✓ 數據文件已準備就緒"
else
    echo "❌ 無法生成數據文件，請手動運行: python main.py"
    exit 1
fi

echo ""
echo "正在啟動 Web 服務器..."
echo "服務器地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服務器"
echo "=========================================="
echo ""

# 進入 web_visualization 目錄並啟動服務器
cd web_visualization
python -m http.server 8000

