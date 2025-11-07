from flask import Flask, render_template, jsonify, request
from search_algorithms import bfs, dfs, a_star, sample_graph, euclidean_distance

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def get_graph():
    return jsonify(sample_graph)

@app.route('/run_search', methods=['POST'])
def run_search():
    data = request.get_json()
    algorithm = data.get('algorithm')
    start_node = data.get('start')
    goal_node = data.get('goal')

    if not all([algorithm, start_node, goal_node]):
        return jsonify({'error': 'Missing parameters'}), 400

    path, visited = None, None
    if algorithm == 'bfs':
        path, visited = bfs(sample_graph, start_node, goal_node)
    elif algorithm == 'dfs':
        path, visited = dfs(sample_graph, start_node, goal_node)
    elif algorithm == 'a_star':
        path, visited = a_star(sample_graph, start_node, goal_node, euclidean_distance)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400

    return jsonify({'path': path, 'visited': visited})

if __name__ == '__main__':
    app.run(debug=True)
