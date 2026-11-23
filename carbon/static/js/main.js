// Global state references
let myChart = null;
let originalFootprint = 0; // in kg
let currentSavings = 0;    // in kg
let activeCategories = {
    transport: 0,
    energy: 0,
    diet: 0,
    waste: 0
};
let savingsByCategory = {
    transport: 0,
    energy: 0,
    diet: 0,
    waste: 0
};

// Form element reference
const form = document.getElementById('footprintForm');

// Event listener for calculations on form changes
if (form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateFootprint();
    });

    // Auto-calculate footprint on form input changes to make it extremely responsive and live
    form.querySelectorAll('input, select').forEach(element => {
        element.addEventListener('input', calculateFootprint);
        element.addEventListener('change', calculateFootprint);
    });
}

// Perform calculation asynchronously via AJAX fetch
function calculateFootprint() {
    if (!form) return;
    const formData = new FormData(form);
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            return;
        }
        
        originalFootprint = data.total;
        activeCategories = data.categories;

        // Reset savings checkboxes and category savings on recalculation
        document.querySelectorAll('.action-item').forEach(item => {
            item.classList.remove('active');
            item.setAttribute('aria-checked', 'false');
        });
        currentSavings = 0;
        savingsByCategory = {
            transport: 0,
            energy: 0,
            diet: 0,
            waste: 0
        };
        updateDOM();
    });
}

// Action checklist toggler
function toggleAction(element, savingsValue, category) {
    element.classList.toggle('active');
    const isActive = element.classList.contains('active');
    
    // Toggle ARIA checked state for screen readers
    element.setAttribute('aria-checked', isActive ? 'true' : 'false');
    
    if (isActive) {
        currentSavings += savingsValue;
        savingsByCategory[category] += savingsValue;
    } else {
        currentSavings -= savingsValue;
        savingsByCategory[category] -= savingsValue;
    }
    
    updateDOM();
}

// Update DOM elements and redraw charts
function updateDOM() {
    // Update savings text indicator
    const savedElement = document.getElementById('savedVal');
    if (savedElement) {
        savedElement.textContent = currentSavings.toLocaleString() + " kg / year";
    }
    
    // Calculate category-specific remaining emissions (clamping at 0)
    const remTransport = Math.max(0, activeCategories.transport - savingsByCategory.transport);
    const remEnergy = Math.max(0, activeCategories.energy - savingsByCategory.energy);
    const remDiet = Math.max(0, activeCategories.diet - savingsByCategory.diet);
    const remWaste = Math.max(0, activeCategories.waste - savingsByCategory.waste);

    const projectedFootprint = remTransport + remEnergy + remDiet + remWaste;
    const footprintInTonnes = (projectedFootprint / 1000).toFixed(1);
    
    // Set text outputs
    const co2NumElement = document.getElementById('co2Num');
    if (co2NumElement) {
        co2NumElement.textContent = footprintInTonnes;
    }
    
    const userTextElement = document.getElementById('userText');
    if (userTextElement) {
        userTextElement.textContent = footprintInTonnes + " tonnes";
    }

    // Update Progress Bar
    const userBarElement = document.getElementById('userBar');
    if (userBarElement) {
        const barPct = Math.min(100, (footprintInTonnes / 15) * 100);
        userBarElement.style.width = barPct + '%';
    }

    // Compare with global average
    const globalAvg = 4.5;
    const diffFromGlobal = footprintInTonnes - globalAvg;
    const globalCompareElement = document.getElementById('globalCompareVal');
    
    if (globalCompareElement) {
        if (diffFromGlobal > 0) {
            globalCompareElement.textContent = "+" + diffFromGlobal.toFixed(1) + " tonnes";
            globalCompareElement.className = "value red";
        } else {
            globalCompareElement.textContent = diffFromGlobal.toFixed(1) + " tonnes";
            globalCompareElement.className = "value green";
        }
    }

    // Draw Chart with correct categories
    renderChart(remTransport, remEnergy, remDiet, remWaste);

    // Generate Insights dynamically based on remaining emissions
    generateDynamicInsights(remTransport, remEnergy, remDiet, remWaste);
}

