from pathlib import Path
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from Algorithms import MCEDH

# Directories
RAW_RESULTS_DIR = BASE_DIR.parent / "Results" / "Raw"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

POINT_GENERATOR_DIR = BASE_DIR.parent / "Generators" / "PointGenerator"

TASK_FILE = POINT_GENERATOR_DIR / "Tasks.txt"
UTIL_FILE = POINT_GENERATOR_DIR / "Utilizations.txt"

# Run algorithm
MCEDH.run(TASK_FILE, UTIL_FILE)

MCEDH_AcceptanceRatio = []
MCEDH_AcceptanceRatioLo = []
MCEDH_AcceptanceRatioHi = []
MCEDH_Utilization = []

# Calculate results
for i in range(101):

    MCEDH_Utilization.append(i / 100)

    if MCEDH.AcceptanceRatioArray[0][i] == 0:
        MCEDH.AcceptanceRatioArray[0][i] = 1

    count = MCEDH.AcceptanceRatioArray[0][i]

    MCEDH_AcceptanceRatio.append(
        (MCEDH.AcceptanceRatioArray[1][i] / count) * 10
    )

    MCEDH_AcceptanceRatioLo.append(
        (MCEDH.AcceptanceRatioArray[2][i] / count) * 10
    )

    MCEDH_AcceptanceRatioHi.append(
        (MCEDH.AcceptanceRatioArray[3][i] / count) * 10
    )

print("MCEDH_AcceptanceRatioLo =", MCEDH_AcceptanceRatioLo)
print("MCEDH_AcceptanceRatioHi =", MCEDH_AcceptanceRatioHi)

# Save results
with open(RAW_RESULTS_DIR / "MCEDHResultLo.txt", "w") as f:
    print(MCEDH_AcceptanceRatioLo[6:], file=f)

with open(RAW_RESULTS_DIR / "MCEDHResultHi.txt", "w") as f:
    print(MCEDH_AcceptanceRatioHi[6:], file=f)

with open(RAW_RESULTS_DIR / "MCEDHResult.txt", "w") as f:
    print(MCEDH_AcceptanceRatio[6:], file=f)

print(f"\nResults saved to: {RAW_RESULTS_DIR}")