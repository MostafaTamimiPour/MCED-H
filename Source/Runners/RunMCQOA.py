from pathlib import Path
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from Algorithms import MCQPA

# Directories
POINT_GENERATOR_DIR = BASE_DIR.parent / "Generators" / "PointGenerator"

TASK_FILE = POINT_GENERATOR_DIR / "Tasks.txt"
UTIL_FILE = POINT_GENERATOR_DIR / "Utilizations.txt"

RAW_RESULTS_DIR = BASE_DIR.parent / "Results" / "Raw"
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Run algorithm
MCQPA.run(TASK_FILE, UTIL_FILE)

MCQPA_AcceptanceRatio = []
MCQPA_AcceptanceRatioLo = []
MCQPA_AcceptanceRatioHi = []
MCQPA_Utilization = []

# Calculate results
for i in range(101):

    MCQPA_Utilization.append(i / 100)

    if MCQPA.AcceptanceRatioArray[0][i] == 0:
        MCQPA.AcceptanceRatioArray[0][i] = 1

    count = MCQPA.AcceptanceRatioArray[0][i]

    MCQPA_AcceptanceRatio.append(
        (MCQPA.AcceptanceRatioArray[1][i] / count) * 10
    )

    MCQPA_AcceptanceRatioLo.append(
        (MCQPA.AcceptanceRatioArray[2][i] / count) * 10
    )

    MCQPA_AcceptanceRatioHi.append(
        (MCQPA.AcceptanceRatioArray[3][i] / count) * 10
    )

print("MCQPA_AcceptanceRatioLo =", MCQPA_AcceptanceRatioLo)
print("MCQPA_AcceptanceRatioHi =", MCQPA_AcceptanceRatioHi)

# Save results
with open(RAW_RESULTS_DIR / "MCQPAResultLo.txt", "w") as f:
    print(MCQPA_AcceptanceRatioLo[6:], file=f)

with open(RAW_RESULTS_DIR / "MCQPAResultHi.txt", "w") as f:
    print(MCQPA_AcceptanceRatioHi[6:], file=f)

with open(RAW_RESULTS_DIR / "MCQPAResult.txt", "w") as f:
    print(MCQPA_AcceptanceRatio[6:], file=f)

print(f"\nResults saved to: {RAW_RESULTS_DIR}")