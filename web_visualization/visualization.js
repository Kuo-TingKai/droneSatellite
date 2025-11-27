import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 全局變量
let scene, camera, renderer, controls;
let simulationData = null;
let currentTimeStep = 0;
let isPlaying = false;
let playSpeed = 1.0;
let animationFrameId = null;
let lastUpdateTime = 0;

// 3D 對象
let earth, satellites = [], uavs = [], groundTerminals = [];
let satelliteTrails = [], uavTrails = [];
let interferenceLinks = [];
let showLinks = true, showTrails = true;

// 常量
const EARTH_RADIUS = 6371000; // 米
const SCALE_FACTOR = 1.0; // 座標縮放因子

// 初始化 Three.js 場景
function initScene() {
    // 創建場景
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    scene.fog = new THREE.Fog(0x000000, 10000000, 50000000);
    
    // 創建相機
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        1000,
        100000000
    );
    camera.position.set(0, 0, 15000000);
    
    // 創建渲染器
    renderer = new THREE.WebGLRenderer({ 
        canvas: document.getElementById('canvas'),
        antialias: true 
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // 添加軌道控制器
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 1000000;
    controls.maxDistance = 100000000;
    
    // 添加光源
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // 創建地球
    createEarth();
    
    // 添加星空背景
    createStarField();
}

// 創建地球
function createEarth() {
    const geometry = new THREE.SphereGeometry(EARTH_RADIUS, 64, 64);
    
    // 使用地球紋理（如果有的話），否則使用簡單材質
    const loader = new THREE.TextureLoader();
    const material = new THREE.MeshPhongMaterial({
        color: 0x2233ff,
        emissive: 0x112244,
        shininess: 30,
        transparent: true,
        opacity: 0.8
    });
    
    earth = new THREE.Mesh(geometry, material);
    scene.add(earth);
    
    // 添加大氣層效果
    const atmosphereGeometry = new THREE.SphereGeometry(EARTH_RADIUS * 1.02, 64, 64);
    const atmosphereMaterial = new THREE.MeshPhongMaterial({
        color: 0x4488ff,
        transparent: true,
        opacity: 0.1,
        side: THREE.BackSide
    });
    const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
    scene.add(atmosphere);
}

// 創建星空背景
function createStarField() {
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 10000 });
    
    const starsVertices = [];
    for (let i = 0; i < 10000; i++) {
        const x = (Math.random() - 0.5) * 200000000;
        const y = (Math.random() - 0.5) * 200000000;
        const z = (Math.random() - 0.5) * 200000000;
        starsVertices.push(x, y, z);
    }
    
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);
}

// 加載模擬數據
async function loadSimulationData() {
    try {
        const response = await fetch('simulation_data.json');
        simulationData = await response.json();
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('max-steps').textContent = simulationData.time_steps.length - 1;
        
        // 初始化所有對象
        initializeObjects();
        
        // 更新到第一個時間步
        updateToTimeStep(0);
        
        // 設置事件監聽器
        setupEventListeners();
        
        // 開始動畫循環
        animate();
        
    } catch (error) {
        console.error('載入數據失敗:', error);
        document.getElementById('loading').textContent = '載入數據失敗！請確保 simulation_data.json 文件存在。';
    }
}

