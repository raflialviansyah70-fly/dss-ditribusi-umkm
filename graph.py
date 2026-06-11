import heapq
import math

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.adj_list = {}
        self.adj_matrix = {}

    def add_node(self, node_id, nama):
        self.nodes[node_id] = nama
        if node_id not in self.adj_list:
            self.adj_list[node_id] = []
        if node_id not in self.adj_matrix:
            self.adj_matrix[node_id] = {}

    def add_edge(self, from_node, to_node, jarak, waktu, biaya):
        for n in [from_node, to_node]:
            if n not in self.nodes:
                raise ValueError(f"Node '{n}' tidak ditemukan.")
        self.edges.append((from_node, to_node, jarak, waktu, biaya))
        self.adj_list[from_node].append((to_node, {
            "jarak": jarak, "waktu": waktu, "biaya": biaya
        }))
        if from_node not in self.adj_matrix:
            self.adj_matrix[from_node] = {}
        self.adj_matrix[from_node][to_node] = jarak

    def get_adjacency_matrix_display(self):
        ids = list(self.nodes.keys())
        matrix = {}
        for i in ids:
            matrix[i] = {}
            for j in ids:
                if i == j:
                    matrix[i][j] = 0
                elif j in self.adj_matrix.get(i, {}):
                    matrix[i][j] = self.adj_matrix[i][j]
                else:
                    matrix[i][j] = math.inf
        return matrix, ids

    def dijkstra(self, start, weight_key="jarak"):
        dist = {n: math.inf for n in self.nodes}
        prev = {n: None for n in self.nodes}
        dist[start] = 0
        pq = [(0, start)]
        visited = set()
        steps = []
        while pq:
            curr_dist, curr = heapq.heappop(pq)
            if curr in visited:
                continue
            visited.add(curr)
            steps.append({
                "node": curr, "nama": self.nodes[curr],
                "dist": curr_dist, "visited": list(visited)
            })
            for neighbor, weights in self.adj_list.get(curr, []):
                w = weights[weight_key]
                new_dist = curr_dist + w
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = curr
                    heapq.heappush(pq, (new_dist, neighbor))
        return dist, prev, steps

    def get_path(self, prev, target):
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
        return path

    def floyd_warshall(self, weight_key="jarak"):
        ids = list(self.nodes.keys())
        n = len(ids)
        idx = {node: i for i, node in enumerate(ids)}
        dist = [[math.inf] * n for _ in range(n)]
        nxt = [[None] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for from_node, to_node, jarak, waktu, biaya in self.edges:
            w = {"jarak": jarak, "waktu": waktu, "biaya": biaya}[weight_key]
            i, j = idx[from_node], idx[to_node]
            dist[i][j] = w
            nxt[i][j] = to_node
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]
        result = {}
        for i, a in enumerate(ids):
            result[a] = {}
            for j, b in enumerate(ids):
                result[a][b] = dist[i][j]
        return result, ids, nxt, idx

    def get_fw_path(self, nxt, idx, ids, start, end):
        si, ei = idx[start], idx[end]
        if nxt[si][ei] is None:
            return []
        path = [start]
        curr = start
        while curr != end:
            ci = idx[curr]
            ei2 = idx[end]
            curr = nxt[ci][ei2]
            if curr is None:
                return []
            path.append(curr)
        return path


def get_default_graph():
    g = Graph()
    nodes = [
        ("G",  "Gudang Pusat"),
        ("P1", "Pasar Badung"),
        ("P2", "Pasar Kreneng"),
        ("T1", "Toko Swalayan Denpasar"),
        ("T2", "Toko Oleh-oleh Kuta"),
        ("W1", "Warung Seminyak"),
        ("W2", "Warung Ubud"),
        ("H1", "Hotel Nusa Dua"),
    ]
    for nid, nama in nodes:
        g.add_node(nid, nama)
    edges = [
        ("G",  "P1",  5,  15, 5000),
        ("G",  "P2",  7,  20, 7000),
        ("G",  "T1",  6,  18, 6000),
        ("P1", "T2", 12,  30, 12000),
        ("P1", "W1", 15,  35, 15000),
        ("P2", "W2", 25,  60, 25000),
        ("T1", "H1", 20,  45, 20000),
        ("T2", "W1",  5,  10, 5000),
        ("W2", "H1", 30,  70, 30000),
        ("W1", "H1", 18,  40, 18000),
    ]
    for f, t, j, w, b in edges:
        g.add_edge(f, t, j, w, b)
    return g