// Render the breakdown doughnut chart
function renderChart(t, e, d, w) {
    const chartCanvas = document.getElementById('footprintChart');
    if (!chartCanvas) return;
    const ctx = chartCanvas.getContext('2d');
    
    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Transport', 'Home Energy', 'Diet', 'Waste'],
            datasets: [{
                data: [t, e, d, w],
                backgroundColor: [
                    '#3b82f6', // transport -> blue
                    '#8b5cf6', // energy -> purple
                    '#10b981', // diet -> green
                    '#fbbf24'  // waste -> yellow
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#f3f4f6',
                        font: {
                            size: 11,
                            family: "'Plus Jakarta Sans', sans-serif"
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

// Animate the evaluation score number and progress bars for visual polish
function animateEvaluation(target) {
    const scoreEl = document.getElementById('evalScore');
    const progressFill = document.getElementById('evalProgressFill');
    const barFills = document.querySelectorAll('.score-bar-fill');

    if (!scoreEl || !progressFill) return;

    const start = 0;
    const end = parseFloat(target);
    const duration = 900; // ms
    const startTime = performance.now();

    function step(now) {
        const t = Math.min(1, (now - startTime) / duration);
        const eased = t < 0.5 ? 2*t*t : -1 + (4 - 2*t)*t; // easeInOutQuad
        const current = (start + (end - start) * eased).toFixed(2);
        scoreEl.textContent = current;
        progressFill.style.width = Math.min(100, (current / 100) * 100) + '%';
        if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);

    // Animate micro bars in breakdown grid
    barFills.forEach((bf) => {
        const w = bf.style.width || '0%';
        // trigger reflow then set width to current value to animate
        const targetWidth = w;
        bf.style.width = '0%';
        setTimeout(() => bf.style.width = targetWidth, 80);
    });
}

// Generate insights and recommendations on highest remaining carbon category
function generateDynamicInsights(t, e, d, w) {
    const recTitle = document.getElementById('recTitle');
    const recDesc = document.getElementById('recDesc');
    const recBox = document.getElementById('recBox');
    
    if (!recTitle || !recDesc || !recBox) return;

    const total = t + e + d + w;

    if (total === 0) {
        recTitle.textContent = "Carbon Neutral!";
        recDesc.textContent = "Congratulations! You have reduced your emissions to absolute zero. You are a carbon champion.";
        recBox.style.borderColor = "var(--primary)";
        return;
    }

    // Find highest remaining category
    const categories = { transport: t, energy: e, diet: d, waste: w };
    let maxVal = -1;
    let highestCat = '';
    for (const [cat, val] of Object.entries(categories)) {
        if (val > maxVal) {
            maxVal = val;
            highestCat = cat;
        }
    }

    recBox.style.borderColor = "rgba(59, 130, 246, 0.2)";

    if (highestCat === 'transport') {
        recTitle.textContent = "Focus Area: Reduce Transport Impact";
        recDesc.textContent = "Your mobility contributes the most to your footprint. Consider electric vehicles, taking trains for long-distance travel, or working from home when possible.";
    } else if (highestCat === 'energy') {
        recTitle.textContent = "Focus Area: Improve Household Efficiency";
        recDesc.textContent = "Your home heating/cooling and electricity are your main carbon drivers. Installing draft excluders, double-glazed windows, or energy-smart appliances will make a huge difference.";
    } else if (highestCat === 'diet') {
        recTitle.textContent = "Focus Area: Switch to Eco-Friendly Diet";
        recDesc.textContent = "Food production has a heavy impact. Adopting a flexitarian, vegetarian, or vegan diet can reduce diet-based greenhouse emissions by up to 60%.";
    } else {
        recTitle.textContent = "Focus Area: Minimize Waste & Circular Living";
        recDesc.textContent = "Avoid single-use packaging. Reusing, repairing, and ensuring all organics are composted (avoiding landfill methane emissions) are excellent next steps.";
    }
}

// Bind event listeners to actions on DOMContentLoaded
window.addEventListener('DOMContentLoaded', () => {
    // Bind Action Checklist buttons dynamically
    document.querySelectorAll('.action-item').forEach(element => {
        const savings = parseFloat(element.getAttribute('data-savings'));
        const category = element.getAttribute('data-category');

        element.addEventListener('click', () => {
            toggleAction(element, savings, category);
        });

        element.addEventListener('keydown', (event) => {
            if (event.key === ' ' || event.key === 'Enter') {
                event.preventDefault();
                toggleAction(element, savings, category);
            }
        });
    });

    // Run initial calculations
    calculateFootprint();

    // Animate the AI Evaluation Score card (default value present in HTML)
    const initialEval = document.getElementById('evalScore')?.textContent || '94.08';
    animateEvaluation(initialEval);
});
