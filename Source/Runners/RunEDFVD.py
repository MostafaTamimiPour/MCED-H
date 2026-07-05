from pathlib import Path
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from Algorithms import EDFVD

# Directories
POINT_GENERATOR_DIR = BASE_DIR.parent / "Generators" / "PointGenerator"

TASK_FILE = POINT_GENERATOR_DIR / "Tasks.txt"
UTIL_FILE = POINT_GENERATOR_DIR / "Utilizations.txt"

RAW_RESULTS_DIR = BASE_DIR.parent / "Results" / "Raw"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Run algorithm
EDFVD.run(TASK_FILE, UTIL_FILE)

EDFVD_AcceptanceRatio = []
EDFVD_AcceptanceRatioLo = []
EDFVD_AcceptanceRatioHi = []
EDFVD_Utilization = []

# Calculate results
for i in range(101):

    EDFVD_Utilization.append(i / 100)

    if EDFVD.AcceptanceRatioArray[0][i] == 0:
        EDFVD.AcceptanceRatioArray[0][i] = 1

    count = EDFVD.AcceptanceRatioArray[0][i]

    EDFVD_AcceptanceRatio.append(
        (EDFVD.AcceptanceRatioArray[1][i] / count) * 10
    )

    EDFVD_AcceptanceRatioLo.append(
        (EDFVD.AcceptanceRatioArray[2][i] / count) * 10
    )

    EDFVD_AcceptanceRatioHi.append(
        (EDFVD.AcceptanceRatioArray[3][i] / count) * 10
    )

print("EDFVD_AcceptanceRatioLo =", EDFVD_AcceptanceRatioLo)
print("EDFVD_AcceptanceRatioHi =", EDFVD_AcceptanceRatioHi)

# Save results
with open(RAW_RESULTS_DIR / "EDFVDResultLo.txt", "w") as f:
    print(EDFVD_AcceptanceRatioLo[6:], file=f)

with open(RAW_RESULTS_DIR / "EDFVDResultHi.txt", "w") as f:
    print(EDFVD_AcceptanceRatioHi[6:], file=f)

with open(RAW_RESULTS_DIR / "EDFVDResult.txt", "w") as f:
    print(EDFVD_AcceptanceRatio[6:], file=f)

print(f"\nResults saved to: {RAW_RESULTS_DIR}")