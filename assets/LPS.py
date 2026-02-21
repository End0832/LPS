try:
    local = local
except NameError:
    local = True

if local:
    from PySide6 import QtWidgets as qw

from math import inf

class Matrix():
    def __init__(self, rcsv):
        self.csv, self.titles = self.read_csv(rcsv)
        self.matrix = self.create_matrix(len(self.titles))
        self.fill()

    def read_csv(self, rcsv):
        csv = []
        titles = []
        if local:
            with open(rcsv, "r", encoding="utf-8") as f:
                f = f.readlines()
        else:
            f = rcsv.splitlines()
        for i in range(1, len(f)):
            csv.append(f[i].strip("\n").split(","))
        for i in range(0, len(csv)):
            titles.append(csv[i][0])
            titles.append(csv[i][1])
        titles = sorted(set(titles))
        return csv, titles

    def create_matrix(self, n):
        matrix = []
        for _ in range(n):
            nested_list = []
            for _ in range(n):
                nested_list.append(inf)
            matrix.append(nested_list)
        return matrix

    def fill(self):
        for a, b, c in self.csv:
            a = self.get_title_pos(a)
            b = self.get_title_pos(b)
            self.matrix[a][b] = int(c)
            self.matrix[b][a] = int(c)
        for i in range(len(self.matrix)):
            self.matrix[i][i] = 0
            
    def get(self):
        return self.matrix

    def get_titles(self):
        return self.titles

    def get_title_pos(self, title):
        return self.titles.index(title)



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
        raw_time = self.cost_for_ends[self.end]

        raw_time = divmod(raw_time, 60)
        time_str = ""
        time_letters = ("min", "s")
        for i in range(len(raw_time)):
            if raw_time[i] != 0:
                time_str = time_str + f"{raw_time[i]} {time_letters[i]} "

        path_str = self.chain_loc[0]
        for i in range(1, len(self.chain_loc)):
            path_str = path_str + " ➙ " + self.chain_loc[i]
            
        return f"TIME: {time_str}\nPATH: {path_str}"

if local:
    matrix = Matrix("data.csv")
    lps = Dijkstra(matrix.get(), matrix.get_titles())
    
    app = qw.QApplication([])
    window = qw.QWidget()
    window.setWindowTitle("LPS")
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
    
    button.clicked.connect(lambda: qw.QMessageBox.information(None, "LPS", lps.get(from_box.currentIndex(), to_box.currentIndex())))
    
    window.show()
    app.exec()








