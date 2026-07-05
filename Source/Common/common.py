def ShowTasks(matrix, TaskInfo, TaskNumber):
    for i in range(TaskInfo):
        for j in range(TaskNumber):
            print(matrix[i][j], end="\t")
        if i == 0:
            print("AbsoluteDeadline\t")
        elif i == 1:
            print("executionTimeHi\t")
        elif i == 2:
            print("energyConsumptionHi\t")
        elif i == 3:
            print("ImplictDeadline\t")
        elif i == 4:
            print("executionTimeLo\t")
        elif i == 5:
            print("energyConsumptionLo\t")
        elif i == 6:
            print("Period\t")
        elif i == 7:
            print("CritLvl\t")
        elif i == 8:
            print("id\t")
        elif i == 9:
            print("PermissionToRun\t")
        elif i == 10:
            print("TaskCount\t")

def LCM(a, b):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    return abs(a * b) // gcd(a, b)

class MatrixSorter:

    def __init__(self, matrix, system):
        self.matrix = matrix
        self.system = system

    def sort_matrix(self):
        if self.system == 0:
            indices = list(range(len(self.matrix[3])))
            indices.sort(key=lambda i: self.matrix[3][i])
            for i in range(len(self.matrix)):
                temp_row = [self.matrix[i][j] for j in indices]
                self.matrix[i] = temp_row
        elif self.system == 1:
            indices = list(range(len(self.matrix[0])))
            indices.sort(key=lambda i: self.matrix[0][i])
            for i in range(len(self.matrix)):
                temp_row = [self.matrix[i][j] for j in indices]
                self.matrix[i] = temp_row
        #print("print in sorter")



class UtilizationAtFirst:
    def __init__(self, matrix, UL, UH, UeH, UeL, TaskNumber):
        self.matrix = matrix
        self.UL = UL
        self.UH = UH
        self.UeH = UeH
        self.UeL = UeL
        self.TaskNumber = TaskNumber

    def calculate_utilization_At_First(self):
        for i in range(self.TaskNumber):

            self.UL = self.UL + (float(self.matrix[4][i]) / float(self.matrix[3][i]))
            if self.matrix[7][i] == 1:
                self.UH = self.UH + (float(self.matrix[1][i]) / float(self.matrix[0][i]))
            self.UeL = self.UeL + (self.matrix[5][i] / self.matrix[3][i])
            if self.matrix[7][i] == 1:
                self.UeH = self.UeH + (1.0 * self.matrix[2][i] / self.matrix[0][i])


def create_ready_queue(tasks):
    """
    Build the scheduler ready queue (matrix) from the task list.
    """

    AbsoluteDeadline = []
    ImplictDeadline = []
    executionTimeLo = []
    executionTimeHi = []
    energyconsumptionLo = []
    energyconsumptionHi = []
    taskid = []
    period = []
    critlvl = []
    PermissionToRun = []
    taskcount = []

    for task in tasks:
        taskid.append(task[0])
        period.append(task[1])

        AbsoluteDeadline.append(task[1])
        ImplictDeadline.append(task[1])

        executionTimeLo.append(task[2])
        executionTimeHi.append(task[3])

        energyconsumptionLo.append(task[5])
        energyconsumptionHi.append(task[6])

        critlvl.append(task[7])
        PermissionToRun.append(task[7])

        taskcount.append(0)

    matrix = [
        AbsoluteDeadline,
        executionTimeHi,
        energyconsumptionHi,
        ImplictDeadline,
        executionTimeLo,
        energyconsumptionLo,
        period,
        critlvl,
        taskid,
        PermissionToRun,
        taskcount
    ]

    return matrix