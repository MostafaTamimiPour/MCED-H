from tqdm import tqdm
import TaskGenerate
from pathlib import Path

# Directory of this script
BASE_DIR = Path(__file__).parent

util_file = BASE_DIR / "Utilizations.txt"
tasks_file = BASE_DIR / "Tasks.txt"

UtilizationArray = []
quality = 50

with open(util_file, "w") as file:
    with open(tasks_file, "w") as file1:
        for i in tqdm(range(1, quality), desc="Processing", unit="iteration", total=quality):
            # for i in range(1,50):

            ULL = i * 1 / quality

            for Q in range(2, quality):
                UHH = Q * 1 / quality

                for P in range(1, Q):
                    UHL = P * 1 / quality

                    if (UHH * 0.6) < UHL < (UHH * 0.8):

                        UL = ULL + UHL
                        U = (UHH + UL) / 2

                        if U <= 1:
                            RepeatPoint = 1
                            SchedulableTasks = []

                            utilization = [ULL, UHL, UHH]

                            tasks = TaskGenerate.Generate(
                                ULL,
                                UHL,
                                UHH
                            )

                            SchedulableTasks = tasks.make_tasks()

                            file.write(str(utilization))
                            file.write("\n")

                            file1.write(str(SchedulableTasks))
                            file1.write("\n")

# Read last generated task set
with open(tasks_file, "r") as file:
    for line in file:
        x = line.strip()

print(x)

print(f"\nTasks saved to: {tasks_file}")
print(f"Utilizations saved to: {util_file}")