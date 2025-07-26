// frontend/js/ui.js
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const visualizeBtn = document.getElementById('visualizeBtn');
    const instructionsList = document.getElementById('instructionsList');
    const referenceSelect = document.getElementById('referenceSelect');
    let currentItemDimensions = {};
    let currentBoxRecommendation = {};

    // Initialize event listeners
    function initEventListeners() {
        // Visualize button click handler
        visualizeBtn.addEventListener('click', () => {
            animateVisualizationButton();
            initThreeJSVisualization(currentBoxRecommendation);
        });

        // Reference object selection change
        referenceSelect.addEventListener('change', (e) => {
            showToast(`Reference set to: ${e.target.options[e.target.selectedIndex].text}`);
        });

        // Modal close handlers are in camera.js
    }

    // Animate the visualize button
    function animateVisualizationButton() {
        const btn = visualizeBtn;
        btn.disabled = true;
        btn.innerHTML = '<div class="loader"></div> Generating 3D View...';
        
        gsap.to(btn, {
            scale: 0.95,
            duration: 0.3,
            yoyo: true,
            repeat: 1,
            onComplete: () => {
                setTimeout(() => {
                    btn.disabled = false;
                    btn.textContent = '3D Visualization';
                }, 1500);
            }
        });
    }

    // Show toast notification
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        gsap.to(toast, {
            y: -20,
            opacity: 1,
            duration: 0.3,
            ease: 'power1.out'
        });

        setTimeout(() => {
            gsap.to(toast, {
                y: 0,
                opacity: 0,
                duration: 0.3,
                ease: 'power1.in',
                onComplete: () => toast.remove()
            });
        }, 3000);
    }

    // Update packing instructions based on item data
    function updatePackingInstructions(itemData) {
        instructionsList.innerHTML = '';
        
        const instructions = [
            'Place heaviest items at the bottom of the box',
            `Use ${itemData.fragility > 0.7 ? '3cm' : '2cm'} bubble wrap around fragile items`,
            'Fill empty spaces with packing peanuts or air cushions',
            'Seal box with reinforced packing tape'
        ];

        instructions.forEach(text => {
            const li = document.createElement('li');
            li.textContent = text;
            instructionsList.appendChild(li);
            
            // Animate each item
            gsap.from(li, {
                x: -20,
                opacity: 0,
                duration: 0.3,
                delay: instructions.indexOf(text) * 0.1
            });
        });
    }

    // Process API response and update UI
    function processAPIResponse(data) {
        currentBoxRecommendation = data.recommended_box;
        
        // Update box dimensions display
        document.getElementById('boxLength').textContent = currentBoxRecommendation.length;
        document.getElementById('boxWidth').textContent = currentBoxRecommendation.width;
        document.getElementById('boxHeight').textContent = currentBoxRecommendation.height;
        
        // Animate the stats
        animateValue('spaceSaved', 0, data.space_saved, 1500);
        animateValue('costSaved', 0, data.cost_saved, 1500);
        
        // Update packing instructions
        updatePackingInstructions(data.item_data);
        
        // Show success message
        showToast('Optimal packaging solution generated!', 'success');
    }

    // Value animation helper
    function animateValue(id, start, end, duration) {
        const element = document.getElementById(id);
        const range = end - start;
        let current = start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        const timer = setInterval(() => {
            current += increment;
            element.textContent = id === 'costSaved' 
                ? current.toFixed(2)
                : Math.round(current);
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }

    // Initialize the UI
    initEventListeners();
    
    // Make functions available globally for camera.js
    window.processAPIResponse = processAPIResponse;
    window.currentItemDimensions = currentItemDimensions;
});