// 初始化所有對象
function initializeObjects() {
    // 創建衛星
    simulationData.satellites.forEach((sat, index) => {
        const geometry = new THREE.SphereGeometry(50000, 16, 16);
        const material = new THREE.MeshPhongMaterial({
            color: 0x2196F3,
            emissive: 0x2196F3,
            emissiveIntensity: 0.5
        });
        const satellite = new THREE.Mesh(geometry, material);
        satellite.userData = { id: sat.id, name: sat.name };
        satellites.push(satellite);
        scene.add(satellite);
        
        // 創建軌跡線
        const trailGeometry = new THREE.BufferGeometry();
        const trailMaterial = new THREE.LineBasicMaterial({
            color: 0x2196F3,
            transparent: true,
            opacity: 0.3
        });
        const trail = new THREE.Line(trailGeometry, trailMaterial);
        trail.userData = { type: 'satellite', index: index };
        satelliteTrails.push(trail);
        scene.add(trail);
    });
    
    // 創建無人機
    for (let i = 0; i < simulationData.metadata.num_uavs; i++) {
        const geometry = new THREE.ConeGeometry(20000, 40000, 8);
        const material = new THREE.MeshPhongMaterial({
            color: 0xFF9800,
            emissive: 0xFF9800,
            emissiveIntensity: 0.3
        });
        const uav = new THREE.Mesh(geometry, material);
        uav.rotation.x = Math.PI;
        uav.userData = { id: i + 1 };
        uavs.push(uav);
        scene.add(uav);
        
        // 創建軌跡線
        const trailGeometry = new THREE.BufferGeometry();
        const trailMaterial = new THREE.LineBasicMaterial({
            color: 0xFF9800,
            transparent: true,
            opacity: 0.2
        });
        const trail = new THREE.Line(trailGeometry, trailMaterial);
        trail.userData = { type: 'uav', index: i };
        uavTrails.push(trail);
        scene.add(trail);
    }
    
    // 創建地面終端
    simulationData.ground_terminals.forEach((gt) => {
        const geometry = new THREE.BoxGeometry(30000, 30000, 30000);
        const material = new THREE.MeshPhongMaterial({
            color: 0x4CAF50,
            emissive: 0x4CAF50,
            emissiveIntensity: 0.2
        });
        const terminal = new THREE.Mesh(geometry, material);
        terminal.userData = {
            id: gt.id,
            name: gt.name || `終端 ${gt.id}`,
            type: gt.type || 'unknown',
            ecef: gt.ecef
        };
        groundTerminals.push(terminal);
        scene.add(terminal);
    });
}

// 更新到指定時間步
function updateToTimeStep(step) {
    if (!simulationData || step < 0 || step >= simulationData.time_steps.length) {
        return;
    }
    
    currentTimeStep = step;
    const timeStepData = simulationData.time_steps[step];
    
    // 更新衛星位置
    timeStepData.satellite_positions.forEach((pos, index) => {
        if (satellites[index]) {
            satellites[index].position.set(pos[0], pos[1], pos[2]);
            
            // 更新軌跡
            if (showTrails && satelliteTrails[index]) {
                updateTrail(satelliteTrails[index], pos, step);
            } else if (satelliteTrails[index]) {
                satelliteTrails[index].visible = false;
            }
        }
    });
    
    // 更新無人機位置
    timeStepData.uav_positions.forEach((pos, index) => {
        if (uavs[index]) {
            uavs[index].position.set(pos[0], pos[1], pos[2]);
            
            // 更新軌跡
            if (showTrails && uavTrails[index]) {
                updateTrail(uavTrails[index], pos, step);
            } else if (uavTrails[index]) {
                uavTrails[index].visible = false;
            }
        }
    });
    
    // 更新地面終端狀態
    timeStepData.ground_terminal_results.forEach((gtResult) => {
        const terminal = groundTerminals.find(t => t.userData.id === gtResult.gt_id);
        if (terminal) {
            const isJammed = gtResult.is_jammed;
            terminal.material.color.setHex(isJammed ? 0xf44336 : 0x4CAF50);
            terminal.material.emissive.setHex(isJammed ? 0xf44336 : 0x4CAF50);
        }
    });
    
    // 更新干擾鏈路
    updateInterferenceLinks(timeStepData);
    
    // 更新 UI
    updateUI(timeStepData);
}

// 更新軌跡（簡化版本，僅顯示當前位置）
function updateTrail(trail, position, step) {
    // 簡化實現：只顯示最近幾個位置點
    const maxTrailPoints = 50;
    const startStep = Math.max(0, step - maxTrailPoints);
    
    const positions = [];
    for (let i = startStep; i <= step; i++) {
        if (i < simulationData.time_steps.length) {
            const data = simulationData.time_steps[i];
            // 根據對象類型獲取位置
            let pos;
            if (trail.userData && trail.userData.type === 'satellite') {
                const satIndex = trail.userData.index;
                if (data.satellite_positions[satIndex]) {
                    pos = data.satellite_positions[satIndex];
                }
            } else if (trail.userData && trail.userData.type === 'uav') {
                const uavIndex = trail.userData.index;
                if (data.uav_positions[uavIndex]) {
                    pos = data.uav_positions[uavIndex];
                }
            }
            
            if (pos) {
                positions.push(pos[0], pos[1], pos[2]);
            }
        }
    }
    
    if (positions.length > 0) {
        trail.geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        trail.geometry.setDrawRange(0, positions.length / 3);
    }
}

