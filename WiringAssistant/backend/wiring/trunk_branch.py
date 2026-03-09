from collections import defaultdict
from typing import Dict, List, Tuple


def label_trunk_and_branches(
    mst_edges: List[Tuple[int, int]],
    num_nodes: int,
    panel_index: int = 0,
):
    """
    mst_edges: list of (i, j) edges
    Node 0 is assumed to be the panel
    Returns: dict[(i,j)] -> "trunk" | "branch"
    """

    adj = defaultdict(list)
    for i, j in mst_edges:
        adj[i].append(j)
        adj[j].append(i)

    labels: Dict[Tuple[int, int], str] = {}

    def dfs(u, parent):
        children = [v for v in adj[u] if v != parent]

        for v in children:
            # Leaf outlet → branch
            if len(adj[v]) == 1:
                labels[(u, v)] = labels[(v, u)] = "branch"
            else:
                labels[(u, v)] = labels[(v, u)] = "trunk"

            dfs(v, u)

    dfs(panel_index, None)
    return labels
