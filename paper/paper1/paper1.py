import time
import psutil
from openpyxl import Workbook
import os
from collections import deque
from bisect import bisect_left

# === 图加载 ===
def load_graph_from_custom_txt(path):
    with open(path) as f:
        lines = f.readlines()
    n, m = map(int, lines[0].split())
    graph = [[] for _ in range(n)]
    rev_graph = [[] for _ in range(n)]
    for line in lines[1:]:
        parts = list(map(int, line.strip().split()))
        if len(parts) < 2:
            continue
        u = parts[0]
        out_deg = parts[1]
        for v in parts[2:2+out_deg]:
            graph[u].append(v)
            rev_graph[v].append(u)
    return graph, rev_graph, n

# === 有序插入+去重 ===
def insert_sorted(lst, value):
    i = bisect_left(lst, value)
    if i == len(lst) or lst[i] != value:
        lst.insert(i, value)

def intersect_sorted(a, b):
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            return True
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return False

# === PLL索引构建 ===
def pll_index(graph, rev_graph, n):
    LOUT = [[] for _ in range(n)]
    LIN = [[] for _ in range(n)]
    def d_in_out(v):
        return (len(rev_graph[v]) + 1) * (len(graph[v]) + 1)
    order = sorted(range(n), key=d_in_out, reverse=True)
    for v in order:
        visited = set()
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if u in visited: continue
            visited.add(u)
            if intersect_sorted(LOUT[v], LIN[u]): continue
            insert_sorted(LIN[u], v)
            queue.extend(graph[u])
        visited.clear()
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if u in visited: continue
            visited.add(u)
            if intersect_sorted(LOUT[u], LIN[v]): continue
            insert_sorted(LOUT[u], v)
            queue.extend(rev_graph[u])
    return LOUT, LIN

# === PPL索引构建（简化） ===
def ppl_index(graph, rev_graph, n):
    LOUT = [[] for _ in range(n)]
    LIN = [[] for _ in range(n)]
    def d_in_out(v):
        return (len(rev_graph[v]) + 1) * (len(graph[v]) + 1)
    order = sorted(range(n), key=d_in_out, reverse=True)
    for v in order:
        visited = set()
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if u in visited: continue
            visited.add(u)
            if intersect_sorted(LOUT[v], LIN[u]):
                continue
            insert_sorted(LIN[u], v)
            queue.extend(graph[u])
        visited.clear()
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if u in visited: continue
            visited.add(u)
            if intersect_sorted(LIN[v], LOUT[u]):
                continue
            insert_sorted(LOUT[u], v)
            queue.extend(rev_graph[u])
    return LOUT, LIN

# === 查询 ===
def query(s, t, LOUT, LIN):
    return intersect_sorted(LOUT[s], LIN[t])

# === 查询数据加载 ===
def load_query_pairs(path):
    pairs = []
    with open(path) as f:
        for line in f:
            parts = list(map(int, line.strip().split()))
            if len(parts) == 2:
                pairs.append((parts[0], parts[1]))
    return pairs

# === 内存监测 ===
def measure_memory():
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

# === 评测 ===
def evaluate(graph_file, query_file, use_ppl=False):
    print(f"\n==== {'PPL' if use_ppl else 'PLL'} 测试 ====")
    graph, rev_graph, n = load_graph_from_custom_txt(graph_file)
    edge_count = sum(len(adj) for adj in graph)
    print(f"顶点数: {n}")
    print(f"边数: {edge_count}")
    t0 = time.time()
    mem0 = measure_memory()
    if use_ppl:
        LOUT, LIN = ppl_index(graph, rev_graph, n)
    else:
        LOUT, LIN = pll_index(graph, rev_graph, n)
    t1 = time.time()
    mem1 = measure_memory()
    index_time = (t1 - t0) * 1000  # ms
    index_size = mem1 - mem0       # MB
    queries = load_query_pairs(query_file)
    t2 = time.time()
    results = [query(u, v, LOUT, LIN) for u, v in queries]
    t3 = time.time()
    query_time = (t3 - t2) * 1000  # ms
    print(f"索引构建时间: {index_time:.2f} ms")
    print(f"索引大小: {index_size:.2f} MB")
    print(f"查询{len(queries)}条用时: {query_time:.2f} ms")
    return results

# === 主程序入口 ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python3 pll_algo.py amaze.txt amaze.txt-50")
        print("      python3 pll_algo.py amaze.txt amaze.txt-50 ppl  # 运行PPL")
        sys.exit(0)
    graph_file = sys.argv[1]
    query_file = sys.argv[2]
    use_ppl = len(sys.argv) > 3 and sys.argv[3].lower() == 'ppl'
    evaluate(graph_file, query_file, use_ppl=use_ppl)
