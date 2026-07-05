from pathlib import Path
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from Algorithms import EDH

# Directories
POINT_GENERATOR_DIR = BASE_DIR.parent / "Generators" / "PointGenerator"

TASK_FILE = POINT_GENERATOR_DIR / "Tasks.txt"
UTIL_FILE = POINT_GENERATOR_DIR / "Utilizations.txt"

RAW_RESULTS_DIR = BASE_DIR.parent / "Results" / "Raw"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Run algorithm
EDH.run(TASK_FILE, UTIL_FILE)

EDH_AcceptanceRatio = []
EDH_AcceptanceRatioLo = []
EDH_AcceptanceRatioHi = []
EDH_Utilization = []

# Calculate results
for i in range(101):

    EDH_Utilization.append(i / 100)

    if EDH.AcceptanceRatioArray[0][i] == 0:
        EDH.AcceptanceRatioArray[0][i] = 1

    count = EDH.AcceptanceRatioArray[0][i]

    EDH_AcceptanceRatio.append(
        (EDH.AcceptanceRatioArray[1][i] / count) * 10
    )

    EDH_AcceptanceRatioLo.append(
        (EDH.AcceptanceRatioArray[2][i] / count) * 10
    )

    EDH_AcceptanceRatioHi.append(
        (EDH.AcceptanceRatioArray[3][i] / count) * 10
    )

print("EDH_AcceptanceRatioLo =", EDH_AcceptanceRatioLo)
print("EDH_AcceptanceRatioHi =", EDH_AcceptanceRatioHi)

# Save results
with open(RAW_RESULTS_DIR / "EDHResultLo.txt", "w") as f:
    print(EDH_AcceptanceRatioLo[6:], file=f)

with open(RAW_RESULTS_DIR / "EDHResultHi.txt", "w") as f:
    print(EDH_AcceptanceRatioHi[6:], file=f)

with open(RAW_RESULTS_DIR / "EDHResult.txt", "w") as f:
    print(EDH_AcceptanceRatio[6:], file=f)

print(f"\nResults saved to: {RAW_RESULTS_DIR}")