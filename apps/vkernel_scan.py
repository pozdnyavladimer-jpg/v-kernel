import re
import sys
import numpy as np

STATE_KEYS = [
    "red_mass",
    "orange_flow",
    "yellow_struct",
    "green_balance",
    "blue_law",
    "violet_future",
]


def encode_text_to_state(text):
    text_lower = text.lower()

    v = {
        "red_mass": 0.15,
        "orange_flow": 0.15,
        "yellow_struct": 0.15,
        "green_balance": 0.15,
        "blue_law": 0.15,
        "violet_future": 0.15,
    }

    # General instability
    if any(w in text_lower for w in ["error", "fail", "problem", "unstable"]):
        v["red_mass"] += 0.20

    # SAFE loop (for) → good structure
    if re.search(r"\bfor\b", text_lower):
        v["orange_flow"] += 0.10
        v["yellow_struct"] += 0.05

    # while → potentially risky
    if re.search(r"\bwhile\b", text_lower):
        v["red_mass"] += 0.18
        v["orange_flow"] -= 0.05

    # dangerous infinite loop
    if re.search(r"while\s+true\s*:", text_lower):
        v["red_mass"] += 0.45
        v["orange_flow"] -= 0.20
        v["green_balance"] -= 0.20
        v["blue_law"] -= 0.10

    # empty pass
    if re.search(r"\bpass\b", text_lower):
        v["red_mass"] += 0.12
        v["yellow_struct"] -= 0.08
        v["green_balance"] -= 0.08

    # deadlocks / stuck
    if any(w in text_lower for w in ["loop", "stuck", "deadlock", "blocked"]):
        v["red_mass"] += 0.25
        v["orange_flow"] -= 0.05

    # bare except
    if re.search(r"except\s*:", text_lower):
        v["green_balance"] -= 0.20
        v["yellow_struct"] -= 0.10
        v["blue_law"] -= 0.05
        v["red_mass"] += 0.15

    # structure
    if re.search(r"\bdef\b|\bclass\b", text_lower):
        v["yellow_struct"] += 0.25
        v["blue_law"] += 0.10

    # control logic
    if re.search(r"\bif\b|\breturn\b", text_lower):
        v["blue_law"] += 0.18
        v["green_balance"] += 0.08

    # healthy processing
    if any(w in text_lower for w in ["result", "append", "process"]):
        v["yellow_struct"] += 0.10
        v["green_balance"] += 0.08

    # adaptive
    if any(w in text_lower for w in ["retry", "adapt", "fallback"]):
        v["violet_future"] += 0.20
        v["green_balance"] += 0.08

    # normalize
    total = sum(max(v[k], 0.0) for k in v)
    return np.array([max(v[k], 0.0) / total for k in STATE_KEYS])


def run_convergence(z0, steps=30, alpha=0.6, beta=0.2):
    z = z0.copy()
    history = [z.copy()]

    for _ in range(steps):
        mean = np.mean(z)
        z = z + alpha * (mean - z)
        z = z - beta * (z ** 3)
        z = np.maximum(z, 0)
        z = z / (np.sum(z) + 1e-9)
        history.append(z.copy())

    return np.array(history)


def compute_metrics(history, z0=None):
    final = history[-1]

    if z0 is None:
        z0 = history[0]

    coherence = float(np.max(final))
    shadow = float(np.std(final))
    vitality = float(np.mean(np.abs(np.diff(history, axis=0))))

    initial_pressure = float(z0[0])
    initial_flow = float(z0[1])
    initial_structure = float(z0[2])
    initial_balance = float(z0[3])
    initial_law = float(z0[4])
    initial_future = float(z0[5])

    initial_risk = (
        1.35 * initial_pressure
        + 0.45 * max(0.0, 0.18 - initial_flow)
        + 0.80 * max(0.0, 0.18 - initial_balance)
        + 0.55 * max(0.0, 0.18 - initial_structure)
        + 0.35 * max(0.0, 0.18 - initial_law)
    )

    stability_score = (
        0.85 * initial_structure
        + 0.85 * initial_balance
        + 0.65 * initial_law
        + 0.25 * initial_future
        - 1.25 * initial_pressure
        - 0.50 * vitality
    )

    return {
        "coherence": coherence,
        "shadow": shadow,
        "vitality": vitality,
        "score": float(stability_score),
        "risk": float(initial_risk),
        "mode": int(np.argmax(z0)),
        "state": {
            "red_mass": initial_pressure,
            "orange_flow": initial_flow,
            "yellow_struct": initial_structure,
            "green_balance": initial_balance,
            "blue_law": initial_law,
            "violet_future": initial_future,
        },
    }


def classify(metrics):
    risk = metrics["risk"]
    score = metrics["score"]

    if risk > 0.34 or score < 0.02:
        return "LOW", "instability detected"
    elif risk > 0.22 or score < 0.13:
        return "MEDIUM", "review recommended"
    else:
        return "HIGH", "stable structure"


def explain_risk(metrics):
    state = metrics["state"]
    reasons = []

    if state["red_mass"] > 0.28:
        reasons.append("high pressure / instability signal")

    if state["orange_flow"] < 0.10:
        reasons.append("low flow / blocked execution")

    if state["green_balance"] < 0.10:
        reasons.append("low balance / weak recovery structure")

    if state["yellow_struct"] < 0.10:
        reasons.append("weak structural signal")

    if state["blue_law"] < 0.10:
        reasons.append("weak rule / validation signal")

    if not reasons:
        reasons.append("no major instability pattern detected")

    return reasons


def scan_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    z0 = encode_text_to_state(text)
    history = run_convergence(z0)
    metrics = compute_metrics(history, z0)

    level, label = classify(metrics)
    reasons = explain_risk(metrics)

    print("\n=== V-KERNEL STABILITY REPORT ===")
    print(f"File: {path}")
    print(f"Mode: {metrics['mode']} ({STATE_KEYS[metrics['mode']]})")
    print(f"Stability: {level}")
    print(f"Label: {label}")
    print(f"Score: {metrics['score']:.4f}")
    print(f"Risk: {metrics['risk']:.4f}")
    print(f"Coherence: {metrics['coherence']:.4f}")
    print(f"Shadow: {metrics['shadow']:.4f}")
    print(f"Vitality: {metrics['vitality']:.4f}")

    print("\nState:")
    for k, v in metrics["state"].items():
        print(f"  {k:15}: {v:.4f}")

    print("\nReason:")
    for r in reasons:
        print(f"  - {r}")

    print("=================================\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apps/vkernel_scan.py <file.py>")
    else:
        scan_file(sys.argv[1])
