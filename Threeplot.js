import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, camera, renderer, controls, instancedMesh;
const MAX_INSTANCES = 150000; // 최대 인스턴스 수

init();
animate();

function init() {
    // 1. Scene 설정
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(50, 50, 100);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    
    // 조명
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    window.addEventListener('resize', onWindowResize);
    document.getElementById('csvFile').addEventListener('change', handleFileSelect);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    document.getElementById('status').innerText = "데이터 분석 중...";

    Papa.parse(file, {
        header: false,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function(results) {
            renderMagneticField(results.data);
        }
    });
}

function renderMagneticField(data) {
    // 기존 메쉬 제거
    if (instancedMesh) {
        scene.remove(instancedMesh);
        instancedMesh.geometry.dispose();
        instancedMesh.material.dispose();
    }

    const count = Math.min(data.length, MAX_INSTANCES);
    
    // 2. Geometry 생성 (바늘 형태의 실린더)
    // 기본 방향은 Y축(+), 길이는 1, 직경은 0.1
    const geometry = new THREE.CylinderGeometry(0, 0.15, 1, 4); 
    const material = new THREE.MeshPhongMaterial({ color: 0xffffff });

    instancedMesh = new THREE.InstancedMesh(geometry, material, count);

    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
        const [x, y, z, bx, by, bz] = data[i];

        // 벡터 크기(세기) 계산
        const magnitude = Math.sqrt(bx*bx + by*by + bz*bz);
        
        // 3. 위치 설정
        dummy.position.set(x, y, z);

        // 4. 방향 설정 (화살표가 B 벡터 방향을 향하도록 회전)
        const direction = new THREE.Vector3(bx, by, bz).normalize();
        const arrowDir = new THREE.Vector3(0, 1, 0); // 기본 실린더 방향
        dummy.quaternion.setFromUnitVectors(arrowDir, direction);

        // 5. 크기 설정 (자기장 세기에 비례하여 길이를 조절하고 싶을 경우)
        const scale = Math.min(magnitude * 0.5, 5.0); // 너무 길어지지 않게 제한
        dummy.scale.set(1, scale, 1);

        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);

        // 6. 색상 설정 (세기에 따라 파란색 -> 빨간색)
        const hue = Math.max(0, 0.7 - (magnitude * 0.1)); // 예시 로직
        color.setHSL(hue, 1.0, 0.5);
        instancedMesh.setColorAt(i, color);
    }

    instancedMesh.instanceMatrix.needsUpdate = true;
    if (instancedMesh.instanceColor) instancedMesh.instanceColor.needsUpdate = true;

    scene.add(instancedMesh);
    document.getElementById('status').innerText = `${count.toLocaleString()} 개의 데이터 렌더링 완료`;
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}