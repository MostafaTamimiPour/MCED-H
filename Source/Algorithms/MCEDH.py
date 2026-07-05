from Common.common import LCM
from Common.common import ShowTasks
from Common.common import MatrixSorter
from Common.slack import Slackenergy
from Common.slack import SlackTime
from Common.common import create_ready_queue
from tqdm import tqdm
import numpy as np
import copy


TaskInfo = 11
Pp = 20
storage = 1000
energy_storage = 20
TaskNumber = 10
rununtil = 1000
AcceptanceRatioArray = [ [0] * 101, [0] * 101, [0] * 101, [0] * 101 ]

tasks=[] 
UtilizationArray = []


def run(task_file, util_file):

    with open(task_file, "r") as file, open(util_file, "r") as file1:

        num_lines = sum(1 for _ in file)  # Get the total number of lines in the file for tqdm
        file.seek(0)  # Reset the file pointer back to the beginning
        for line_tasks, line_utilizations in tqdm(zip(file, file1), total=num_lines, desc="Processing files"):
                
                utilization = []
                utilization=line_utilizations.strip()
                SchedulableTasks=line_tasks.strip()
                SchedulableTasks=eval(SchedulableTasks)
                utilization = eval(utilization)
                Ull = utilization[0]
                Uhl = utilization[1]
                Uhh = utilization[2]
                U = float( ( Ull + Uhl + Uhh ) / 2 )

                HiTaskNumbers = 1
                LoTaskNumbers = 0

                for i in range (len(SchedulableTasks)):
                    if (SchedulableTasks[i][7]==1):
                        HiTaskNumbers+=1
                for i in range (len(SchedulableTasks)):
                    if (SchedulableTasks[i][7]==0):
                        LoTaskNumbers+=1
                        
                scheduleTasks(SchedulableTasks, 
                            TaskNumber, 
                            Pp, 
                            rununtil, 
                            storage, 
                            energy_storage, 
                            AcceptanceRatioArray,
                            U,
                            HiTaskNumbers, 
                            LoTaskNumbers)


