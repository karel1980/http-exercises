
from maze_generator import MazeGenerator, MazeVisualizer
from flask import Flask
from uuid import uuid4
import json

class MazeServer:
    def __init__(self, maze):
        self.maze = maze
        self.cells_by_id = {}
        num_rows, num_cols = len(maze), len(maze[0])

        self.app = Flask('maze')

        for row in range(num_rows):
            for col in range(num_cols):
                cell_id = str(uuid4())
                self.cells_by_id[cell_id] = maze[row][col]
                maze[row][col] += (cell_id,(row, col))

        self.goal = (num_rows-1, num_cols-1)

        self.app.add_url_rule('/', 'index', lambda: self.index())
        self.app.add_url_rule('/maze/<cell_id>', 'cell', lambda cell_id: self.show_cell(cell_id))

    def index(self):
        entrance_id = self.maze[0][0][5]

        response = {}
        response['greeting'] = """Welcome to the maze. You may proceed to the entrance."""
        response['entrance'] = """/maze/%s"""%(entrance_id,)

        return json.dumps(response, indent=4)

    def show_cell(self, cell_id):
        cell_info = self.get_cell_info(cell_id)
        return json.dumps(cell_info, indent=4)

    def get_cell_by_position(self, row, col):
        return self.maze[row][col]

    def get_cell_by_id(self, cell_id):
        return self.cells_by_id[cell_id]

    def get_cell_info(self, cell_id):
        cell_info = {}
        cell_info['self'] = "/maze/" + cell_id

        cell = self.cells_by_id[cell_id]

        cell_info['exits'] = {}
        row, col = cell[6]

        if (row, col) == self.goal:
            cell_info['congratulations'] = "Congratulations, you reached the exit!"

        if cell[0] == 1: cell_info['exits']['left'] = "/maze/" + self.get_cell_by_position(row, col-1)[5]
        if cell[1] == 1: cell_info['exits']['up'] = "/maze/" + self.get_cell_by_position(row-1, col)[5]
        if cell[2] == 1: cell_info['exits']['right'] = "/maze/" + self.get_cell_by_position(row, col+1)[5]
        if cell[3] == 1: cell_info['exits']['down'] = "/maze/" + self.get_cell_by_position(row+1, col)[5]

        return cell_info

    def start(self):
        self.app.run()

if __name__=="__main__":
    maze = MazeGenerator().generate(10,10)
    server = MazeServer(maze)
    #MazeVisualizer().show_maze(maze)
    server.start()
