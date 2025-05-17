import networkx as nx
import pydot
from matplotlib import pyplot as plt

# Створюємо спрямований граф
G = nx.DiGraph()

# Додаємо вузли з мітками (блоки коду)
nodes = {
    "n0": "Start",
    "n1": "if not username or not password",
    "n2": 'return "Missing credentials"',
    "n3": "if username not in db",
    "n4": 'return "User not found"',
    "n5": 'attempts = db[username].get("attempts", 0)',
    "n6": "if attempts >= 3",
    "n7": 'return "Account locked"',
    "n8": 'if db[username]["password"] != password',
    "n9": 'db[username]["attempts"] = attempts + 1',
    "n10": 'return "Invalid password"',
    "n11": 'db[username]["attempts"] = 0',
    "n12": 'return "Authenticated"',
    "n13": "End"
}
for node, label in nodes.items():
    G.add_node(node, label=label)

# Додаємо ребра (переходи між блоками)
edges = [
    ("n0", "n1"),
    ("n1", "n2", {"label": "True"}),
    ("n1", "n3", {"label": "False"}),
    ("n2", "n13"),
    ("n3", "n4", {"label": "True"}),
    ("n3", "n5", {"label": "False"}),
    ("n4", "n13"),
    ("n5", "n6"),
    ("n6", "n7", {"label": "True"}),
    ("n6", "n8", {"label": "False"}),
    ("n7", "n13"),
    ("n8", "n9", {"label": "True"}),
    ("n8", "n11", {"label": "False"}),
    ("n9", "n10"),
    ("n10", "n13"),
    ("n11", "n12"),
    ("n12", "n13")
]
G.add_edges_from(edges)

# Знаходимо всі прості шляхи від n0 до n13
paths = list(nx.all_simple_paths(G, source="n0", target="n13"))
print("Шляхи виконання:")
for i, path in enumerate(paths, 1):
    # Виводимо мітки вузлів замість ідентифікаторів
    path_labels = [nodes[node] for node in path]
    print(f"Шлях {i}: {' -> '.join(path_labels)}")

# Розраховуємо цикломатичну складність
M = G.number_of_edges() - G.number_of_nodes() + 2
print(f"Цикломатична складність: {M}")

# Експортуємо граф у .dot-файл
nx.nx_pydot.write_dot(G, "cfg.dot")

# Візуалізація через matplotlib (без ідентифікаторів вузлів)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Фіксоване розташування для стабільності
# Малюємо граф без міток ідентифікаторів
nx.draw(G, pos, with_labels=False, node_color="lightblue", node_size=2000, font_size=10, arrowsize=20)
# Додаємо лише мітки вузлів (атрибут label)
labels = nx.get_node_attributes(G, "label")
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="normal")
# Додаємо мітки ребер (True/False)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
plt.title("Control Flow Graph (CFG)")
plt.tight_layout()
plt.show()