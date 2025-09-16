
from time import perf_counter
from pathlib import Path

def parse_graph_adjlst(file_path):
    file_path = Path(file_path)
    edges = []
    max_node = -1
    first = None
    with file_path.open('r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split()
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
    n_hint = m_hint = None
    if first is not None and len(first) >= 2 and all(p.lstrip("-").isdigit() for p in first[:2]):
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
    return adj, n, m

def kcore_montresor(adj):
    n = len(adj)
    val = [len(adj[v]) for v in range(n)]
    changed = True
    rounds = 0
    start = perf_counter()
    while changed:
        changed = False
        rounds += 1
        new_val = val[:]
        for v in range(n):
            maxk = val[v]
            if maxk <= 0:
                continue
            c = [0]*(maxk+1)
            for u in adj[v]:
                j = val[u] if val[u] <= maxk else maxk
                c[j] += 1
            cumul = 0
            new_bound = val[v]
            for i in range(maxk, 0, -1):
                cumul += c[i]
                if cumul >= i:
                    new_bound = i
                    break
            if new_bound < val[v]:
                new_val[v] = new_bound
                changed = True
        val = new_val
    elapsed_ms = (perf_counter() - start) * 1000.0
    return val, (max(val) if val else 0), elapsed_ms, rounds

def kcore_bz(adj):
    n = len(adj)
    if n == 0:
        return [], 0, 0.0
    deg = [len(adj[v]) for v in range(n)]
    maxd = max(deg)
    bin_counts = [0]*(maxd+1)
    for d in deg:
        bin_counts[d] += 1
    start_pos = [0]*(maxd+1)
    cur = 0
    for d in range(maxd+1):
        start_pos[d], cur = cur, cur + bin_counts[d]
    vert = [0]*n
    pos = [0]*n
    next_pos = start_pos[:]
    for v in range(n):
        d = deg[v]
        vert[next_pos[d]] = v
        pos[v] = next_pos[d]
        next_pos[d] += 1
    start = perf_counter()
    for i in range(n):
        v = vert[i]
        for u in adj[v]:
            if deg[u] > deg[v]:
                du = deg[u]
                pu = pos[u]
                pw = start_pos[du]
                w = vert[pw]
                if u != w:
                    vert[pu], vert[pw] = vert[pw], vert[pu]
                    pos[u], pos[w] = pw, pu
                start_pos[du] += 1
                deg[u] -= 1
    elapsed_ms = (perf_counter() - start) * 1000.0
    return deg, (max(deg) if deg else 0), elapsed_ms

if __name__ == "__main__":
    import sys, json
    fp = sys.argv[1] if len(sys.argv) > 1 else "amaze.txt"
    adj, n, m = parse_graph_adjlst(fp)
    core_m, kmax_m, t_m_ms, rounds = kcore_montresor(adj)
    core_bz, kmax_bz, t_bz_ms = kcore_bz(adj)
    out = {
        "dataset": fp,
        "vertices": n,
        "edges": m,
        "decomposition_time_ms": round(t_m_ms, 3),
        "decomposition_k_max": int(kmax_m),
        "WG_BZ_time_ms": round(t_bz_ms, 3),
        "WG_BZ_k_max": int(kmax_bz),
        "montresor_rounds": rounds
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
