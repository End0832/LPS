from PySide6 import QtWidgets as qw
from math import inf

class Matrix():
    def __init__(self, name):
        self.csv = []
        self.titles = []
        with open(name, "r", encoding="utf-8") as f:
            f = f.readlines()
            for i in range(1, len(f)):
                self.csv.append(f[i].strip("\n").split(","))
            for i in range(0, len(self.csv)):
                nested_list = self.csv[i]
                self.titles.append(nested_list[0])
                self.titles.append(nested_list[1])
            self.titles = sorted(set(self.titles))
        
        self.matrix = []
        for _ in range(0, len(self.titles)):
            nested_list = []
            for _ in range(0, len(self.titles)):
                nested_list.append(inf)
            self.matrix.append(nested_list)

    def get_titles(self):
        return self.titles
            
    def get(self):
        return self.matrix

    def change_value(self, pos, val):
        row, column = pos.strip("[").strip(" ").strip("]").split(",")
        row = int(row)
        column = int(column)
        nested_list = self.matrix[row]
        nested_list[column] = val
        self.matrix[row] = nested_list

    def check(self, val):
        results = []
        for i in range(0, len(self.csv)):
            nested_list = self.csv[i]
            for j in range(0, len(nested_list) - 1):
                if nested_list[j] == val:
                    if j == 0:
                        results.append((nested_list[0], nested_list[1], nested_list[2]))
                    if j == 1:
                        results.append((nested_list[1], nested_list[0], nested_list[2]))
        return results

    def title_position(self, title):
        for i in range(0, len(self.titles)):
            if title == self.titles[i]:
                return i

    def fill(self):
        for i in range(0, len(self.titles)):
            ways = self.check(self.titles[i])
            for j in range(0, len(ways)):
                a, b, c = ways[j]
                a = self.title_position(a)
                b = self.title_position(b)
                self.change_value(f"[{a}, {b}]", int(c))
                self.change_value(f"[{b}, {a}]", int(c))
            self.change_value(f"[{a}, {a}]", 0)





class Dijkstra():
    def __init__(self, matrix, loc):
        self.matrix = matrix
        self.loc = loc

    def get_roads(self):
        self.cost_for_ends = []
        self.path = []
        visited = []
        n = len(self.matrix)
        for _ in range(n):
            self.cost_for_ends.append(inf)
            visited.append(False)
            self.path.append(None)
        
        self.cost_for_ends[self.start] = 0

        for _ in range(n):
            smallest = None
            min_dist = inf
            for i in range(n):
                if visited[i] == False and self.cost_for_ends[i] < min_dist:
                    min_dist = self.cost_for_ends[i]
                    smallest = i

            if smallest == None:
                break

            visited[smallest] = True

            for j in range(n):
                if self.matrix[smallest][j] != inf and visited[j] == False:
                    dist = self.matrix[smallest][j] + self.cost_for_ends[smallest]
                    if dist < self.cost_for_ends[j]:
                        self.cost_for_ends[j] = dist
                        self.path[j] = smallest

    def get_shortest_path(self):
        self.chain = []
        current = self.end
        self.chain.append(current)
        while current != self.start:
            current = self.path[current]
            self.chain.append(current)

        self.chain.reverse()

    def get_locations(self):
        self.chain_loc = []
        for i in range(len(self.chain)):
            self.chain_loc.append(self.loc[self.chain[i]])

    def get(self, start, end):
        self.start = start
        self.end = end
        self.get_roads()
        self.get_shortest_path()
        self.get_locations()
        seconds = self.cost_for_ends[self.end]
        
        if seconds < 60:
            time = str(seconds) + " s"
        else:
            minutes = 0
            while seconds >= 60:
                seconds = seconds - 60
                minutes = minutes + 1
            time = str(minutes) + " min " + str(seconds) + " s"

        path_str = self.chain_loc[0]
        for i in range(1, len(self.chain_loc)):
            path_str = path_str + " -> " + self.chain_loc[i]
            
        return f"TIME: {time}\nPATH: {path_str}"



matrix = Matrix("data.csv")
matrix.fill()

gps = Dijkstra(matrix.get(), matrix.get_titles())

print(matrix.get_titles())



app = qw.QApplication([])
window = qw.QWidget()
window.setWindowTitle("GPS")
window.resize(190, 100)

layout = qw.QVBoxLayout(window)

from_box = qw.QComboBox()
to_box = qw.QComboBox()
button = qw.QPushButton()

from_box.addItems(matrix.get_titles())
to_box.addItems(matrix.get_titles())
button.setText("Travel")

layout.addWidget(from_box)
layout.addWidget(to_box)
layout.addWidget(button)

button.clicked.connect(lambda: qw.QMessageBox.information(None, "GPS", gps.get(from_box.currentIndex(), to_box.currentIndex())))

window.show()
app.exec()
