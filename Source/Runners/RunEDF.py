from pathlib import Path
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from Algorithms import EDF

# Directories
POINT_GENERATOR_DIR = BASE_DIR.parent / "Generators" / "PointGenerator"

TASK_FILE = POINT_GENERATOR_DIR / "Tasks.txt"
UTIL_FILE = POINT_GENERATOR_DIR / "Utilizations.txt"

RAW_RESULTS_DIR = BASE_DIR.parent / "Results" / "Raw"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Run algorithm
EDF.run(TASK_FILE, UTIL_FILE)

EDF_AcceptanceRatio = []
EDF_AcceptanceRatioLo = []
EDF_AcceptanceRatioHi = []
EDF_Utilization = []

# Calculate results
for i in range(101):

    EDF_Utilization.append(i / 100)

    if EDF.AcceptanceRatioArray[0][i] == 0:
        EDF.AcceptanceRatioArray[0][i] = 1

    count = EDF.AcceptanceRatioArray[0][i]

    EDF_AcceptanceRatio.append(
        (EDF.AcceptanceRatioArray[1][i] / count) * 10
    )

    EDF_AcceptanceRatioLo.append(
        (EDF.AcceptanceRatioArray[2][i] / count) * 10
    )

    EDF_AcceptanceRatioHi.append(
        (EDF.AcceptanceRatioArray[3][i] / count) * 10
    )

print("EDF_AcceptanceRatioLo =", EDF_AcceptanceRatioLo)
print("EDF_AcceptanceRatioHi =", EDF_AcceptanceRatioHi)

# Save results
with open(RAW_RESULTS_DIR / "EDFResultLo.txt", "w") as f:
    print(EDF_AcceptanceRatioLo[6:], file=f)

with open(RAW_RESULTS_DIR / "EDFResultHi.txt", "w") as f:
    print(EDF_AcceptanceRatioHi[6:], file=f)

with open(RAW_RESULTS_DIR / "EDFResult.txt", "w") as f:
    print(EDF_AcceptanceRatio[6:], file=f)

print(f"\nResults saved to: {RAW_RESULTS_DIR}")