def scheduleTasks(tasks, 
                  tasknumber, 
                  Pp, 
                  rununtil, 
                  storage, 
                  energystorage, 
                  AcceptanceRatioArray,
                  U , 
                  TimesSystemGoesInHiMode , 
                  LoTaskNumbers):
    

    currentTime = 0
    Ideadline = 0
    PermisionChecker = 0
    system = 0


    matrix = create_ready_queue(tasks)


    UL =0
    ULL =0
    UHL=0 
    UHH =0
    UH =0
    Uell = 0 
    Uehl = 0
    Uehh = 0

    for i in range(TaskNumber):

        UL = UL + (float(matrix[4][i]) / float(matrix[3][i]))
        if matrix[7][i] == 0:

            ULL = ULL + (float(matrix[4][i]) / float(matrix[0][i]))
        if matrix[7][i] == 1:

            UH = UH + (float(matrix[1][i]) / float(matrix[0][i]))
            UHH = UHH + (float(matrix[1][i]) / float(matrix[0][i]))
            UHL = UHL + (float(matrix[4][i]) / float(matrix[0][i]))



    for i in range (tasknumber):
        
        if ( matrix[7][i] == 0):
            Uell = Uell + float(matrix[2][i] / matrix[0][i])

        if ( matrix[7][i] == 1):
            Uehl = Uehl + float(matrix[5][i] / matrix[0][i])
            Uehh = Uehh + float(matrix[2][i] / matrix[0][i])


    MyCase = ULL + (1/(1-(UHH-UHL)))
    if( MyCase <=1):
        for i in range(TaskNumber):
            if( matrix[7][i] == 1):
                result = ImplicitDeadline(matrix, Pp, i, Ideadline, ULL , UHL , UHH )
                result.implicitDeadline(matrix, Pp, i, Ideadline, ULL , UHL , UHH)
                matrix[3][i] = int(result.Ideadline*matrix[3][i])
    

    TasksInLoop=tasks

    MatrixInLoop=copy.deepcopy(matrix)

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
        executingmatrixLo = ExecutingMatrixLo(MatrixInLoop, currentTime, TasksInLoop, energystorage, storage,
                                    TaskNumber, TaskInfo, Pp, system, LoTaskSuccess, HiTaskSuccess )

        system = executingmatrixLo.system
        if system == 0:
            executingmatrixLo.Executing_Matrix_Lo()
            energystorage = executingmatrixLo.energystorage
            system = executingmatrixLo.system
            LoTaskSuccess = executingmatrixLo.LoTaskSuccess
            HiTaskSuccess = executingmatrixLo.HiTaskSuccess
            MatrixInLoop = executingmatrixLo.matrix
        
        executingmatrixHi = ExecutingMatrixHi(MatrixInLoop, currentTime, TasksInLoop, energystorage, storage,
                        TaskNumber, TaskInfo, Pp, system, LoTaskSuccess,
                        HiTaskSuccess, PermisionChecker )


        if system == 1:
            executingmatrixHi.executing_matrix_hi()
            energystorage = executingmatrixHi.energystorage
            LoTaskSuccess = executingmatrixHi.LoTaskSuccess
            HiTaskSuccess = executingmatrixHi.HiTaskSuccess
            PermisionChecker = executingmatrixHi.PermisionChecker
            MatrixInLoop = executingmatrixHi.matrix
            
        AcceptanceRatio = LoTaskSuccess + HiTaskSuccess
        AcceptanceRatioArray[1][round(U * 100)] += AcceptanceRatio
        
        QualityOfLoTasks =  LoTaskSuccess 
        QualityOfHiTasks =  HiTaskSuccess
        AcceptanceRatioArray[3][round(U * 100)] += ( QualityOfHiTasks / ( TimesSystemGoesInHiMode - 1 ) )
        AcceptanceRatioArray[2][round(U * 100)] += ( QualityOfLoTasks / ( LoTaskNumbers  ) )

        # print("***********************************")
        # ShowTasks(MatrixInLoop ,TaskInfo, TaskNumber )
        # print("currentTime ", currentTime)
        # print("energystorage ", energystorage)

        currentTime += 1
        energystorage += Pp
        
    AcceptanceRatioArray[0][round(U * 100)] += 1
    AcceptanceRatioArray[3][round(U * 100)] = round(AcceptanceRatioArray[3][round(U * 100)])
    AcceptanceRatioArray[2][round(U * 100)] = round(AcceptanceRatioArray[2][round(U * 100)])

pass




class PermissionToRunAcceptLoTask:
    def __init__(self, matrix, currentTime, TaskNumber, TaskInfo, energystorage, storage, Pp, tasks, system , PermisionChecker):
        self.matrix = matrix
        self.currentTime = currentTime
        self.tasks = tasks
        self.energystorage = energystorage
        self.storage = storage
        self.TaskNumber = TaskNumber
        self.TaskInfo = TaskInfo
        self.Pp = Pp
        self.system = system
        self.PermisionChecker = PermisionChecker

    def Permission_To_Run_Accept_Lo_Task(self):
        emax=0
        slack=0
        PSe = 0

        for k in range (self.TaskNumber):
            if ( self.matrix[9][k]==0 and self.matrix[10][k] == 0 ):

                self.matrix[9][k] = 1 

                slacktime = SlackTime(self.matrix, self.currentTime, self.TaskNumber, self.TaskInfo, slack,
                            self.tasks, self.system, self.Pp)
                slacktime.calculate_slack_time()
                slack = slacktime.slack

                slackenergy = Slackenergy(self.matrix, self.currentTime, self.TaskNumber, self.TaskInfo, self.energystorage,
                                        self.storage, self.Pp, emax, PSe, self.tasks, self.system)
                slackenergy.calculate_slack_energy()
                PSe = slackenergy.PSE

                if(slack < 0 or PSe < 0 ):
                    self.matrix[9][k] = 0
                    self.matrix[10][k] = 1
                    self.PermisionChecker = 1
                    break

                            


class ImplicitDeadline:
    def __init__(self, matrix, Pp, i, Ideadline , ULL , UHL , UHH ):
        self.matrix = matrix
        self.Pp = Pp
        self.i = i
        self.Ideadline = Ideadline
        self.ULL=ULL
        self.UHL=UHL
        self.UHH= UHH

    def implicitDeadline(self):

        if self.matrix[7][self.i] == 1:
            self.Ideadline = self.ULL + (self.UHL/(self.Pp-(self.UHH-self.UHL)))
            self.Ideadline = self.Ideadline/self.Pp


