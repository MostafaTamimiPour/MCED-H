from math import floor
import numpy as np
import copy

from Common.common import LCM
from Common.common import ShowTasks
from Common.common import MatrixSorter
from Common.common import UtilizationAtFirst
from Common.common import create_ready_queue
from tqdm import tqdm


Pp = 1
storage = 1000
energy_storage = 20
TaskNumber = 10
rununtil = 1000
AcceptanceRatioArray = [ [0] * 101, [0] * 101, [0] * 101, [0] * 101 ]

TaskInfo = 11

TaskCounterForMQPA = 0
ForMQPA = 0




def run(task_file, util_file ):

    with open(task_file, "r") as file, open(util_file, "r") as file1:

        num_lines = sum(1 for _ in file)  # Get the total number of lines in the file for tqdm
        file.seek(0)  # Reset the file pointer back to the beginning
        for line_tasks, line_utilizations in tqdm(zip(file, file1), total=num_lines, desc="Processing files"):
                SchedulableTasks=[]
                utilization = []
                utilization=line_utilizations.strip()
                SchedulableTasks=line_tasks.strip()
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
                        
                U = (Uhh + Ull + Uhl) / 2

                scheduleTasks(SchedulableTasks, 
                            Pp, 
                            rununtil, 
                            storage, 
                            energy_storage, 
                            U, 
                            AcceptanceRatioArray,
                            HiTaskNumbers, 
                            LoTaskNumbers ,
                            TaskCounterForMQPA)



def scheduleTasks(tasks, 
                  Pp, 
                  rununtil, 
                  storage, 
                  energystorage, 
                  U, 
                  AcceptanceRatioArray,
                  TimesSystemGoesInHiMode , 
                  LoTaskNumbers ,
                  TaskCounterForMQPA
                  ):
    



    
    global ForMQPA
    LoTaskSuccess = 0
    HiTaskSuccess = 0
    currentTime = 0

    l=0
    system = 0

    matrix = create_ready_queue(tasks)


    UL = 0
    UH = 0
    UeH = 0
    UeL = 0

    u = UtilizationAtFirst(matrix, UL, UH, UeH, UeL, TaskNumber)
    u.calculate_utilization_At_First()

    UL = u.UL
    UH = u.UH
    UeH = u.UeH
    UeL = u.UeL

    
    MatrixInLoop=0


    Q = MCQPA(matrix, UL, UH, UeH, UeL, TaskNumber , TaskCounterForMQPA)
    Q.calculate_schedulability()
    l = Q.TaskCounterForMQPA    
    ForMQPA =  ForMQPA + l

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

        executingmatrixLo = ExecutingMatrixLo(MatrixInLoop, energystorage,TaskNumber,system, LoTaskSuccess, HiTaskSuccess )

        system=executingmatrixLo.system

        if system == 0:
            executingmatrixLo.Executing_Matrix_Lo()
            energystorage = executingmatrixLo.energystorage
            system = executingmatrixLo.system
            LoTaskSuccess = executingmatrixLo.LoTaskSuccess
            HiTaskSuccess = executingmatrixLo.HiTaskSuccess
        executingmatrixHi = ExecutingMatrixHi(MatrixInLoop, energystorage,TaskNumber, LoTaskSuccess, HiTaskSuccess )

        if system == 1:
            executingmatrixHi.executing_matrix_hi()
            energystorage = executingmatrixHi.energystorage
            LoTaskSuccess = 0
            HiTaskSuccess = executingmatrixHi.HiTaskSuccess
        AcceptanceRatio = LoTaskSuccess + HiTaskSuccess
        AcceptanceRatioArray[1][int(U * 100)] += AcceptanceRatio
        QualityOfLoTasks =  LoTaskSuccess 
        QualityOfHiTasks =  HiTaskSuccess
        AcceptanceRatioArray[3][int(U * 100)] += ( QualityOfHiTasks / ( TimesSystemGoesInHiMode - 1 ) )
        AcceptanceRatioArray[2][int(U * 100)] += ( QualityOfLoTasks / ( LoTaskNumbers  ) )


        # print("***********************************")
        # ShowTasks(MatrixInLoop ,TaskInfo, TaskNumber )
        # print("currentTime ", currentTime)
        # print("energystorage ", energystorage)

        currentTime += 1
        energystorage += Pp

    AcceptanceRatioArray[0][int(U * 100)] += 1



