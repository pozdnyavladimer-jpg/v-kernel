import random
import math

-------------------------

CONFIG

-------------------------

NUM_NODES = 30
CONNECTION_PROB = 0.15
NOISE_LEVEL = 0.3
PRUNE_THRESHOLD = 0.1
ITERATIONS = 20

-------------------------

GRAPH INIT

-------------------------

nodes = {i: {"value": random.random()} for i in range(NUM_NODES)}
edges = {}

for i in range(NUM_NODES):
for j in range(NUM_NODES):
if i != j and random.random() < CONNECTION_PROB:
edges[(i, j)] = random.random()

-------------------------

FUNCTIONS

-------------------------

def forward_pass(nodes, edges):
new_nodes = {}
for i in nodes:
total = 0
for (a, b), w in edges.items():
if b == i:
total += nodes[a]["value"] * w
new_nodes[i] = {"value": total}
return new_nodes

def backward_pass(nodes):
# normalize values (simulate validation)
total = sum(abs(n["value"]) for n in nodes.values()) + 1e-6
for i in nodes:
nodes[i]["value"] /= total
return nodes

def add_noise(nodes):
for i in nodes:
nodes[i]["value"] += random.uniform(-NOISE_LEVEL, NOISE_LEVEL)
return nodes

def prune(edges):
to_delete = []
for k, w in edges.items():
if abs(w) < PRUNE_THRESHOLD:
to_delete.append(k)

for k in to_delete:
    del edges[k]

return len(to_delete)

def reinforce(edges):
for k in edges:
edges[k] *= 1.05  # strengthen
return edges

def coherence(nodes):
values = [n["value"] for n in nodes.values()]
mean = sum(values) / len(values)
variance = sum((v - mean) ** 2 for v in values) / len(values)
return 1 / (1 + variance)

-------------------------

MAIN LOOP

-------------------------

print("=== V-KERNEL SIMULATION START ===")

for step in range(ITERATIONS):

# 1. add entropy
nodes = add_noise(nodes)

# 2. forward pass
nodes = forward_pass(nodes, edges)

# 3. backward validation
nodes = backward_pass(nodes)

# 4. compute coherence (Bindu)
coh = coherence(nodes)

# 5. reinforce stable paths
edges = reinforce(edges)

# 6. prune weak connections
removed = prune(edges)

print(f"[STEP {step}] coherence={coh:.4f} edges={len(edges)} pruned={removed}")

print("=== SIMULATION END ===")
