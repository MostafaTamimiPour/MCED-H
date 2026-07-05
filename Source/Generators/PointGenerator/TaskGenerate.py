
import numpy as np

class Generate () :
    def __init__(self , ULL , UHL , UHH):

        self.Task=[]

        self.ULL=ULL
        self.UHL=UHL
        self.UHH=UHH

        self.TaskNumber = 10
        self.RunUntil = 1000
        self.Pp = 1
        self.storage = 100
        self.energy_storage = 0

        # Define the range of values for each attribute
        self.task_id=0
        self.period=0
        self.execution_time_lo=0
        self.execution_time_hi=0
        self.deadline=0
        self.energy_consumption_lo=0
        self.energy_consumption_hi=0
        self.critlvl=0
        self.task_crit = []


    def make_tasks(self):
        #print("UL=",self.ULL+self.UHL)
        #print("UHH=",self.UHH)

        # Generate a list of Task objects with random attributes
        L=0
        H=0
        tasks = []
        while ( (H<2) or (L<2) ):
            L=0
            H=0
            self.task_crit=[]
            for i in range(self.TaskNumber):
                critlvl =  np.random.random()
                if critlvl >= 0.5:
                    critlvl=1
                else:
                    critlvl=0
                self.task_crit.append(critlvl)
            for i in range(self.TaskNumber):
                if self.task_crit[i]==1:
                    H=H+1
                if self.task_crit[i]==0:
                    L=L+1
            if(self.ULL==0 ):
                self.task_crit=[]
                for i in range(self.TaskNumber):
                    critlvl=1
                    self.task_crit.append(critlvl)
        H=0
        L=0
        for i in range(self.TaskNumber):
            if self.task_crit[i]==1:
                H=H+1
            if self.task_crit[i]==0:
                L=L+1
        # print("UL=",self.ULL)
        # print("H=",H)
        # print("L=",L)


        for i in range(self.TaskNumber):
            if (self.ULL>0):
                if self.task_crit[i] == 0 :
                    period = self.RunUntil
                    # period = np.random.randint(700, self.RunUntil)
                    deadline = period
                    execution_time_hi = int((period*self.ULL)/L)
                    energy_unit = np.random.randint(2, 3)
                    energy_consumption_hi = execution_time_hi * energy_unit
                    execution_time_lo = execution_time_hi 
                    energy_consumption_lo = execution_time_hi * energy_unit
                    taskid = i
                    
                if  self.task_crit[i] == 1 :
                    period = self.RunUntil
                    # period = np.random.randint(700, self.RunUntil)
                    deadline = period
                    execution_time_hi = int((period*self.UHH)/H)
                    execution_time_lo =  int((period*self.UHL)/H)
                    energy_unit = np.random.randint(2, 3)
                    energy_consumption_hi = execution_time_hi * energy_unit
                    taskid = i
                    energy_consumption_lo = execution_time_lo * energy_unit
            if (self.ULL==0):
                period = self.RunUntil
                # period = np.random.randint(700, self.RunUntil)
                deadline = period
                execution_time_hi = int((period*self.UHH)/H)
                execution_time_lo =  int((period*self.UHL)/H)
                energy_unit = np.random.randint(2, 3)
                energy_consumption_hi = execution_time_hi * energy_unit
                taskid = i
                energy_consumption_lo = execution_time_lo * energy_unit
                #print("period=",period)
                #print("self.UHL",self.UHL)
                #print("H=",H)
                #print("execution_time_hi=",execution_time_hi)
                
                
                
            if (execution_time_lo == 0 or energy_consumption_lo == 0 or execution_time_hi == 0 or energy_consumption_hi == 0):
                execution_time_lo = 1 
                energy_consumption_lo = 1 
                execution_time_hi = 1 
                energy_consumption_hi = 1
    
                
            Task=[taskid,period,execution_time_lo,execution_time_hi,deadline,energy_consumption_lo,energy_consumption_hi,self.task_crit[i]]
            tasks.append(Task)


        h=0
        for i in range(self.TaskNumber):
            if tasks[i][7]:
                h=h+1

        UHL=0
        UHH=0
        ULL=0


        for i in range (self.TaskNumber) :

            if(tasks[i][7] == 0):
                ULL = ULL + (tasks[i][2] / tasks[i][1])
            if(tasks[i][7] == 1):
                UHH = UHH +  (tasks[i][3] / tasks[i][1])
                UHL = UHL +  (tasks[i][2] / tasks[i][1])

        # Q = open ('MyTasks.txt','w')
        # if ( ((self.ULL+self.UHL+ self.UHH)/2 == 0.91) ):
        #     print("UL=",self.ULL)
        #     print("H=",H)
        #     print("L=",L)
        #     #f.write(str((self.ULL+self.UHL+ self.UHH)/2))
        #     Q.write('\n')
        #     Q.write(str(tasks))
        #     print("*")
        #     print(tasks)

          
        return tasks