// 更新干擾鏈路
function updateInterferenceLinks(timeStepData) {
    // 清除現有鏈路
    interferenceLinks.forEach(link => scene.remove(link));
    interferenceLinks = [];
    
    if (!showLinks) return;
    
    // 為每個被阻斷的終端創建干擾鏈路
    timeStepData.ground_terminal_results.forEach((gtResult) => {
        if (gtResult.is_jammed) {
            const terminal = groundTerminals.find(t => t.userData.id === gtResult.gt_id);
            if (terminal) {
                timeStepData.uav_positions.forEach((uavPos) => {
                    const geometry = new THREE.BufferGeometry().setFromPoints([
                        new THREE.Vector3(...uavPos),
                        new THREE.Vector3(...terminal.userData.ecef)
                    ]);
                    const material = new THREE.LineBasicMaterial({
                        color: 0xf44336,
                        transparent: true,
                        opacity: 0.2,
                        linewidth: 2
                    });
                    const line = new THREE.Line(geometry, material);
                    interferenceLinks.push(line);
                    scene.add(line);
                });
            }
        }
    });
}

// 更新 UI
function updateUI(timeStepData) {
    document.getElementById('time-display').textContent = Math.round(timeStepData.time);
    document.getElementById('step-display').textContent = currentTimeStep;
    document.getElementById('avg-sinr').textContent = timeStepData.avg_sinr.toFixed(2);
    document.getElementById('jammed-rate').textContent = (timeStepData.jammed_rate * 100).toFixed(1);
    document.getElementById('jammed-count').textContent = timeStepData.jammed_count;
    document.getElementById('normal-count').textContent = 
        simulationData.metadata.num_ground_terminals - timeStepData.jammed_count;
    
    // 更新滑塊
    const slider = document.getElementById('time-slider');
    slider.max = simulationData.time_steps.length - 1;
    slider.value = currentTimeStep;
}

// 設置事件監聽器
function setupEventListeners() {
    // 時間滑塊
    document.getElementById('time-slider').addEventListener('input', (e) => {
        const step = parseInt(e.target.value);
        updateToTimeStep(step);
        isPlaying = false;
        document.getElementById('play-pause').textContent = '播放';
    });
    
    // 播放/暫停按鈕
    document.getElementById('play-pause').addEventListener('click', () => {
        isPlaying = !isPlaying;
        document.getElementById('play-pause').textContent = isPlaying ? '暫停' : '播放';
    });
    
    // 重置按鈕
    document.getElementById('reset').addEventListener('click', () => {
        currentTimeStep = 0;
        isPlaying = false;
        updateToTimeStep(0);
        document.getElementById('play-pause').textContent = '播放';
    });
    
    // 速度滑塊
    document.getElementById('speed-slider').addEventListener('input', (e) => {
        playSpeed = parseFloat(e.target.value);
        document.getElementById('speed-display').textContent = playSpeed.toFixed(1);
    });
    
    // 顯示選項
    document.getElementById('show-links').addEventListener('change', (e) => {
        showLinks = e.target.checked;
        updateToTimeStep(currentTimeStep);
    });
    
    document.getElementById('show-trails').addEventListener('change', (e) => {
        showTrails = e.target.checked;
        satelliteTrails.forEach(trail => trail.visible = showTrails);
        uavTrails.forEach(trail => trail.visible = showTrails);
    });
    
    // 窗口大小調整
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// 動畫循環
function animate() {
    animationFrameId = requestAnimationFrame(animate);
    
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastUpdateTime) / 1000;
    lastUpdateTime = currentTime;
    
    // 自動播放
    if (isPlaying && simulationData) {
        const frameTime = deltaTime * playSpeed;
        const stepInterval = simulationData.metadata.time_range.dt;
        const stepsPerSecond = 1 / stepInterval;
        const stepsToAdvance = Math.floor(frameTime * stepsPerSecond);
        
        if (stepsToAdvance > 0) {
            let newStep = currentTimeStep + stepsToAdvance;
            if (newStep >= simulationData.time_steps.length) {
                newStep = 0; // 循環播放
            }
            updateToTimeStep(newStep);
        }
    }
    
    // 更新控制器
    controls.update();
    
    // 旋轉地球
    if (earth) {
        earth.rotation.y += 0.0001;
    }
    
    // 渲染
    renderer.render(scene, camera);
}

// 初始化
initScene();
loadSimulationData();

