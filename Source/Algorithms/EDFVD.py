import numpy as np
import copy
from tqdm import tqdm

from Common.common import ShowTasks
from Common.common import MatrixSorter
from Common.common import create_ready_queue


Pp = 1
storage = 1000
energy_storage = 20
TaskNumber = 10
rununtil = 1000
AcceptanceRatioArray = [ [0] * 101, [0] * 101, [0] * 101, [0] * 101 ]
currentTime_array = []
Complete_Task_array = []
TaskInfo = 11
Taskcounter = 0
ConfirmedByEDFVD = 0


x = 0
hyperperiod = 1
system = 0

tasks=[]
k=0  
UtilizationArray = []
RepeatPoint = 0


def run(task_file, util_file):


    with open(task_file, "r") as file, open(util_file, "r") as file1:

        num_lines = sum(1 for _ in file)  # Get the total number of lines in the file for tqdm
        file.seek(0)  # Reset the file pointer back to the beginning
        for line_tasks, line_utilizations in tqdm(zip(file, file1), total=num_lines, desc="Processing files"):
                utilization = []
                Taskcounter = 0
                SchedulableTasks=[]
                utilization = []
                utilization=line_utilizations.strip()
                SchedulableTasks=line_tasks.strip()

                Taskcounter = Taskcounter + 1
                HiTaskNumbers = 1
                LoTaskNumbers = 0
                SchedulableTasks=eval(SchedulableTasks)
                utilization = eval(utilization)
                Ull = utilization[0]
                Uhl = utilization[1]
                Uhh = utilization[2]

                for i in range (len(SchedulableTasks)):
                    if (SchedulableTasks[i][7]==1):
                        HiTaskNumbers+=1
                for i in range (len(SchedulableTasks)):
                    if (SchedulableTasks[i][7]==0):
                        LoTaskNumbers+=1

                scheduleTasks(SchedulableTasks, 
                            TaskNumber, 
                            TaskInfo, 
                            Pp, 
                            rununtil, 
                            storage, 
                            energy_storage, 
                            system , 
                            AcceptanceRatioArray ,
                            HiTaskNumbers, 
                            LoTaskNumbers,
                            Ull,
                            Uhl,
                            Uhh)



def scheduleTasks(tasks, 
                  tasknumber, 
                  taskinfo, 
                  Pp, 
                  rununtil, 
                  storage, 
                  energystorage, 
                  System, 
                  AcceptanceRatioArray,
                  TimesSystemGoesInHiMode , 
                  LoTaskNumbers,
                  Ull,
                  Uhl,
                  Uhh ):
    
    global ConfirmedByEDFVD
    LoTaskSuccess = 0
    HiTaskSuccess = 0
    currentTime = 0
    Ideadline = 0

    system = System


    u = float( ( Ull + Uhl + Uhh ) / 2 )

    matrix = create_ready_queue(tasks)


    case1 = (Ull + Uhh )
    case2 = Ull + ( Uhl / ( 1 - Uhh ) ) 

    if( case2 <=1 and case1 > 1 ):
        ConfirmedByEDFVD = ConfirmedByEDFVD + 1
        for i in range(TaskNumber):
            if( matrix[7][i] == 1):
                result = ImplicitDeadline(matrix, currentTime, tasknumber, taskinfo, tasks, Pp, i, Ideadline, Ull , Uhl , Uhh )
                result.implicitDeadline()
                matrix[3][i] = int(result.Ideadline*matrix[3][i])
                

    MatrixInLoop=0

    MatrixInLoop=copy.deepcopy(matrix)
    system = 0

    sorter = MatrixSorter(MatrixInLoop, system)
    sorter.sort_matrix()
    for i in range(TaskInfo):
        for j in range(TaskNumber):
            MatrixInLoop[i][j] = sorter.matrix[i][j]
    for i in range(rununtil + 1):

        if energystorage > storage:
            energystorage = storage

        LoTaskSuccess=0
        HiTaskSuccess=0
        QualityOfLoTasks = 0
        QualityOfHiTasks = 0  

        executingmatrixLo = ExecutingMatrixLo(MatrixInLoop, energystorage,TaskNumber, system, LoTaskSuccess,HiTaskSuccess )
    
        system=executingmatrixLo.system

        if system == 0:
            
            executingmatrixLo.Executing_Matrix_Lo()
            energystorage = executingmatrixLo.energystorage
            system = executingmatrixLo.system
            LoTaskSuccess = executingmatrixLo.LoTaskSuccess
            HiTaskSuccess = executingmatrixLo.HiTaskSuccess
        
        executingmatrixHi = ExecutingMatrixHi(MatrixInLoop, energystorage, TaskNumber, system, LoTaskSuccess,HiTaskSuccess )

        if system == 1:
            
            executingmatrixHi.executing_matrix_hi()
            energystorage = executingmatrixHi.energystorage
            LoTaskSuccess = 0
            HiTaskSuccess = executingmatrixHi.HiTaskSuccess
            
        AcceptanceRatio = LoTaskSuccess + HiTaskSuccess
        AcceptanceRatioArray[1][round(u * 100)] += AcceptanceRatio
        
        QualityOfLoTasks =  LoTaskSuccess 
        QualityOfHiTasks =  HiTaskSuccess
        AcceptanceRatioArray[3][round(u * 100)] += ( QualityOfHiTasks / ( TimesSystemGoesInHiMode - 1 ) )
        AcceptanceRatioArray[2][round(u * 100)] += ( QualityOfLoTasks / ( LoTaskNumbers  ) )

        # print("***********************************")
        # ShowTasks(MatrixInLoop ,TaskInfo, TaskNumber )
        # print("currentTime ", currentTime)
        # print("energystorage ", energystorage)

        currentTime += 1
        energystorage += Pp

    AcceptanceRatioArray[0][round(u * 100)] += 1



    pass




