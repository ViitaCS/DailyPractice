import time
import openpyxl
import argparse

def load_directed_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        head = f.readline().strip().split()
        if len(head) < 2:
            raise ValueError("首行应为: n m")
        n, m = map(int, head)
        out_edges = [[] for _ in range(n)]
        for line in f:
            parts = list(map(int, line.strip().split()))
            if not parts:
                continue
            u = parts[0]
            k = parts[1] if len(parts) > 1 else 0
            vs = parts[2:2+k]
            out_edges[u].extend(vs)
    return out_edges, n

def symmetrize_to_undirected(out_edges):
    n = len(out_edges)
    adj = [set() for _ in range(n)]
    for u in range(n):
        for v in out_edges[u]:
            if u != v:
                adj[u].add(v)
                adj[v].add(u)
    return [sorted(list(s)) for s in adj]

def max_clique_exact(adj):
    n = len(adj)
    adj_sets = [set(neis) for neis in adj]
    order = sorted(range(n), key=lambda x: len(adj[x]), reverse=True)
    best = 0

    def expand(R, P):
        nonlocal best
        if not P:
            if len(R) > best:
                best = len(R)
            return
        P_order = sorted(P, key=lambda v: len(adj[v]), reverse=True)
        colors = []
        bounds = []
        for v in P_order:
            placed = False
            for color in colors:
                if all(u not in adj_sets[v] for u in color):
                    color.add(v)
                    placed = True
                    break
            if not placed:
                colors.append({v})
            bounds.append(len(colors))

        for idx in range(len(P_order) - 1, -1, -1):
            v = P_order[idx]
            if len(R) + bounds[idx] <= best:
                return
            R_new = R + [v]
            P_new = [u for u in P_order[:idx] if u in adj_sets[v]]
            expand(R_new, P_new)

    P0 = [v for v in order if len(adj[v]) > 0]
    if not P0 and n > 0:
        return 1
    expand([], P0)
    if best == 0 and n > 0:
        best = 1
    return best

def max_clique_greedy_ego(adj):
    n = len(adj)
    if n == 0:
        return 0
    adj_sets = [set(neis) for neis in adj]
    best = 1

    def greedy_from(seed):
        cand = list(adj_sets[seed])
        cand.sort(key=lambda v: len(adj_sets[v] & adj_sets[seed]), reverse=True)
        clique = [seed]
        clique_set = {seed}
        for v in cand:
            if all((v in adj_sets[u]) for u in clique_set):
                clique.append(v)
                clique_set.add(v)
        return len(clique)

    order = sorted(range(n), key=lambda v: len(adj[v]), reverse=True)
    for v in order[: min(n, 2000)]:  
        best = max(best, greedy_from(v))
    return best

def run(graph_path, dataset_name, out_xlsx=None):
    out_edges, n = load_directed_graph(graph_path)
    adj = symmetrize_to_undirected(out_edges)
    m_undirected = sum(len(nei) for nei in adj) // 2

    t0 = time.time()
    omega = max_clique_exact(adj)
    t1 = time.time()
    elapsed_ms = (t1 - t0) * 1000.0

    result = {
        "数据集名称": dataset_name,
        "顶点数": n,
        "边数": m_undirected,
        "算法时间(ms)": round(elapsed_ms, 4),
        "算法最大团": int(omega),
    }
    print(result)

    if out_xlsx:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["数据集名称", "顶点数", "边数", "算法时间(ms)", "算法最大团"])
        ws.append([dataset_name, n, m_undirected, round(elapsed_ms, 4), int(omega)])
        wb.save(out_xlsx)
        print("Excel 已写入：", out_xlsx)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", default="../amaze.txt", help="图文件路径（amaze.txt 格式）")
    parser.add_argument("--name",  default="amaze", help="数据集名称")
    parser.add_argument("--xlsx",  default="", help="可选：输出Excel路径")
    args = parser.parse_args()
    run(args.graph, args.name, args.xlsx if args.xlsx else None)
