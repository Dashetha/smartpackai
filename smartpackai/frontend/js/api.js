// frontend/js/api.js
class SmartPackAPI {
    constructor() {
        this.baseUrl = 'http://localhost:8000'; // Update with your backend URL
        this.endpoints = {
            predictBox: '/api/predict-box',
            optimizePack: '/api/optimize-pack'
        };
    }

    // Predict optimal box size
    async predictBoxSize(itemData) {
        try {
            const response = await fetch(`${this.baseUrl}${this.endpoints.predictBox}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Box prediction failed:', error);
            throw error;
        }
    }

    // Optimize packing arrangement
    async optimizePacking(boxData) {
        try {
            const response = await fetch(`${this.baseUrl}${this.endpoints.optimizePack}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(boxData)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Packing optimization failed:', error);
            throw error;
        }
    }

    // Simulate API response (for demo purposes)
    async simulateAPI(itemDimensions) {
        // This would be replaced with actual API calls in production
        return new Promise(resolve => {
            setTimeout(() => {
                const fragility = Math.random().toFixed(2);
                const spaceSaved = Math.floor(Math.random() * 30) + 10;
                const costSaved = (Math.random() * 5 + 1).toFixed(2);
                
                resolve({
                    status: 'success',
                    recommended_box: {
                        length: Math.ceil(itemDimensions.length * 1.2),
                        width: Math.ceil(itemDimensions.width * 1.3),
                        height: Math.ceil(itemDimensions.height * 1.4)
                    },
                    space_saved: spaceSaved,
                    cost_saved: costSaved,
                    item_data: {
                        ...itemDimensions,
                        fragility: fragility
                    },
                    packing_plan: {
                        items: [
                            {
                                position: { x: 0, y: 0, z: 0 },
                                rotation: { x: 0, y: 0, z: 0 }
                            }
                        ],
                        void_fill: {
                            type: fragility > 0.7 ? 'foam' : 'bubble_wrap',
                            volume: fragility > 0.7 ? 300 : 200
                        }
                    }
                });
            }, 1000);
        });
    }
}

// Initialize API instance
const api = new SmartPackAPI();

// Example usage:
// api.predictBoxSize(itemData).then(response => {...});
// api.optimizePacking(boxData).then(response => {...});

// Make API instance available globally for camera.js
window.SmartPackAPI = api;