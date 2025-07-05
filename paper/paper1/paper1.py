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

# === PLL索引构建（优化剪枝版） ===
def pll_index(graph, rev_graph, n):
    LOUT = [[] for _ in range(n)]
    LIN = [[] for _ in range(n)]

    # 顺序排序（根据出入度）
    order = sorted(range(n), key=lambda v: (len(rev_graph[v]) + 1) * (len(graph[v]) + 1), reverse=True)

    for v in order:
        visited = [False] * n

        # 正向BFS：构建 LIN
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if visited[u]: continue
            visited[u] = True

            if intersect_sorted(LOUT[v], LIN[u]):
                continue
            insert_sorted(LIN[u], v)
            queue.extend(graph[u])

        visited = [False] * n

        # 反向BFS：构建 LOUT
        queue = deque([v])
        while queue:
            u = queue.popleft()
            if visited[u]: continue
            visited[u] = True

            if intersect_sorted(LOUT[u], LIN[v]):
                continue
            insert_sorted(LOUT[u], v)
            queue.extend(rev_graph[u])

    return LOUT, LIN

# === PPL索引构建（优化路径标记剪枝版） ===
def ppl_index(graph, rev_graph, n):
    LOUT = [{} for _ in range(n)]  # dict: path_id -> position
    LIN = [{} for _ in range(n)]

    # 改进的路径选择策略：选择最长的链式路径
    paths = []
    used = [False] * n
    
    # 按出度排序，优先选择出度小的节点作为路径起点
    candidates = sorted(range(n), key=lambda v: len(graph[v]))
    
    for v in candidates:
        if used[v] or len(graph[v]) == 0:
            continue
            
        # 寻找最长链式路径
        path = []
        u = v
        while not used[u] and len(graph[u]) == 1:
            path.append(u)
            used[u] = True
            u = graph[u][0]
            if u >= n or u in path:  # 避免循环
                break
                
        if len(path) >= 3:  # 只保留长度>=3的路径
            paths.append(path)
    
    # 限制路径数量，避免过多路径
    if len(paths) > n // 10:  # 最多保留 n/10 条路径
        paths = sorted(paths, key=len, reverse=True)[:n//10]
    
    for pid, path in enumerate(paths):
        plen = len(path)

        # 正向 BFS：构建 LIN（优化剪枝）
        for j in reversed(range(plen)):
            src = path[j]
            visited = [False] * n
            queue = deque([src])
            
            while queue:
                u = queue.popleft()
                if visited[u]: continue
                visited[u] = True
                
                # 优化剪枝条件：检查是否已有更优的路径覆盖
                skip = False
                for existing_pid in LIN[u]:
                    if existing_pid < pid:  # 只检查已处理的路径
                        continue
                    if existing_pid in LOUT[src]:
                        skip = True
                        break
                
                if skip:
                    continue
                    
                LIN[u][pid] = j
                queue.extend(graph[u])

        # 反向 BFS：构建 LOUT（优化剪枝）
        for j in range(plen):
            src = path[j]
            visited = [False] * n
            queue = deque([src])
            
            while queue:
                u = queue.popleft()
                if visited[u]: continue
                visited[u] = True
                
                # 优化剪枝条件：检查是否已有更优的路径覆盖
                skip = False
                for existing_pid in LOUT[u]:
                    if existing_pid < pid:  # 只检查已处理的路径
                        continue
                    if existing_pid in LIN[src]:
                        skip = True
                        break
                
                if skip:
                    continue
                    
                LOUT[u][pid] = j
                queue.extend(rev_graph[u])

    return LOUT, LIN

# === 查询 ===
def query(s, t, LOUT, LIN):
    # PLL 情况：标签是 list
    if isinstance(LOUT[s], list):
        return intersect_sorted(LOUT[s], LIN[t])
    # PPL 情况：标签是 dict（path_id -> position）
    elif isinstance(LOUT[s], dict):
        for pid in LOUT[s]:
            if pid in LIN[t] and LOUT[s][pid] <= LIN[t][pid]:
                return True
        return False
    else:
        raise TypeError("Unsupported label type")

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
    print(f"{'PPL' if use_ppl else 'PLL'}")
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
