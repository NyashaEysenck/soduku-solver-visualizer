from flask import Flask, render_template, jsonify
from solver.solver import SudokuSolver

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
solver = SudokuSolver(board.copy())

app = Flask(__name__)
solver.solve() 

@app.route('/')
def home():
    return render_template('sudoku.html')

@app.route('/start')
def start():
    return jsonify({'status': 'solving started'})

@app.route('/get_data')
def get_data():
    if solver.snapshots:
        last_snapshot = solver.snapshots.popleft()
        data = {
            'board': last_snapshot[0],
            'last_pos': last_snapshot[1],
            'is_valid': last_snapshot[2]
        }
    else:
        data = {
            'board': board,
            'last_pos': None,
            'is_valid': True
        }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
