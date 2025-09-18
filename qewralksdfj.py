python3 - <<'PY'
import csv, collections
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path("/home/aairobots/catkin_ws/src/hw1/submission/hw1_results.csv")
out_dir  = Path("/home/aairobots/catkin_ws/src/hw1/submission/")
out_dir.mkdir(parents=True, exist_ok=True)

def norm(s: str) -> str:
    return s.strip().lower().replace(" ", "_")


with csv_path.open(newline='') as f:
    r0 = csv.reader(f)
    headers = next(r0)
    norm_headers = [norm(h) for h in headers]
    idx = {h:i for i,h in enumerate(norm_headers)}
    need = ["dimension","algorithm","time","nodes_expanded","error"]
    missing = [k for k in need if k not in idx]
    if missing:
        raise SystemExit(f"CSV header keys missing (normalized): {missing}\n"
                         f"Found headers: {norm_headers}")

    time_map  = collections.defaultdict(list)
    nodes_map = collections.defaultdict(list)

    for row in r0:
        err = row[idx["error"]].strip().lower() if row[idx["error"]] is not None else ""
        if err not in ("", "none"):
            continue

        dim = row[idx["dimension"]].strip()
        alg = row[idx["algorithm"]].strip()

        try:
            t = float(row[idx["time"]])
        except:
            continue
        try:
            n = int(row[idx["nodes_expanded"]])
        except:
            try:
                n = int(float(row[idx["nodes_expanded"]]))
            except:
                continue

        time_map[(dim,alg)].append(t)
        nodes_map[(dim,alg)].append(n)

dims = sorted({d for (d,_) in time_map.keys()})
algs = ['bfs','ucs','gbfs','astar','custom-astar']
avg  = lambda xs: sum(xs)/len(xs) if xs else 0.0


plt.figure()
for alg in algs:
    ys = [avg(time_map.get((d,alg), [])) for d in dims]
    if any(ys):
        plt.plot(dims, ys, marker='o', label=alg)
plt.xlabel("Grid Dimension")
plt.ylabel("Average Time")
plt.title("Task 2: Avg Time vs Dimension")
plt.legend()
plt.grid(True, linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.savefig(out_dir/"task2.png")

plt.figure()
for alg in algs:
    ys = [avg(nodes_map.get((d,alg), [])) for d in dims]
    if any(ys):
        plt.plot(dims, ys, marker='o', label=alg)
plt.xlabel("Grid Dimension")
plt.ylabel("Average Nodes Expanded")
plt.title("Task 3: Avg Nodes vs Dimension")
plt.legend()
plt.grid(True, linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.savefig(out_dir/"task3.png")

print("Saved:", out_dir/"task2.png", "and", out_dir/"task3.png")
PY
