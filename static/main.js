let isRunning = false;
let intervalId;

function renderGrid(board, lastPos, lastNum, isValid) {
    const container = document.getElementById('grid-container');
    container.innerHTML = ''; // Clear existing grid if any

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            gridItem.id = `cell-${i}-${j}`;
            gridItem.textContent = board[i][j];

            // Highlight new entry
            if (lastPos && i === lastPos[0] && j === lastPos[1]) {
                gridItem.style.backgroundColor = isValid ? 'lightgreen' : 'salmon';
                gridItem.style.color = 'black';
            } else {
                gridItem.style.backgroundColor = '#fff';
                gridItem.style.color = '#000';
            }

            container.appendChild(gridItem);
        }
    }

    // Highlight board border red if it's a failure
    if (!isValid) {
        container.style.border = '5px solid red';
        setTimeout(() => container.style.border = 'none', 1000); // Remove border after 1 second
    } else {
        container.style.border = 'none';
    }
}

function startVisualization() {
    if (isRunning) return; // Prevent multiple intervals
    isRunning = true;
    document.getElementById('placeholder').style.display = 'none'; // Hide placeholder
    fetch('/start').then(() => {
        intervalId = setInterval(function() {
            fetch('/get_data')
                .then(response => response.json())
                .then(data => {
                    if (data.board) {
                        renderGrid(data.board, data.last_pos, data.last_num, data.is_valid);
                    }
                });
        }, 100); // Fetch new data every 3 seconds
    });
}

function pauseVisualization() {
    clearInterval(intervalId);
    isRunning = false;
}

document.getElementById('start-btn').addEventListener('click', startVisualization);
document.getElementById('pause-btn').addEventListener('click', pauseVisualization);