pass




class MCQPA:
    def __init__(self, matrix, UL, UH, UeH, UeL, TaskNumber,TaskCounterForMQPA):
        self.matrix = matrix
        self.UL = UL
        self.UH = UH
        self.UeH = UeH
        self.UeL = UeL
        self.TaskNumber = TaskNumber
        self.TaskCounterForMQPA = TaskCounterForMQPA


    def calculate_schedulability(self):
        b = 0
        t = 0
        x = [0] * self.TaskNumber
        SumOfExecutions = 0

        if (max(self.UL , self.UH)< 1) :
            # Calculate B using
            for i in range (self.TaskNumber):

                SumOfExecutions = SumOfExecutions + max(self.matrix[1][i], self.matrix[4][i])
            rho = round(max(self.UL, self.UH), 3)
            rho = min(max(self.UL, self.UH), 0.999)
            b = ( SumOfExecutions / ( 1 - rho ) )
            b = floor(b)

            # End of Calculate B using

            t = b
            test = 0
            s = [b]

            while t > 0 :

                i = 0
                x = [0] * self.TaskNumber

                # this for calculates landa_i
                for i in range ( self.TaskNumber ) :
                    x[i] = max ( floor( ( t - self.matrix[3][i] ) / self.matrix[6][i] ) + 1 , 0 )
                # end of  calculating landa_i

                s=[]
                s.append(t)
                # calculating S(t)
                for i in range ( self.TaskNumber ):
                    if ( x[i] > 0 ):
                        for j in range ( x[i] ) :
                            test = t - (j * self.matrix[6][i]) - self.matrix[3][i]
                            if (test > 1):
                                s.append(test)
                s=np.sort(s)

                # End of calculating S(t)

                x=0
                y=0
                DeltaMax = 0

                for i in range (len (s)):
                    Delta = 0
                    for j in range (self.TaskNumber):

                        if (self.matrix[7][j] == 0 and self.matrix[3][j] < t):

                            x = max ( floor( ( t - self.matrix[3][j] ) / self.matrix[6][j] ) + 1 , 0 ) * self.matrix[1][j]
                            y =  min ( max ( floor( ( t - self.matrix[3][j] ) / self.matrix[6][j] ) + 1 , 0 ) , floor(s[i]/ self.matrix[6][j]) + 1  ) * (self.matrix[4][j] - self.matrix[1][j])
                            Delta = x + y

                        if (self.matrix[7][j] == 1 and self.matrix[3][j] < t):
                            x = max ( floor( ( t - self.matrix[3][j] ) / self.matrix[6][j] ) + 1 , 0 ) * self.matrix[4][j]
                            y =  max ( floor( ( (t - s[i] ) - self.matrix[3][j] ) / self.matrix[6][j] ) + 1 , 0 )  * (self.matrix[1][j] - self.matrix[4][j])
                            Delta = Delta + x + y



                        if (Delta > t):
                            break
            
                        if (Delta > DeltaMax):
                            DeltaMax = Delta


                if ( DeltaMax == t ):
                    t = t - 1
                else :
                    t = floor(DeltaMax)

                if ( t == 0):
                    self.TaskCounterForMQPA  = self.TaskCounterForMQPA  + 1

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
    def __init__(self, matrix, energystorage, TaskNumber, LoTaskSuccess, HiTaskSuccess):
        self.matrix = matrix
        self.energystorage = energystorage
        self.TaskNumber = TaskNumber
        self.LoTaskSuccess = LoTaskSuccess
        self.HiTaskSuccess = HiTaskSuccess

    def executing_matrix_hi(self):
        q = 0
        j = 0
        e = 0
        K = 0
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



