document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('visualization-canvas');
    const ctx = canvas.getContext('2d');
    const algorithmSelect = document.getElementById('algorithm-select');
    const startNodeSelect = document.getElementById('start-node-select');
    const goalNodeSelect = document.getElementById('goal-node-select');
    const startBtn = document.getElementById('start-btn');

    let graph = {};
    const nodePositions = {
        'A': { x: 100, y: 100 },
        'B': { x: 250, y: 100 },
        'C': { x: 100, y: 250 },
        'D': { x: 400, y: 100 },
        'E': { x: 250, y: 250 },
        'F': { x: 100, y: 400 },
        'G': { x: 250, y: 400 },
    };
    const nodeRadius = 20;

    async function fetchGraph() {
        const response = await fetch('/graph');
        graph = await response.json();
        populateNodeSelectors();
        drawGraph();
    }

    function populateNodeSelectors() {
        const nodes = Object.keys(graph);
        startNodeSelect.innerHTML = '';
        goalNodeSelect.innerHTML = '';
        nodes.forEach(node => {
            const startOption = document.createElement('option');
            startOption.value = node;
            startOption.textContent = node;
            startNodeSelect.appendChild(startOption);

            const goalOption = document.createElement('option');
            goalOption.value = node;
            goalOption.textContent = node;
            goalNodeSelect.appendChild(goalOption);
        });
    }

    function drawGraph() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw edges
        for (const node in graph) {
            for (const [neighbor, weight] of graph[node]) {
                const pos1 = nodePositions[node];
                const pos2 = nodePositions[neighbor];
                ctx.beginPath();
                ctx.moveTo(pos1.x, pos1.y);
                ctx.lineTo(pos2.x, pos2.y);
                ctx.stroke();
            }
        }

        // Draw nodes
        for (const node in nodePositions) {
            const pos = nodePositions[node];
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, nodeRadius, 0, 2 * Math.PI);
            ctx.fillStyle = 'lightblue';
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node, pos.x, pos.y);
        }
    }

    async function startVisualization() {
        const algorithm = algorithmSelect.value;
        const startNode = startNodeSelect.value;
        const goalNode = goalNodeSelect.value;

        const response = await fetch('/run_search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                algorithm,
                start: startNode,
                goal: goalNode,
            }),
        });
        const { path, visited } = await response.json();

        animateSearch(visited, path);
    }

    function animateSearch(visited, path) {
        let i = 0;
        const interval = setInterval(() => {
            if (i >= visited.length) {
                clearInterval(interval);
                highlightPath(path);
                return;
            }

            const node = visited[i];
            const pos = nodePositions[node];
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, nodeRadius, 0, 2 * Math.PI);
            ctx.fillStyle = 'orange';
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = 'black';
            ctx.fillText(node, pos.x, pos.y);
            i++;
        }, 500);
    }

    function highlightPath(path) {
        if (!path) return;
        path.forEach(node => {
            const pos = nodePositions[node];
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, nodeRadius, 0, 2 * Math.PI);
            ctx.fillStyle = 'lightgreen';
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = 'black';
            ctx.fillText(node, pos.x, pos.y);
        });
    }

    startBtn.addEventListener('click', startVisualization);
    fetchGraph();
});
