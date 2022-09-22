from math import exp
import random

idx = 0
map = []
dire = [(-1, 0), (0, -1), (1, 0), (0, 1)]

for i in range(10):
    tmp = []
    for j in range(10):
        tmp2 = [1, 1, 1, 1]
        tmp.append(tmp2)
    map.append(tmp)


class Ant:
    def __init__(self, Idx):
        self.idx = Idx
        self.X = 0
        self.Y = 0
        self.HP = 5
        self.age = 0
        self.path = []

    def move(self):
        self.age += 1
        prob = [0, 0, 0, 0]
        lastpath = -1 if len(self.path) == 0 else self.path[-1]

        if self.X != 0 and lastpath != 2:
            #prob[0] = (pow(map[self.X][self.Y][0], 3) + 1)/(20-self.X-self.Y)
            prob[0] = max(pow(map[self.X][self.Y][0], 3), 0.001)/1.5
        if self.Y != 0 and lastpath != 3:
            #prob[1] = (pow(map[self.X][self.Y][1], 3) + 1)/(20-self.X-self.Y)
            prob[1] = max(pow(map[self.X][self.Y][1], 3), 0.001)/1.5
        if self.X != 9 and lastpath != 0:
            #prob[2] = (pow(map[self.X][self.Y][2], 3) + 1)/(18-self.X-self.Y)
            prob[2] = max(pow(map[self.X][self.Y][2], 3), 0.001)
        if self.Y != 9 and lastpath != 1:
            #prob[3] = (pow(map[self.X][self.Y][3], 3) + 1)/(18-self.X-self.Y)
            prob[3] = max(pow(map[self.X][self.Y][3], 3), 0.001)

        totprob = prob[0] + prob[1] + prob[2] + prob[3]
        P = random.random()*totprob
        if P < prob[0]:
            map[self.X][self.Y][0] -= 1/self.age
            self.X -= 1
            self.path.append(0)
        elif P < prob[0]+prob[1]:
            map[self.X][self.Y][1] -= 1/self.age
            self.Y -= 1
            self.path.append(1)
        elif P < prob[0]+prob[1]+prob[2]:
            map[self.X][self.Y][2] -= 1/self.age
            self.X += 1
            self.path.append(2)
        else:
            map[self.X][self.Y][3] -= 1/self.age
            self.Y += 1
            self.path.append(3)
        return


Antlst = []
Die = []
Suc = []
Old = []

for i in range(1000):

    if i % 100 == 0:
        Die.append(0)
        Suc.append(0)
        Old.append(0)

    if i % 4 == 0:
        Antlst.append(Ant(i))

    for a in Antlst:
        a.move()
        if a.X == 9 and a.Y == 9:
            a.HP = 0
            Suc[a.idx//100] += 1
            X = 0
            Y = 0
            Len = len(a.path)
            for i in a.path:
                map[X][Y][i] += 50/Len
                X += dire[i][0]
                Y += dire[i][1]
                continue
        # new tower built at round 300
        if (1 <= a.X <= 4 and 6 <= a.Y <= 9) or (300 < i <= 1000 and 6 <= a.X <= 9 and 4 <= a.Y <= 7) or (600 < i <= 1000 and 4 <= a.X <= 7 and 0 <= a.Y <= 3):
            a.HP -= 1
            if a.HP <= 0:
                Die[a.idx//100] += 1
                X = 0
                Y = 0
                Len = len(a.path)
                for i in a.path:
                    map[X][Y][i] -= 20/Len
                    X += dire[i][0]
                    Y += dire[i][1]
                continue

        if a.age > 50 and a.HP > 0:
            a.HP = 0
            Old[a.idx//100] += 1
            X = 0
            Y = 0
            Len = len(a.path)
            for i in a.path:
                map[X][Y][i] -= 20/Len
                X += dire[i][0]
                Y += dire[i][1]
            continue

    for idx in range(len(Antlst)-1, -1, -1):
        if Antlst[idx].HP <= 0:
            Antlst.pop(idx)

    for l in range(10):
        for j in range(10):
            for k in range(4):
                map[l][j][k] *= 0.9

print("Die:    ", Die)
print("Succeed:", Suc)
print("Old:    ", Old)
