from bangtal import *

class Animator(Timer):
    def __init__(self, now_scene, seconds=0):
        super().__init__(seconds)
        self.counter=0
        self.schedule=[1 for i in range(3001)]
        self.reservation=[[0] for i in range(3001)]
        self.scene=now_scene

    def onTimeout(self):
        self.scene.setLight(self.schedule[self.counter])
        self.counter+=1
        if self.reservation[self.counter][0]!=0:    
            self.reservation[self.counter][1].start()
        self.set(0.1)
        self.start()

    def light_on(self, start, lenth):
        for i in range(int(lenth*10)):
            if int(start*10)+i==3001:
                break
            self.schedule[int(start*10)+i]=1

    def light_off(self, start, lenth):
        for i in range(int(lenth*10)):
            if int(start*10)+i==3001:
                break
            self.schedule[int(start*10)+i]=0

    def fade_in(self, start,lenth):
        for i in range(int(lenth*10)):
            if int(start*10)+i==3001:
                break
            self.schedule[int(start*10)+i]=i/(lenth*10-1)

    def fade_out(self, start, lenth):
        for i in range(int(lenth*10)):
            if int(start*10)+i==3001:
                break
            self.schedule[int(start*10)+i]=1-(i/(lenth*10-1))

    def reserve(self, start, clk):
        self.reservation[start*10][0]=1
        self.reservation[start*10].append(clk)