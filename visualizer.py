import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

FIXED_POS = {
    "G":  (0, 2),
    "P1": (2, 3),
    "P2": (2, 1),
    "T1": (1, 0),
    "T2": (4, 3.5),
    "W1": (5, 2.5),
    "W2": (4, 0.5),
    "H1": (7, 1.5),
}

def build_nx_graph(graph_obj, weight_key="jarak"):
    G = nx.DiGraph()
    for nid, nama in graph_obj.nodes.items():
        G.add_node(nid, label=nama)
    for f, t, jarak, waktu, biaya in graph_obj.edges:
        w = {"jarak": jarak, "waktu": waktu, "biaya": biaya}[weight_key]
        unit = {"jarak": "km", "waktu": "mnt", "biaya": "Rp"}[weight_key]
        label_val = f"Rp{w:,}" if weight_key == "biaya" else f"{w}{unit}"
        G.add_edge(f, t, weight=w, label=label_val,
                   jarak=jarak, waktu=waktu, biaya=biaya)
    return G

def draw_graph(graph_obj, weight_key="jarak", highlight_path=None, title="Graf Distribusi UMKM Bali"):
    G = build_nx_graph(graph_obj, weight_key)
    pos = {n: FIXED_POS.get(n, (0, 0)) for n in G.nodes()}

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    node_colors = []
    for n in G.nodes():
        if n == "G":
            node_colors.append("#f59e0b")
        elif highlight_path and n in highlight_path:
            node_colors.append("#10b981")
        else:
            node_colors.append("#3b82f6")

    normal_edges = list(G.edges())
    highlight_edges = []
    if highlight_path and len(highlight_path) > 1:
        highlight_edges = [(highlight_path[i], highlight_path[i+1])
                           for i in range(len(highlight_path)-1)
                           if G.has_edge(highlight_path[i], highlight_path[i+1])]
        normal_edges = [e for e in normal_edges if e not in highlight_edges]

    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                           edge_color="#4b5563", arrows=True,
                           arrowsize=20, width=1.5,
                           connectionstyle="arc3,rad=0.1", ax=ax)

    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges,
                               edge_color="#f59e0b", arrows=True,
                               arrowsize=25, width=3.5,
                               connectionstyle="arc3,rad=0.1", ax=ax)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=900, ax=ax)

    labels = {n: f"{n}\n{graph_obj.nodes[n][:12]}" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels,
                            font_color="white", font_size=7,
                            font_weight="bold", ax=ax)

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_color="#d1d5db", font_size=7, ax=ax)

    patches = [
        mpatches.Patch(color="#f59e0b", label="Gudang (Origin)"),
        mpatches.Patch(color="#10b981", label="Node di Rute"),
        mpatches.Patch(color="#3b82f6", label="Node Lain"),
    ]
    ax.legend(handles=patches, loc="upper left",
              facecolor="#1f2937", labelcolor="white", fontsize=8)

    ax.set_title(title, color="white", fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()
    return fig