class ExecutingMatrixLo:
    def __init__(self, matrix, currentTime, tasks, energystorage, storage, TaskNumber,
                 TaskInfo, Pp, system, LoTaskSuccess, HiTaskSuccess):
        self.matrix = matrix
        self.currentTime = currentTime
        self.tasks = tasks
        self.energystorage = energystorage
        self.storage = storage
        self.TaskNumber = TaskNumber
        self.TaskInfo = TaskInfo
        self.Pp = Pp
        self.system = system
        self.LoTaskSuccess = LoTaskSuccess
        self.HiTaskSuccess = HiTaskSuccess

    def Executing_Matrix_Lo(self):
        q = 0
        j = 0
        e = 0
        emax = 0
        PSe = 0
        slack = 0


        slacktime = SlackTime(self.matrix, self.currentTime, self.TaskNumber, self.TaskInfo, slack,
                              self.tasks, self.system, self.Pp)
        slacktime.calculate_slack_time()
        slack = slacktime.slack

        slackenergy = Slackenergy(self.matrix, self.currentTime, self.TaskNumber, self.TaskInfo, self.energystorage,
                                  self.storage, self.Pp, emax, PSe, self.tasks, self.system)
        slackenergy.calculate_slack_energy()
        PSe = slackenergy.PSE

        k = 0
        # for checking if we cant run all task in LO mode it goes in Hi mode
        if (slack < 0 or PSe < 0):
            self.system = 1

        while q == 0 and j < self.TaskNumber and self.system == 0:

            if self.matrix[4][j] > 0:

                e = self.matrix[5][j] / self.matrix[4][j]
                f = self.energystorage - e

                if f < 0 or emax > self.energystorage:
                    if slack != 0 or self.energystorage == self.storage:
                        break
                self.matrix[4][j] = self.matrix[4][j] - 1
                self.matrix[5][j] = self.matrix[5][j] - e
                self.energystorage = self.energystorage - e
                q += 1
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
            k += 1

class ExecutingMatrixHi:
    def __init__(self, matrix, currentTime, tasks, energystorage, storage, TaskNumber,
                 TaskInfo, Pp, system, LoTaskSuccess, HiTaskSuccess,PermisionChecker):
        self.matrix = matrix
        self.currentTime = currentTime
        self.tasks = tasks
        self.energystorage = energystorage
        self.storage = storage
        self.TaskNumber = TaskNumber
        self.TaskInfo = TaskInfo
        self.Pp = Pp
        self.system = system
        self.LoTaskSuccess = LoTaskSuccess
        self.HiTaskSuccess = HiTaskSuccess
        self.PermisionChecker = PermisionChecker

    def executing_matrix_hi(self):
        q = 0
        j = 0
        e = 0
        emax = 0
        slack = 0

        if ( self.PermisionChecker == 0 ) :

            Permission_To_Run_Acceppted = PermissionToRunAcceptLoTask(self.matrix, self.currentTime, self.TaskNumber,
                                                    self.TaskInfo, self.energystorage,
                                                    self.storage, self.Pp, self.tasks, self.system , self.PermisionChecker)

            Permission_To_Run_Acceppted.Permission_To_Run_Accept_Lo_Task()
            self.matrix = Permission_To_Run_Acceppted.matrix
            self.PermisionChecker = Permission_To_Run_Acceppted.PermisionChecker

        K = 0

        while q == 0 and j < self.TaskNumber:
            if self.matrix[1][j] > 0:
                if (self.matrix[9][j] == 1 or self.matrix[7][j] == 1 ) :

                    e = self.matrix[2][j] / self.matrix[1][j]
                    f = self.energystorage - e

                    slacktime = SlackTime(self.matrix, self.currentTime, self.TaskNumber, self.TaskInfo, slack,
                                          self.tasks, self.system, self.Pp)
                    slacktime.calculate_slack_time()
                    slack = slacktime.slack



                    if slack > 0:
                        if f < 0 or emax > self.energystorage:
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



