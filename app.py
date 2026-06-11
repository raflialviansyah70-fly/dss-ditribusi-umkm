import streamlit as st
import pandas as pd
import math
from graph import Graph, get_default_graph
from visualizer import draw_graph

st.set_page_config(
    page_title="DSS Distribusi UMKM Bali",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; color: #f1f5f9; }
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #f59e0b; }
    .metric-label { font-size: 12px; color: #94a3b8; margin-top: 4px; }
    .step-card {
        background: #1e293b;
        border-left: 4px solid #3b82f6;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 13px;
    }
    .path-badge {
        display: inline-block;
        background: #f59e0b;
        color: #000;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        margin: 2px;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #f59e0b;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }
    div[data-testid="stMetricValue"] { color: #f59e0b !important; }
</style>
""", unsafe_allow_html=True)

if "graph" not in st.session_state:
    st.session_state.graph = get_default_graph()

g: Graph = st.session_state.graph

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/delivery.png", width=60)
    st.markdown("## 🚚 DSS Distribusi UMKM")
    st.markdown("**Mata Kuliah:** Struktur Data  \n**Algoritma:** Dijkstra + Floyd-Warshall")
    st.divider()

    st.markdown("### ➕ Tambah Node")
    with st.form("form_node"):
        nid  = st.text_input("ID Node (misal: T3)", max_chars=5)
        nama = st.text_input("Nama Lokasi")
        add_n = st.form_submit_button("Tambah Node")
        if add_n:
            if nid and nama:
                if nid in g.nodes:
                    st.error("ID sudah ada.")
                else:
                    g.add_node(nid.upper(), nama)
                    st.success(f"Node {nid.upper()} ditambahkan!")
            else:
                st.warning("Isi semua field.")

    st.markdown("### ➕ Tambah Edge")
    node_ids = list(g.nodes.keys())
    with st.form("form_edge"):
        col1, col2 = st.columns(2)
        f_node = col1.selectbox("Dari", node_ids, key="ef")
        t_node = col2.selectbox("Ke",   node_ids, key="et")
        jarak  = st.number_input("Jarak (km)",    min_value=0.1, value=5.0,  step=0.5)
        waktu  = st.number_input("Waktu (menit)", min_value=1,   value=15,   step=1)
        biaya  = st.number_input("Biaya BBM (Rp)",min_value=100, value=5000, step=500)
        add_e  = st.form_submit_button("Tambah Edge")
        if add_e:
            if f_node != t_node:
                g.add_edge(f_node, t_node, jarak, int(waktu), int(biaya))
                st.success(f"Edge {f_node} → {t_node} ditambahkan!")
            else:
                st.error("Node asal dan tujuan harus berbeda.")

    st.divider()
    if st.button("🔄 Reset ke Default"):
        st.session_state.graph = get_default_graph()
        st.rerun()

st.markdown("""
<div style='text-align:center; padding: 20px 0 10px 0'>
    <h1 style='color:#f59e0b; font-size:32px; margin:0'>🚚 DSS Optimasi Rute Distribusi UMKM Bali</h1>
    <p style='color:#94a3b8; font-size:14px; margin-top:6px'>
        Decision Support System berbasis Graph — Algoritma Dijkstra & Floyd-Warshall
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visualisasi Graf",
    "🔍 Dijkstra",
    "🗺️ Floyd-Warshall",
    "📋 Data Graf",
    "ℹ️ Tentang Sistem"
])

with tab1:
    st.markdown('<div class="section-header">Visualisasi Graf Distribusi</div>', unsafe_allow_html=True)
    weight_vis = st.radio("Tampilkan bobot:", ["jarak", "waktu", "biaya"],
                          horizontal=True,
                          format_func=lambda x: {"jarak":"Jarak (km)","waktu":"Waktu (mnt)","biaya":"Biaya (Rp)"}[x])
    fig = draw_graph(g, weight_key=weight_vis)
    st.pyplot(fig, use_container_width=True)
    st.info(f"**Total Node:** {len(g.nodes)}  |  **Total Edge:** {len(g.edges)}  |  **Tipe:** Directed Weighted Graph")

with tab2:
    st.markdown('<div class="section-header">Pencarian Rute Terpendek — Dijkstra</div>', unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
    start_node  = col_d1.selectbox("Node Asal", list(g.nodes.keys()),
                                    format_func=lambda x: f"{x} – {g.nodes[x]}")
    target_node = col_d2.selectbox("Node Tujuan", list(g.nodes.keys()),
                                    index=min(4, len(g.nodes)-1),
                                    format_func=lambda x: f"{x} – {g.nodes[x]}")
    weight_d    = col_d3.selectbox("Optimasi berdasarkan",
                                    ["jarak", "waktu", "biaya"],
                                    format_func=lambda x: {"jarak":"Jarak (km)","waktu":"Waktu (menit)","biaya":"Biaya BBM (Rp)"}[x])

    if st.button("▶️ Jalankan Dijkstra", type="primary"):
        if start_node == target_node:
            st.warning("Node asal dan tujuan sama.")
        else:
            dist, prev, steps = g.dijkstra(start_node, weight_key=weight_d)
            path = g.get_path(prev, target_node)
            if dist[target_node] == math.inf:
                st.error(f"❌ Tidak ada rute dari {start_node} ke {target_node}.")
            else:
                total_j = total_w = total_b = 0
                for i in range(len(path)-1):
                    for nb, wts in g.adj_list[path[i]]:
                        if nb == path[i+1]:
                            total_j += wts["jarak"]
                            total_w += wts["waktu"]
                            total_b += wts["biaya"]
                            break

                m1, m2, m3 = st.columns(3)
                m1.metric("📏 Total Jarak", f"{total_j} km")
                m2.metric("⏱️ Estimasi Waktu", f"{total_w} menit")
                m3.metric("💰 Biaya BBM", f"Rp {total_b:,}")

                st.markdown("**Rute Optimal:**")
                path_html = " → ".join([f'<span class="path-badge">{p} ({g.nodes[p]})</span>' for p in path])
                st.markdown(path_html, unsafe_allow_html=True)

                fig2 = draw_graph(g, weight_key=weight_d, highlight_path=path,
                                  title=f"Rute Dijkstra: {start_node} → {target_node}")
                st.pyplot(fig2, use_container_width=True)

                with st.expander("📋 Lihat Proses Langkah Dijkstra"):
                    for i, step in enumerate(steps):
                        d_str = str(step['dist']) if step['dist'] != math.inf else "∞"
                        st.markdown(f"""
                        <div class="step-card">
                            <b>Langkah {i+1}</b> — Kunjungi <b>{step['node']} ({step['nama']})</b><br>
                            Jarak kumulatif: <b>{d_str}</b> | Visited: {', '.join(step['visited'])}
                        </div>
                        """, unsafe_allow_html=True)

                with st.expander("📊 Semua Jarak dari " + start_node):
                    rows = []
                    for nid, nama in g.nodes.items():
                        d = dist[nid]
                        p = g.get_path(prev, nid)
                        rows.append({
                            "Tujuan": f"{nid} – {nama}",
                            f"Jarak ({weight_d})": d if d != math.inf else "Tidak terjangkau",
                            "Rute": " → ".join(p) if d != math.inf else "-"
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tab3:
    st.markdown('<div class="section-header">Analisis Semua Rute — Floyd-Warshall</div>', unsafe_allow_html=True)
    weight_fw = st.radio("Bobot:", ["jarak", "waktu", "biaya"], horizontal=True,
                          format_func=lambda x: {"jarak":"Jarak (km)","waktu":"Waktu (mnt)","biaya":"Biaya (Rp)"}[x],
                          key="fw_weight")

    if st.button("▶️ Jalankan Floyd-Warshall", type="primary"):
        fw_dist, ids, nxt, idx = g.floyd_warshall(weight_key=weight_fw)

        st.markdown("**Matriks Jarak Terpendek:**")
        matrix_data = {}
        for a in ids:
            matrix_data[a] = {}
            for b in ids:
                v = fw_dist[a][b]
                matrix_data[a][b] = v if v != math.inf else "∞"
        df_fw = pd.DataFrame(matrix_data, index=ids, columns=ids)
        st.dataframe(df_fw.style.applymap(
            lambda v: "color: #f59e0b; font-weight:bold" if v == 0 else
                      ("color: #ef4444" if v == "∞" else "color: #10b981")
        ), use_container_width=True)

        st.markdown("**Rekomendasi Rute dari Gudang (G):**")
        rec_rows = []
        for nid in ids:
            if nid == "G":
                continue
            d = fw_dist["G"][nid]
            path = g.get_fw_path(nxt, idx, ids, "G", nid)
            unit = {"jarak": "km", "waktu": "mnt", "biaya": "Rp"}[weight_fw]
            val = f"Rp{d:,.0f}" if weight_fw == "biaya" else f"{d} {unit}"
            rec_rows.append({
                "Tujuan": f"{nid} – {g.nodes[nid]}",
                f"Nilai Optimal": val if d != math.inf else "❌ Tidak terjangkau",
                "Rute": " → ".join(path) if path else "-"
            })
        st.dataframe(pd.DataFrame(rec_rows), use_container_width=True, hide_index=True)

with tab4:
    st.markdown('<div class="section-header">Data Node & Edge</div>', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Daftar Node**")
        df_nodes = pd.DataFrame([{"ID": k, "Nama": v} for k, v in g.nodes.items()])
        st.dataframe(df_nodes, use_container_width=True, hide_index=True)
    with col_t2:
        st.markdown("**Daftar Edge**")
        df_edges = pd.DataFrame(g.edges, columns=["Dari", "Ke", "Jarak (km)", "Waktu (mnt)", "Biaya (Rp)"])
        st.dataframe(df_edges, use_container_width=True, hide_index=True)

    st.markdown("**Adjacency Matrix (Jarak km)**")
    matrix, ids_m = g.get_adjacency_matrix_display()
    df_adj = pd.DataFrame(
        {i: {j: (matrix[i][j] if matrix[i][j] != math.inf else "∞") for j in ids_m} for i in ids_m},
        index=ids_m
    )
    st.dataframe(df_adj, use_container_width=True)

with tab5:
    st.markdown('<div class="section-header">Tentang Sistem</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Deskripsi Sistem
    DSS ini membantu pelaku UMKM di Bali menentukan **rute distribusi paling efisien**
    dari gudang ke titik-titik pengiriman berdasarkan **jarak, waktu, atau biaya BBM**.

    ---
    ### 🔵 Struktur Graph
    | Aspek | Detail |
    |---|---|
    | Jenis | Directed Weighted Graph |
    | Representasi | Adjacency List + Adjacency Matrix |
    | Node | Lokasi distribusi |
    | Edge | Rute antar lokasi dengan bobot |

    ---
    ### ⚙️ Algoritma
    **Dijkstra** — O((V+E) log V) — rute terpendek satu sumber

    **Floyd-Warshall** — O(V³) — semua pasangan jarak terpendek

    ---
    ### 📦 Teknologi
    Python · Streamlit · NetworkX · Matplotlib · Pandas
    """)
