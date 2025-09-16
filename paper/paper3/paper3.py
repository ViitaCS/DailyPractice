from collections import defaultdict, deque
from time import perf_counter
from pathlib import Path
import json

def parse_graph_with_header(path):
    path = Path(path)
    n_hint = m_hint = None
    edges = []
    max_node = -1
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        first = None
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split()
            if first is None:
                first = parts
                continue
            u = int(parts[0]); deg = int(parts[1]); nbrs = list(map(int, parts[2:]))
            for v in nbrs:
                if u == v: 
                    continue
                a, b = (u, v) if u < v else (v, u)
                edges.append((a, b))
                if a > max_node: max_node = a
                if b > max_node: max_node = b
    if first and len(first) >= 2 and all(p.lstrip("-").isdigit() for p in first[:2]):
        n_hint, m_hint = int(first[0]), int(first[1])
    n = n_hint if n_hint is not None else (max_node + 1 if max_node >= 0 else 0)
    adj = [[] for _ in range(n)]
    seen = set()
    for a, b in edges:
        if (a, b) in seen: 
            continue
        seen.add((a, b))
        if a < n and b < n:
            adj[a].append(b); adj[b].append(a)
    m = len(seen)
    for v in range(n):
        adj[v].sort()
    return adj, n, m

def orient_graph(adj):
    n = len(adj)
    deg = [len(adj[v]) for v in range(n)]
    order = list(range(n))
    order.sort(key=lambda v: (deg[v], v))
    rank = [0]*n
    for i, v in enumerate(order):
        rank[v] = i
    fwd = [[] for _ in range(n)]
    for u in range(n):
        ru = rank[u]
        for v in adj[u]:
            if ru < rank[v]:
                fwd[u].append(v)
    for u in range(n):
        fwd[u].sort()
    return fwd, rank

def list_triangles(adj):
    n = len(adj)
    fwd, rank = orient_graph(adj)
    eid = {}
    edges = []
    def get_eid(a, b):
        if a > b: a, b = b, a
        key = (a, b)
        if key in eid: return eid[key]
        eid[key] = len(edges)
        edges.append(key)
        return eid[key]
    for u in range(n):
        for v in adj[u]:
            if u < v:
                get_eid(u, v)
    tri_edges = []
    edge_to_tris = defaultdict(list)
    for u in range(n):
        Nu = fwd[u]
        Nu_set = set(Nu)
        for v in Nu:
            Nv = fwd[v]
            if len(Nu) <= len(Nv):
                larger = set(Nv)
                for w in Nu:
                    if w in larger and w != v:
                        e_uv = get_eid(u, v)
                        e_uw = get_eid(u, w)
                        e_vw = get_eid(v, w) if v < w else get_eid(w, v)
                        t_id = len(tri_edges)
                        tri_edges.append((e_uv, e_uw, e_vw))
                        edge_to_tris[e_uv].append(t_id)
                        edge_to_tris[e_uw].append(t_id)
                        edge_to_tris[e_vw].append(t_id)
            else:
                larger = Nu_set
                for w in Nv:
                    if w in larger and w != v:
                        e_uv = get_eid(u, v)
                        e_uw = get_eid(u, w)
                        e_vw = get_eid(v, w) if v < w else get_eid(w, v)
                        t_id = len(tri_edges)
                        tri_edges.append((e_uv, e_uw, e_vw))
                        edge_to_tris[e_uv].append(t_id)
                        edge_to_tris[e_uw].append(t_id)
                        edge_to_tris[e_vw].append(t_id)
    return edges, tri_edges, edge_to_tris

def k_truss_algo1(adj):
    from heapq import heappush, heappop
    start = perf_counter()
    edges, tri_edges, e2t = list_triangles(adj)
    m_e = len(edges)
    sup = [len(e2t.get(i, [])) for i in range(m_e)]
    tri_alive = [True]*len(tri_edges)
    edge_alive = [True]*m_e
    truss = [-1]*m_e
    heap = []
    cur_sup = sup[:]
    in_heap = [True]*m_e
    for e in range(m_e):
        heappush(heap, (cur_sup[e], e))
    while heap:
        s, e = heappop(heap)
        if not in_heap[e]: 
            continue
        if s != cur_sup[e]:
            heappush(heap, (cur_sup[e], e))
            continue
        in_heap[e] = False
        edge_alive[e] = False
        truss[e] = s + 2
        for t_id in e2t.get(e, []):
            if not tri_alive[t_id]:
                continue
            a,b,c = tri_edges[t_id]
            x,y = (b,c) if a==e else ((a,c) if b==e else (a,b))
            tri_alive[t_id] = False
            for z in (x,y):
                if edge_alive[z] and cur_sup[z] > 0:
                    cur_sup[z] -= 1
                    heappush(heap, (cur_sup[z], z))
    kmax = max(truss) if truss else 2
    elapsed_ms = (perf_counter() - start) * 1000.0
    return edges, truss, kmax, elapsed_ms

def k_truss_algo2(adj):
    start = perf_counter()
    edges, tri_edges, e2t = list_triangles(adj)
    m_e = len(edges)
    sup = [len(e2t.get(i, [])) for i in range(m_e)]
    max_sup = max(sup) if sup else 0
    buckets = [deque() for _ in range(max_sup+1)]
    pos = [-1]*m_e
    for i, s in enumerate(sup):
        buckets[s].append(i)
        pos[i] = s
    edge_alive = [True]*m_e
    tri_alive = [True]*len(tri_edges)
    truss = [-1]*m_e
    cur_min = 0
    remaining = m_e
    while remaining > 0:
        while cur_min <= max_sup and not buckets[cur_min]:
            cur_min += 1
        if cur_min > max_sup:
            break
        e = buckets[cur_min].popleft()
        if not edge_alive[e]:
            continue
        edge_alive[e] = False
        remaining -= 1
        truss[e] = cur_min + 2
        for t_id in e2t.get(e, []):
            if not tri_alive[t_id]:
                continue
            a,b,c = tri_edges[t_id]
            x,y = (b,c) if a==e else ((a,c) if b==e else (a,b))
            tri_alive[t_id] = False
            for z in (x,y):
                if edge_alive[z]:
                    s_old = pos[z]
                    s_new = max(0, s_old - 1)
                    pos[z] = s_new
                    buckets[s_new].append(z)
    kmax = max(truss) if truss else 2
    elapsed_ms = (perf_counter() - start) * 1000.0
    return edges, truss, kmax, elapsed_ms

if __name__ == "__main__":
    import sys
    fp = sys.argv[1] if len(sys.argv) > 1 else "amaze.txt"
    adj, n, m = parse_graph_with_header(fp)
    e1, tr1, kmax1, t1 = k_truss_algo1(adj)
    e2, tr2, kmax2, t2 = k_truss_algo2(adj)
    out = {
        "dataset": fp,
        "vertices": n,
        "edges": m,
        "algo1_time_ms": round(t1, 3),
        "algo1_k_max": int(kmax1),
        "algo2_time_ms": round(t2, 3),
        "algo2_k_max": int(kmax2)
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