class ImplicitDeadline:
    def __init__(self, matrix, currentTime, tasknumber, taskinfo, tasks, Pp, i, Ideadline , ULL , UHL , UHH ):
        self.matrix = matrix
        self.currentTime = currentTime
        self.tasknumber = tasknumber
        self.taskinfo = taskinfo
        self.tasks = tasks
        self.Pp = Pp
        self.i = i
        self.Ideadline = Ideadline
        self.ULL=ULL
        self.UHL=UHL
        self.UHH= UHH

    def implicitDeadline(self):
        if self.matrix[7][self.i] == 1:
            self.Ideadline = ( self.UHL / ( 1 - self.ULL ) )


class ExecutingMatrixLo:
    def __init__(self, matrix, energystorage, TaskNumber, system, LoTaskSuccess, HiTaskSuccess):
        
        self.matrix = matrix
        self.energystorage = energystorage
        self.TaskNumber = TaskNumber
        self.system = system
        self.LoTaskSuccess = LoTaskSuccess
        self.HiTaskSuccess = HiTaskSuccess

    def Executing_Matrix_Lo(self):
        Q = 0
        j = 0
        e = 0
        K = 0


        while Q == 0 and j < self.TaskNumber and self.system == 0:

            if self.matrix[4][j] > 0:
                
                    e = self.matrix[5][j] / self.matrix[4][j]
                    f = self.energystorage - e

                    if f < 0 :
                        break
                    self.matrix[4][j] = self.matrix[4][j] - 1
                    self.matrix[5][j] = self.matrix[5][j] - e
                    self.energystorage = self.energystorage - e
                    Q += 1
                    self.matrix[1][j] = self.matrix[1][j] - 1
                    self.matrix[2][j] = self.matrix[2][j] - e
                    if self.matrix[4][j] == 0 and self.system == 0:

                        if (self.matrix[10][j] == 0 and self.matrix[7][j] == 0 ):
                            self.LoTaskSuccess = self.LoTaskSuccess + 1
                            self.matrix[10][j] = self.matrix[10][j] + 1

                        if (self.matrix[10][j] == 0 and self.matrix[7][j] == 1 ):
                            critLvlMesure =  np.random.random()
                            if critLvlMesure < 0.05:
                                self.system=1
                            else:
                                self.system=0
                            if (self.system == 0 and self.matrix[7][j] == 1 ):
                                self.matrix[1][j] = 0
                                self.matrix[2][j] = 0
                                if (self.matrix[10][j] == 0):
                                    self.HiTaskSuccess = self.HiTaskSuccess + 1

                                    self.matrix[10][j] = self.matrix[10][j] + 1
            if self.matrix[4][j] <= 0:
                j += 1
            K += 1

class ExecutingMatrixHi:
    def __init__(self, matrix, energystorage, TaskNumber, system,  LoTaskSuccess, HiTaskSuccess, ):
        
        self.matrix = matrix
        self.energystorage = energystorage
        self.TaskNumber = TaskNumber
        self.system = system
        self.LoTaskSuccess = LoTaskSuccess
        self.HiTaskSuccess = HiTaskSuccess

    def executing_matrix_hi(self):
        q = 0
        j = 0
        e = 0
        K = 0
        p = 0


        while q == 0 and j < self.TaskNumber:

            if self.matrix[1][j] > 0:
                if (self.matrix[9][j] == 1 or self.matrix[7][j] == 1 ) :

                    e = self.matrix[2][j] / self.matrix[1][j]
                    f = self.energystorage - e
                    if f < 0 :
                            break

                    self.matrix[1][j] = self.matrix[1][j] - 1
                    self.matrix[2][j] = self.matrix[2][j] - e
                    self.energystorage = self.energystorage - e
                    q += 1
                    if (self.matrix[1][j] == 0):
                        if (self.matrix[7][j] == 1):
                            if (self.matrix[10][j] == 0 ):

                                self.HiTaskSuccess = self.HiTaskSuccess + 1
                                self.matrix[10][j] = self.matrix[10][j] + 1

                        if (self.matrix[7][j] == 0):
                            if (self.matrix[9][j] == 1):
                                if (self.matrix[10][j] == 0 ):
                                    self.LoTaskSuccess = self.LoTaskSuccess + 1
                                    self.matrix[10][j] = self.matrix[10][j] + 1
            if self.matrix[1][j] <= 0 or self.matrix[9][j] == 0 :
                j += 1
            K += 1




