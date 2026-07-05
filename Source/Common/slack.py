class SlackTime:
    def __init__(self, matrix, currentTime, TaskNumber, TaskInfo, slack, tasks, system, Pp):
        self.matrix = matrix
        self.currentTime = currentTime
        self.TaskNumber = TaskNumber
        self.TaskInfo = TaskInfo
        self.slack = slack
        self.tasks = tasks
        self.system = system
        self.Pp = Pp

    def calculate_slack_time(self):
        temp = 10000
        At = 0
        self.slack = 10000
        maxdeadline = 0
        if self.system == 0:
            for i in range(self.TaskNumber):
                if self.matrix[4][i] > 0 and maxdeadline < self.matrix[3][i]:
                    maxdeadline = self.matrix[3][i]

            for i in range(self.TaskNumber):
                if maxdeadline == 0:
                    break
                At = 0
                for j in range(i + 1):
                    Ideadline = 0
                    deadline = self.matrix[3][j]
                    if deadline <= self.matrix[3][i]:
                        At = self.matrix[4][j] + At
                    if i == j and self.matrix[1][j] != 0:
                        if At > 0:
                            temp = self.matrix[3][j] - self.currentTime - At
                        if self.slack > temp:
                            self.slack = temp
                    if self.matrix[4][i] == 0 and self.matrix[1][i] != 0:
                        if i + 1 > self.TaskNumber - 1:
                            self.matrix[3][i] = maxdeadline

                            temp = deadline - (deadline - self.matrix[3][j]) - At
                        if self.slack > temp:
                            self.slack = temp

        if self.system == 1:
            for i in range(self.TaskNumber):
                if maxdeadline < self.matrix[0][i] and self.matrix[9][i] == 1 :
                    maxdeadline = self.matrix[0][i]
            for i in range(self.TaskNumber):
                if maxdeadline == 0:
                    break
                At = 0
                for j in range(i + 1):
                    if self.matrix[0][i] >= self.matrix[0][j] and (self.matrix[9][j]==1):
                        At = self.matrix[1][j] + At

                if i == j and self.matrix[0][i] >= self.currentTime and (self.matrix[9][j]==1) :
                    temp = self.matrix[0][i] - self.currentTime - At


                if self.slack > temp:
                    self.slack = temp


class Slackenergy:
    def __init__(self, matrix, currentTime, TaskNumber, TaskInfo, energystorage, storage, Pp, emax, PSE, tasks, system):
        self.matrix = matrix
        self.currentTime = currentTime
        self.TaskNumber = TaskNumber
        self.TaskInfo = TaskInfo
        self.energystorage = energystorage
        self.storage = storage
        self.Pp = Pp
        self.emax = emax
        self.PSE = PSE
        self.tasks = tasks
        self.system = system

    def calculate_slack_energy(self):
        maxdeadline = 0
        temp = 10000
        AT = 0
        slackenergy = 10000
        e = 0

        if self.system == 0:
            for i in range(self.TaskNumber):
                if self.matrix[4][i] > 0 and maxdeadline < self.matrix[3][i]:
                    maxdeadline = self.matrix[3][i]

            for i in range(self.TaskNumber):
                if maxdeadline == 0:
                    break
                AT = 0

                for j in range(i + 1):
                    Ideadline = 0
                    deadline = self.matrix[3][j]


                    if deadline <= self.matrix[3][i]:
                        AT = self.matrix[5][j] + AT


                    if i == j and self.matrix[1][j] != 0:
                        if AT > 0:
                            temp = self.energystorage + ((self.matrix[3][j] - self.currentTime) * self.Pp) - AT

                        if slackenergy > temp:
                            slackenergy = temp

                    if self.matrix[4][i] == 0 and self.matrix[1][i] != 0:
                        deadline = deadline + self.matrix[6][j]

                        if i + 1 > self.TaskNumber - 1:
                            maxdeadline = self.matrix[3][i]

                        if deadline <= maxdeadline:
                            deadline = deadline + self.matrix[6][j]

                        if slackenergy > temp:
                            slackenergy = temp

        if self.system == 1:

            for i in range(self.TaskNumber):
                if self.matrix[1][i] > 0 and maxdeadline < self.matrix[0][i] and self.matrix[9][i] == 1:
                    maxdeadline = self.matrix[0][i]

            for i in range(self.TaskNumber):
                if maxdeadline == 0:
                    #print("NO task")
                    break

                At = 0
                for j in range(i + 1):
                    if self.matrix[0][i] >= self.matrix[0][j] and ( self.matrix[9][j]==1):
                        At = self.matrix[2][j] + At
                if i == j and self.matrix[0][i] >= self.currentTime:
                    temp = self.energystorage + ((self.matrix[0][i] - self.currentTime) * self.Pp) - At

                if slackenergy > temp:
                    slackenergy = temp

        self.PSE = slackenergy

