python3 - <<'PY'
import csv, collections
import matplotlib.pyplot as plt

csv_path = "/home/aairobots/catkin_ws/src/hw1/submission/hw1_results.csv"
out_dir  = "/home/aairobots/catkin_ws/src/hw1/submission/"

time_map  = collections.defaultdict(list)
nodes_map = collections.defaultdict(list)

with open(csv_path, newline='') as f:
    r = csv.DictReader(f)
    for row in r:
        if row.get('Error','').strip().lower() not in ('', 'none'):
            continue
        d = row['Dimension'].strip()
        a = row['Algorithm'].strip()
        try:
            t = float(row['Time']); n = int(row['Nodes Expanded'])
        except: 
            continue
        time_map[(d,a)].append(t)
        nodes_map[(d,a)].append(n)

dims = sorted({d for (d,_) in time_map.keys()})
algs = ['bfs','ucs','gbfs','astar','custom-astar']
avg  = lambda xs: sum(xs)/len(xs) if xs else 0.0

# Task 2
plt.figure()
for alg in algs:
    ys = [avg(time_map.get((d,alg), [])) for d in dims]
    if any(ys): plt.plot(dims, ys, marker='o', label=alg)
plt.xlabel("Grid Dimension"); plt.ylabel("Average Time")
plt.title("Task 2: Avg Time vs Dimension"); plt.legend(); plt.grid(True, ls=':', lw=0.5)
plt.tight_layout(); plt.savefig(out_dir+"task2.png")

# Task 3
plt.figure()
for alg in algs:
    ys = [avg(nodes_map.get((d,alg), [])) for d in dims]
    if any(ys): plt.plot(dims, ys, marker='o', label=alg)
plt.xlabel("Grid Dimension"); plt.ylabel("Average Nodes Expanded")
plt.title("Task 3: Avg Nodes vs Dimension"); plt.legend(); plt.grid(True, ls=':', lw=0.5)
plt.tight_layout(); plt.savefig(out_dir+"task3.png")
print("Saved task2.png, task3.png")
PY
