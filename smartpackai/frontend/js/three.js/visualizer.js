// frontend/js/threejs/visualizer.js
function initThreeJSVisualization() {
    const container = document.getElementById('threejs-container');
    
    // Clear previous scene if exists
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0x14B8A6, 1);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Box (outer container)
    const boxGeometry = new THREE.BoxGeometry(2.5, 1.8, 1.2);
    const boxMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x8B5CF6,
        transparent: true,
        opacity: 0.7,
        wireframe: false
    });
    const box = new THREE.Mesh(boxGeometry, boxMaterial);
    scene.add(box);

    // Items inside box
    const item1Geometry = new THREE.BoxGeometry(1.2, 0.8, 0.5);
    const item1Material = new THREE.MeshPhongMaterial({ color: 0x14B8A6 });
    const item1 = new THREE.Mesh(item1Geometry, item1Material);
    item1.position.set(-0.5, -0.3, -0.2);
    scene.add(item1);

    const item2Geometry = new THREE.SphereGeometry(0.4, 32, 32);
    const item2Material = new THREE.MeshPhongMaterial({ color: 0xFF6B6B });
    const item2 = new THREE.Mesh(item2Geometry, item2Material);
    item2.position.set(0.7, 0.2, 0.3);
    scene.add(item2);

    // Camera position
    camera.position.z = 4;

    // Animation
    function animate() {
        requestAnimationFrame(animate);
        box.rotation.x += 0.005;
        box.rotation.y += 0.005;
        renderer.render(scene, camera);
    }
    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}