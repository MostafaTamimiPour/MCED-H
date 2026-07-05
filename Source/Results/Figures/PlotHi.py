import ast
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# Paths
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
RAW_RESULTS_DIR = BASE_DIR.parent / "Raw"


# =============================================================================
# Helper Function
# =============================================================================

def load_result(filename):
    with open(RAW_RESULTS_DIR / filename, "r") as f:
        return ast.literal_eval(f.read())


# =============================================================================
# Load Results
# =============================================================================

EDF_AcceptanceRatio = load_result("EDFResultHi.txt")
EDFVD_AcceptanceRatio = load_result("EDFVDResultHi.txt")
EDH_AcceptanceRatio = load_result("EDHResultHi.txt")
MCEDH_AcceptanceRatio = load_result("MCEDHResultHi.txt")
MCQPA_AcceptanceRatio = load_result("MCQPAResultHi.txt")


# =============================================================================
# Normalize Results
# =============================================================================

for result in (
    EDF_AcceptanceRatio,
    EDFVD_AcceptanceRatio,
    EDH_AcceptanceRatio,
    MCEDH_AcceptanceRatio,
    MCQPA_AcceptanceRatio,
):
    for i in range(len(result)):
        result[i] /= 10


# =============================================================================
# Utilization Values
# =============================================================================

Utilization = [round(i / 100, 2) for i in range(6, 101)]


# =============================================================================
# Plot
# =============================================================================

fig, ax = plt.subplots()

ax.plot(
    Utilization,
    EDFVD_AcceptanceRatio,
    linestyle=(0, ()),
    marker="o",
    color="#1f77b4",
    label="EDFVD",
)

ax.plot(
    Utilization,
    EDF_AcceptanceRatio,
    linestyle="-",
    marker="s",
    color="#ff7f0e",
    label="EDF",
)

ax.plot(
    Utilization,
    EDH_AcceptanceRatio,
    linestyle="--",
    marker="^",
    color="#2ca02c",
    label="EDH",
)

ax.plot(
    Utilization,
    MCEDH_AcceptanceRatio,
    linestyle="-.",
    marker="D",
    color="#d62728",
    label="MCEDH",
)

ax.plot(
    Utilization,
    MCQPA_AcceptanceRatio,
    linestyle=":",
    marker="x",
    color="#9467bd",
    label="MCQPA",
)

ax.set_xlabel("Average Utilization")
ax.set_ylabel("Normalized Acceptance Ratio")
ax.set_title("Acceptance Ratio vs Utilization for HI Tasks")

ax.set_xticks(np.arange(0.0, 1.01, 0.05))
ax.set_yticks(np.arange(0.0, 1.1, 0.1))

ax.grid(True)
ax.legend()

plt.show()