from bangtal import *
import keyboard as kb
from animator import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

###________________________________________________________________________________________인트로
intro=Scene("인트로", "")

title=["인트로/선과함께.png", "인트로/원작.png", "인트로/짤툰.png", "인트로/메이플.png"]
title_count=0
intro_title=Object(title[title_count])
intro_title.locate(intro, 440, 350)
intro_title.show()

title_clk=Timer(0)
def title_change():
    global title_count
    title_count+=1
    if title_count<4:
        intro_title.setImage(title[title_count])
        intro_title.show()
    else:
        hellgate.enter()
title_clk.onTimeout=title_change

intro_animator=Animator(intro)
intro_animator.fade_out(1, 2)
intro_animator.reserve(3, title_clk)
intro_animator.fade_out(4, 2)
intro_animator.reserve(6, title_clk)
intro_animator.fade_out(7, 2)
intro_animator.reserve(9, title_clk)
intro_animator.fade_out(10, 2)
intro_animator.reserve(12, title_clk)

def intro_onEnter():
    intro_animator.start()
intro.onEnter=intro_onEnter

def intro_onLeave():
    intro_animator.stop()
intro.onLeave=intro_onLeave
###________________________________________________________________________________________/인트로

leading_roll_file_set=[[[["캐릭터/주연/정지/디폴트/좌/stand1_0.png", "캐릭터/주연/정지/디폴트/좌/stand1_1.png", "캐릭터/주연/정지/디폴트/좌/stand1_2.png", "캐릭터/주연/정지/디폴트/좌/stand1_3.png"],["캐릭터/주연/정지/디폴트/우/stand1_0.png", "캐릭터/주연/정지/디폴트/우/stand1_1.png", "캐릭터/주연/정지/디폴트/우/stand1_2.png", "캐릭터/주연/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/주연/이동/디폴트/좌/walk1_0.png","캐릭터/주연/이동/디폴트/좌/walk1_1.png","캐릭터/주연/이동/디폴트/좌/walk1_2.png","캐릭터/주연/이동/디폴트/좌/walk1_3.png","캐릭터/주연/이동/디폴트/좌/walk1_4.png"],["캐릭터/주연/이동/디폴트/우/walk1_0.png","캐릭터/주연/이동/디폴트/우/walk1_1.png","캐릭터/주연/이동/디폴트/우/walk1_2.png","캐릭터/주연/이동/디폴트/우/walk1_3.png","캐릭터/주연/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/주연/위/디폴트/좌/rope_0.png","캐릭터/주연/위/디폴트/좌/rope_1.png","캐릭터/주연/위/디폴트/좌/rope_2.png"],["캐릭터/주연/위/디폴트/우/rope_0.png","캐릭터/주연/위/디폴트/우/rope_1.png","캐릭터/주연/위/디폴트/우/rope_2.png"]],[["캐릭터/주연/위/사다리/좌/ladder_0.png","캐릭터/주연/위/사다리/좌/ladder_1.png","캐릭터/주연/위/사다리/좌/ladder_2.png"],["캐릭터/주연/위/사다리/우/ladder_0.png","캐릭터/주연/위/사다리/우/ladder_1.png","캐릭터/주연/위/사다리/우/ladder_2.png"]]],[[["캐릭터/주연/아래/디폴트/좌/prone_0.png"],["캐릭터/주연/아래/디폴트/우/prone_0.png"]]]]

class Character(Object):
    def __init__(self, file_set, scene, x, y, motion, mask, dir, shown, control):    ##________(file_set) [0: 정지, 1:이동, 2:사다리타기, 3: 엎드리기 ...] [0: 디폴트, ...] [0: 좌, 1: 우]
        super().__init__(file_set[motion][mask][dir][0])
        self.locate(scene, x, y)
        if shown:
            self.show()

        self.images=file_set
        self.state=[motion, mask, dir, 0]
        self.location=[scene, x, y]
        self.control=control
        self.speed=3

        self.motion_timer=Timer(0.03)
        self.motion_count=0
        def motion_timer_onTimeout():
            global key
            global exam
            exam.set(key)##______________________test
            self.motion_count+=1
   
            if key==83:
                self.state[0]=1
                self.state[2]=1
                self.state[3]=int(self.motion_count%25/5)
                if self.location[1]+self.speed<1280:
                    self.location[1]+=self.speed
            elif key==82:
                self.state[0]=1
                self.state[2]=0
                self.state[3]=int(self.motion_count%25/5)
                if self.location[1]-self.speed>0:
                    self.location[1]-=self.speed
            elif key==85:
                self.state[0]=3
                self.state[3]=self.motion_count%1
            else:
                self.state[0]=0
                self.state[3]=int(self.motion_count%20/5)

            self.setImage(self.images[self.state[0]][self.state[1]][self.state[2]][self.state[3]])
            self.locate(self.location[0], self.location[1], self.location[2])
            if shown:
                self.show()
            else:
                self.hide()
            self.motion_timer.set(0.03)
            self.motion_timer.start()
        self.motion_timer.onTimeout=motion_timer_onTimeout

hellgate=Scene("지옥문", "지옥문/1.png")

leading_roll=Character(leading_roll_file_set, hellgate, 150, 135, 0, 0, 0, True, False)

control_character=leading_roll
key=10
def press_key(scene, k, pressed):
    global key
    if pressed:
        key=k
    else:
        key=0
Scene.onKeyboardDefault=press_key

exam=Timer(key)
showTimer(exam)##______________________test

control_character.motion_timer.start()

hellgate_animator=Animator(hellgate)
hellgate_animator.fade_in(0,1)


def hellgate_onEnter():
    hellgate_animator.start()
hellgate.onEnter=hellgate_onEnter

startGame(hellgate)