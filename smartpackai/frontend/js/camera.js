// frontend/js/camera.js
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('scannerOverlay');
    const ctx = canvas.getContext('2d');
    const scanBtn = document.getElementById('scanBtn');
    const scannerModal = document.getElementById('scannerModal');
    const closeButtons = document.querySelectorAll('.close');
    const captureBtn = document.getElementById('captureBtn');

    // Initialize camera
    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    facingMode: 'environment',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            video.srcObject = stream;
            
            // Set canvas dimensions to match video
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                drawDetectionBox();
            };
        } catch (err) {
            console.error("Camera error:", err);
            alert("Could not access the camera. Please enable camera permissions.");
        }
    }

    // Draw detection box overlay
    function drawDetectionBox() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw center rectangle (detection area)
        const rectWidth = canvas.width * 0.7;
        const rectHeight = canvas.height * 0.5;
        const x = (canvas.width - rectWidth) / 2;
        const y = (canvas.height - rectHeight) / 2;
        
        ctx.strokeStyle = '#14B8A6';
        ctx.lineWidth = 3;
        ctx.setLineDash([10, 5]);
        ctx.strokeRect(x, y, rectWidth, rectHeight);
        
        // Draw corner markers
        const cornerSize = 20;
        ctx.setLineDash([]);
        
        // Top-left
        drawCorner(x, y, cornerSize);
        // Top-right
        drawCorner(x + rectWidth, y, cornerSize);
        // Bottom-left
        drawCorner(x, y + rectHeight, cornerSize);
        // Bottom-right
        drawCorner(x + rectWidth, y + rectHeight, cornerSize);
        
        requestAnimationFrame(drawDetectionBox);
    }

    function drawCorner(x, y, size) {
        ctx.beginPath();
        // Horizontal line
        ctx.moveTo(x, y);
        ctx.lineTo(x + size, y);
        // Vertical line
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + size);
        ctx.stroke();
    }

    // Modal controls
    scanBtn.addEventListener('click', () => {
        scannerModal.style.display = 'block';
        initCamera();
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            scannerModal.style.display = 'none';
            document.getElementById('resultsModal').style.display = 'none';
            const stream = video.srcObject;
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        });
    });

    // Capture dimensions
    captureBtn.addEventListener('click', () => {
        // Simulate dimension detection (replace with actual CV logic)
        document.getElementById('lengthValue').textContent = '24.5 cm';
        document.getElementById('widthValue').textContent = '18.2 cm';
        document.getElementById('heightValue').textContent = '10.7 cm';
        
        // Close scanner and show results after delay
        setTimeout(() => {
            scannerModal.style.display = 'none';
            document.getElementById('resultsModal').style.display = 'block';
            simulateResults();
        }, 1000);
    });

    // Create floating boxes in hero section
    function createFloatingBoxes() {
        const container = document.getElementById('floatingBoxes');
        for (let i = 0; i < 8; i++) {
            const box = document.createElement('div');
            box.className = 'floating-box';
            box.style.width = `${Math.random() * 100 + 50}px`;
            box.style.height = `${Math.random() * 100 + 50}px`;
            box.style.left = `${Math.random() * 80 + 10}%`;
            box.style.top = `${Math.random() * 80 + 10}%`;
            box.style.animationDelay = `${Math.random() * 5}s`;
            container.appendChild(box);
        }
    }

    createFloatingBoxes();
});

// Simulate API results
function simulateResults() {
    // Animate stats counting up
    animateValue('spaceSaved', 0, 37, 1500);
    animateValue('costSaved', 0, 4.20, 1500);
    
    // Init 3D visualization
    initThreeJSVisualization();
}

function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = (progress * (end - start) + start).toFixed(progress < 1 ? 2 : 0);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}