from bangtal import *
from animator import *
import random

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

class Character(Object):
    def __init__(self, file_set, scene, x, y, motion, mask, dir, shown, control):    ##________(file_set) [0: 정지, 1:이동, 2:사다리타기, 3: 엎드리기 4:점프 5:공격] [0: 디폴트, ...] [0: 좌, 1: 우]
        super().__init__(file_set[motion][mask][dir][0])
        self.locate(scene, x, y)
        if shown:
            self.show()

        self.shown=shown
        self.images=file_set
        self.state=[motion, mask, dir, random.randint(0,3)]
        self.location=[scene, x, y]
        self.control=control
        self.x_speed=4
        self.y_speed=0
        self.gravity_accel=-1
        self.on_jump=False
        self.on_rope=False
        self.on_attack=False
        self.attack_count=0
        self.key=0

        self.motion_timer=Timer(0.03)
        self.motion_count=0
        def motion_timer_onTimeout():
            global key
            global exam
            if not on_event:
                self.key=key

            self.motion_count+=1

            if (self.control or on_event) and not self.on_attack:
                if self.key==83 and not self.on_rope:
                    move_right(self)
                elif self.key==82 and not self.on_rope:
                    move_left(self)
                elif self.key==217 and not self.on_rope:      ##공격
                    attack(self)
                elif self.key==219 and not self.on_rope:      ##점프
                    jump(self)
                elif self.key==84:   ##사다리타기
                    up(self)
                elif self.key==85:
                    if self.location[0].rope_signal(self.location[1], self.location[2]):
                        down(self)
                    else:
                        prone(self)
                        self.on_rope=False
                else:
                    if not self.on_rope:
                        stand(self)

            elif self.on_attack:
                attack(self)
            else:
                stand(self)

            if not self.on_rope:
                gravity(self)

            if self.control==True:
                self.location[0].player_location[0]=self.location[1]
                self.location[0].player_location[1]=self.location[2]
                exam.set(self.location[2])##______________________test 추후 삭제 요망
            character_locate(self)

            self.motion_timer.set(0.03)
            self.motion_timer.start()
        self.motion_timer.onTimeout=motion_timer_onTimeout
        self.motion_timer.start()

        def attack(self):
            if not self.on_attack:
                self.location[0].hit_signal(self.location[1], self.location[2], self.state[2])
                self.on_attack=True
                self.state[0]=5
                self.state[3]=int(self.attack_count%20/5)
                self.attack_count+=1
            elif self.attack_count%20==0:
                self.on_attack=False
            else:
                self.state[0]=5
                self.state[3]=int(self.attack_count%20/5)
                self.attack_count+=1


        def up(self):
            if self.location[0].portal(self.location[1], self.location[2]) and self.location[0].kill_count==self.location[0].kill_quest:    #포탈
                self.location[0].clear=True
                target=self.location[0].portal(self.location[1], self.location[2])
                target.enter()
            elif self.location[0].rope_signal(self.location[1], self.location[2]+10):      #사다리타기
                self.y_speed=3
                self.on_rope=True
                self.on_jump=False
                self.state[0]=2
                self.state[3]=int(self.motion_count%15/5)
                if self.location[2]+self.y_speed<760:
                    self.location[2]+=self.y_speed
                self.y_speed=0
            else:
                self.state[0]=0
                self.state[3]=int(self.motion_count%20/5)
                self.on_rope=False

        def down(self):
            self.y_speed=3
            self.on_rope=True
            self.state[0]=2
            self.state[3]=int(self.motion_count%15/5)
            if self.location[2]-self.y_speed>0:
                self.location[2]-=self.y_speed
            self.y_speed=0

        def move_right(self):
            self.state[0]=1
            self.state[2]=1
            self.state[3]=int(self.motion_count%25/5)
            if self.location[1]+self.x_speed<1240:
                self.location[1]+=self.x_speed


        def move_left(self):
            self.state[0]=1
            self.state[2]=0
            self.state[3]=int(self.motion_count%25/5)
            if self.location[1]-self.x_speed>0:
                self.location[1]-=self.x_speed


        def prone(self):
            self.state[0]=3
            self.state[3]=self.motion_count%1

        def jump(self):
            if not self.on_jump:
                self.on_jump=True
                self.y_speed=10
        
        def stand(self):
            self.state[0]=0
            self.state[3]=int(self.motion_count%20/5)

        def gravity(self):
            if self.on_jump==True or self.location[2]!=self.location[0].ground(self.location[1], self.location[2]):
                self.on_jump=True
                if self.location[2]+self.y_speed>self.location[0].ground(self.location[1], self.location[2]):
                    self.location[2]+=self.y_speed
                    self.y_speed+=self.gravity_accel
                else:
                    self.location[2]=self.location[0].ground(self.location[1], self.location[2])
                    self.y_speed=0
                    self.on_jump=False
            else:
                self.on_jump=False

        def character_locate(self):
            if self.on_jump:
                self.state[0]=4
                self.state[3]=0
            self.setImage(self.images[self.state[0]][self.state[1]][self.state[2]][self.state[3]])
            self.locate(self.location[0], self.location[1], self.location[2])
            if self.shown:
                self.show()
            else:
                self.hide()

leading_roll_file_set=[[[["캐릭터/주연/정지/디폴트/좌/stand1_0.png", "캐릭터/주연/정지/디폴트/좌/stand1_1.png", "캐릭터/주연/정지/디폴트/좌/stand1_2.png", "캐릭터/주연/정지/디폴트/좌/stand1_3.png"],["캐릭터/주연/정지/디폴트/우/stand1_0.png", "캐릭터/주연/정지/디폴트/우/stand1_1.png", "캐릭터/주연/정지/디폴트/우/stand1_2.png", "캐릭터/주연/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/주연/이동/디폴트/좌/walk1_0.png","캐릭터/주연/이동/디폴트/좌/walk1_1.png","캐릭터/주연/이동/디폴트/좌/walk1_2.png","캐릭터/주연/이동/디폴트/좌/walk1_3.png","캐릭터/주연/이동/디폴트/좌/walk1_4.png"],["캐릭터/주연/이동/디폴트/우/walk1_0.png","캐릭터/주연/이동/디폴트/우/walk1_1.png","캐릭터/주연/이동/디폴트/우/walk1_2.png","캐릭터/주연/이동/디폴트/우/walk1_3.png","캐릭터/주연/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/주연/위/디폴트/좌/rope_0.png","캐릭터/주연/위/디폴트/좌/rope_1.png","캐릭터/주연/위/디폴트/좌/rope_2.png"],["캐릭터/주연/위/디폴트/우/rope_0.png","캐릭터/주연/위/디폴트/우/rope_1.png","캐릭터/주연/위/디폴트/우/rope_2.png"]],[["캐릭터/주연/위/사다리/좌/ladder_0.png","캐릭터/주연/위/사다리/좌/ladder_1.png","캐릭터/주연/위/사다리/좌/ladder_2.png"],["캐릭터/주연/위/사다리/우/ladder_0.png","캐릭터/주연/위/사다리/우/ladder_1.png","캐릭터/주연/위/사다리/우/ladder_2.png"]]],[[["캐릭터/주연/아래/디폴트/좌/prone_0.png"],["캐릭터/주연/아래/디폴트/우/prone_0.png"]]], [[["캐릭터/주연/점프/디폴트/좌/jump_0.png"],["캐릭터/주연/점프/디폴트/우/jump_0.png"]]],[[["캐릭터/주연/공격/디폴트/좌/attack_0.png", "캐릭터/주연/공격/디폴트/좌/attack_1.png", "캐릭터/주연/공격/디폴트/좌/attack_2.png", "캐릭터/주연/공격/디폴트/좌/attack_3.png"],[ "캐릭터/주연/공격/디폴트/우/attack_0.png", "캐릭터/주연/공격/디폴트/우/attack_1.png", "캐릭터/주연/공격/디폴트/우/attack_2.png", "캐릭터/주연/공격/디폴트/우/attack_3.png"]]]]
deoksoon_file_set=[[[["캐릭터/덕순/정지/디폴트/좌/stand1_0.png", "캐릭터/덕순/정지/디폴트/좌/stand1_1.png", "캐릭터/덕순/정지/디폴트/좌/stand1_2.png", "캐릭터/덕순/정지/디폴트/좌/stand1_3.png"],["캐릭터/덕순/정지/디폴트/우/stand1_0.png", "캐릭터/덕순/정지/디폴트/우/stand1_1.png", "캐릭터/덕순/정지/디폴트/우/stand1_2.png", "캐릭터/덕순/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/덕순/이동/디폴트/좌/walk1_0.png","캐릭터/덕순/이동/디폴트/좌/walk1_1.png","캐릭터/덕순/이동/디폴트/좌/walk1_2.png","캐릭터/덕순/이동/디폴트/좌/walk1_3.png","캐릭터/덕순/이동/디폴트/좌/walk1_4.png"],["캐릭터/덕순/이동/디폴트/우/walk1_0.png","캐릭터/덕순/이동/디폴트/우/walk1_1.png","캐릭터/덕순/이동/디폴트/우/walk1_2.png","캐릭터/덕순/이동/디폴트/우/walk1_3.png","캐릭터/덕순/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/덕순/위/디폴트/좌/rope_0.png","캐릭터/덕순/위/디폴트/좌/rope_1.png","캐릭터/덕순/위/디폴트/좌/rope_2.png"],["캐릭터/덕순/위/디폴트/우/rope_0.png","캐릭터/덕순/위/디폴트/우/rope_1.png","캐릭터/덕순/위/디폴트/우/rope_2.png"]],[["캐릭터/덕순/위/사다리/좌/ladder_0.png","캐릭터/덕순/위/사다리/좌/ladder_1.png","캐릭터/덕순/위/사다리/좌/ladder_2.png"],["캐릭터/덕순/위/사다리/우/ladder_0.png","캐릭터/덕순/위/사다리/우/ladder_1.png","캐릭터/덕순/위/사다리/우/ladder_2.png"]]],[[["캐릭터/덕순/아래/디폴트/좌/prone_0.png"],["캐릭터/덕순/아래/디폴트/우/prone_0.png"]]],[[["캐릭터/덕순/점프/디폴트/좌/jump_0.png"],["캐릭터/덕순/점프/디폴트/우/jump_0.png"]]]]
haewonmaek_file_set=[[[["캐릭터/해원맥/정지/디폴트/좌/stand1_0.png", "캐릭터/해원맥/정지/디폴트/좌/stand1_1.png", "캐릭터/해원맥/정지/디폴트/좌/stand1_2.png", "캐릭터/해원맥/정지/디폴트/좌/stand1_3.png"],["캐릭터/해원맥/정지/디폴트/우/stand1_0.png", "캐릭터/해원맥/정지/디폴트/우/stand1_1.png", "캐릭터/해원맥/정지/디폴트/우/stand1_2.png", "캐릭터/해원맥/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/해원맥/이동/디폴트/좌/walk1_0.png","캐릭터/해원맥/이동/디폴트/좌/walk1_1.png","캐릭터/해원맥/이동/디폴트/좌/walk1_2.png","캐릭터/해원맥/이동/디폴트/좌/walk1_3.png","캐릭터/해원맥/이동/디폴트/좌/walk1_4.png"],["캐릭터/해원맥/이동/디폴트/우/walk1_0.png","캐릭터/해원맥/이동/디폴트/우/walk1_1.png","캐릭터/해원맥/이동/디폴트/우/walk1_2.png","캐릭터/해원맥/이동/디폴트/우/walk1_3.png","캐릭터/해원맥/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/해원맥/위/디폴트/좌/rope_0.png","캐릭터/해원맥/위/디폴트/좌/rope_1.png","캐릭터/해원맥/위/디폴트/좌/rope_2.png"],["캐릭터/해원맥/위/디폴트/우/rope_0.png","캐릭터/해원맥/위/디폴트/우/rope_1.png","캐릭터/해원맥/위/디폴트/우/rope_2.png"]],[["캐릭터/해원맥/위/사다리/좌/ladder_0.png","캐릭터/해원맥/위/사다리/좌/ladder_1.png","캐릭터/해원맥/위/사다리/좌/ladder_2.png"],["캐릭터/해원맥/위/사다리/우/ladder_0.png","캐릭터/해원맥/위/사다리/우/ladder_1.png","캐릭터/해원맥/위/사다리/우/ladder_2.png"]]],[[["캐릭터/해원맥/아래/디폴트/좌/prone_0.png"],["캐릭터/해원맥/아래/디폴트/우/prone_0.png"]]],[[["캐릭터/해원맥/점프/디폴트/좌/jump_0.png"],["캐릭터/해원맥/점프/디폴트/우/jump_0.png"]]],[[['캐릭터/해원맥/공격/디폴트/좌/attack_0.png', '캐릭터/해원맥/공격/디폴트/좌/attack_1.png', '캐릭터/해원맥/공격/디폴트/좌/attack_2.png', '캐릭터/해원맥/공격/디폴트/좌/attack_3.png'],[ '캐릭터/해원맥/공격/디폴트/우/attack_0.png', '캐릭터/해원맥/공격/디폴트/우/attack_1.png', '캐릭터/해원맥/공격/디폴트/우/attack_2.png', '캐릭터/해원맥/공격/디폴트/우/attack_3.png']]]]
gangrim_file_set=[[[["캐릭터/강림/정지/디폴트/좌/stand1_0.png", "캐릭터/강림/정지/디폴트/좌/stand1_1.png", "캐릭터/강림/정지/디폴트/좌/stand1_2.png", "캐릭터/강림/정지/디폴트/좌/stand1_3.png"],["캐릭터/강림/정지/디폴트/우/stand1_0.png", "캐릭터/강림/정지/디폴트/우/stand1_1.png", "캐릭터/강림/정지/디폴트/우/stand1_2.png", "캐릭터/강림/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/강림/이동/디폴트/좌/walk1_0.png","캐릭터/강림/이동/디폴트/좌/walk1_1.png","캐릭터/강림/이동/디폴트/좌/walk1_2.png","캐릭터/강림/이동/디폴트/좌/walk1_3.png","캐릭터/강림/이동/디폴트/좌/walk1_4.png"],["캐릭터/강림/이동/디폴트/우/walk1_0.png","캐릭터/강림/이동/디폴트/우/walk1_1.png","캐릭터/강림/이동/디폴트/우/walk1_2.png","캐릭터/강림/이동/디폴트/우/walk1_3.png","캐릭터/강림/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/강림/위/디폴트/좌/rope_0.png","캐릭터/강림/위/디폴트/좌/rope_1.png","캐릭터/강림/위/디폴트/좌/rope_2.png"],["캐릭터/강림/위/디폴트/우/rope_0.png","캐릭터/강림/위/디폴트/우/rope_1.png","캐릭터/강림/위/디폴트/우/rope_2.png"]],[["캐릭터/강림/위/사다리/좌/ladder_0.png","캐릭터/강림/위/사다리/좌/ladder_1.png","캐릭터/강림/위/사다리/좌/ladder_2.png"],["캐릭터/강림/위/사다리/우/ladder_0.png","캐릭터/강림/위/사다리/우/ladder_1.png","캐릭터/강림/위/사다리/우/ladder_2.png"]]],[[["캐릭터/강림/아래/디폴트/좌/prone_0.png"],["캐릭터/강림/아래/디폴트/우/prone_0.png"]]], [[["캐릭터/강림/점프/디폴트/좌/jump_0.png"],["캐릭터/강림/점프/디폴트/우/jump_0.png"]]],[[['캐릭터/강림/공격/디폴트/좌/attack_0.png', '캐릭터/강림/공격/디폴트/좌/attack_1.png', '캐릭터/강림/공격/디폴트/좌/attack_2.png', '캐릭터/강림/공격/디폴트/좌/attack_3.png'],[ '캐릭터/강림/공격/디폴트/우/attack_0.png', '캐릭터/강림/공격/디폴트/우/attack_1.png', '캐릭터/강림/공격/디폴트/우/attack_2.png', '캐릭터/강림/공격/디폴트/우/attack_3.png']]]]

def character_enter(scene):
    global control_character
    control_character.location[0]=scene
    control_character.location[1]=scene.player_location[0]
    control_character.location[2]=scene.player_location[1]
    control_character.locate(scene, scene.player_location[0], scene.player_location[1])
    control_character.show()

class Portal(Object):
    def __init__(self, scene, x, y):
        self.portal_images=["포탈/Frame0.png","포탈/Frame1.png", "포탈/Frame2.png","포탈/Frame3.png", "포탈/Frame4.png", "포탈/Frame5.png", "포탈/Frame6.png", "포탈/Frame7.png"]
        super().__init__(self.portal_images[0])
        self.locate(scene, x, y)
        self.show()
        self.count=0

        self.timer=Timer(0.08)
        def change():
            self.count+=1
            self.setImage(self.portal_images[self.count%7])
            self.show
            self.timer.set(0.08)
            self.timer.start()
        self.timer.onTimeout=change
        self.timer.start()

class Stage(Scene):
    def __init__(self, title, image, ground, next_x, next_y, before_x, before_y):
        super().__init__(title, image)
        self.ground_function=ground
        self.next_pt_location=[next_x, next_y]
        self.before_pt_location=[before_x, before_y]
        self.rope_location=[]
        if not next_x==0:
            self.next=Portal(self, self.next_pt_location[0], self.next_pt_location[1])
        if not before_x==0:
            self.before=Portal(self, self.before_pt_location[0], self.before_pt_location[1])
        self.next_scene=None
        self.before_scene=None
        
        self.player_location=[before_x, before_y]
        self.clear=False
        self.mob_list=[]
        self.kill_count=0
        self.kill_quest=0

    def onEnter(self):
        character_enter(self)
        self.self_set()
        super().onEnter()

    def self_set(self):
        pass

    def ground(self, x, y):
        return self.ground_function(x, y)

    def portal(self, character_x, character_y):
        if character_x>self.next_pt_location[0] and character_x<self.next_pt_location[0]+54 and character_y>=self.next_pt_location[1] and character_y<self.next_pt_location[1]+150:
            return self.next_scene
        elif character_x>self.before_pt_location[0] and character_x<self.before_pt_location[0]+54 and character_y>=self.before_pt_location[1] and character_y<self.before_pt_location[1]+150:
            return self.before_scene
        else:
            return False

    def hit_signal(self, x, y, dir):
        hit=[[x+(-1)*(100-(50*dir)) , x+dir*100], [y, y+100]]
        for mob in self.mob_list:
            if mob.location[1]>=hit[0][0] and mob.location[1]<=hit[0][1] and mob.location[2]>=hit[1][0] and mob.location[2]<=hit[1][1]:
                mob.hit_signal()

    def rope_signal(self, x, y):
        for rope in self.rope_location:
            if x>rope[0]-10 and x<rope[0]+10 and y>=rope[1] and y<=rope[2]:
                return True
        return False


class Message(Object):
    def __init__(self, scene, animator, file_set):
        super().__init__(file_set[0])
        self.setScale(0.7)
        self.now_x=375
        self.now_y=720-390
        self.scene=scene
        self.locate(scene, self.now_x, self.now_y)
        self.animator=animator

        self.count=0
        self.file_set=file_set

    def onMouseAction(self, x, y, action):
        if action==MouseAction.DRAG_RIGHT:
            self.now_x+=10
            self.locate(self.scene, self.now_x, self.now_y)
        elif action==MouseAction.DRAG_LEFT:
            self.now_x-=10
            self.locate(self.scene, self.now_x, self.now_y)
        elif action==MouseAction.DRAG_UP:
            self.now_y+=10
            self.locate(self.scene, self.now_x, self.now_y)
        elif action==MouseAction.DRAG_DOWN:
            self.now_y-=10
            self.locate(self.scene, self.now_x, self.now_y)
        else:
            self.hide()
            self.count+=1
            self.setImage(self.file_set[self.count])
            self.animator.start()

class Mob(Object):
    def __init__(self, file_set, scene, x, y, right_lim, left_lim, dir, shown, control):    ##________(file_set) [0: 정지, 1:맞음, 2:죽음][0: 좌, 1: 우]
        super().__init__(file_set[0][dir][0])
        self.locate(scene, x, y)
        if shown:
            self.show()

        self.shown=shown
        self.images=file_set
        self.state=[0, dir, 0]
        self.location=[scene, x, y]
        self.control=control
        self.x_speed=3
        self.life=4
        self.on_hit=False
        self.on_death=False
        self.right_limit=right_lim
        self.left_limit=left_lim
        self.key=0

        self.location[0].mob_list.append(self)

        self.death_timer=Timer(0.2)
        self.death_count=0
        def death():
            if self.death_count<10:
                self.state[0]=2
                self.state[2]=self.death_count
                self.death_count+=1
                self.death_timer.set(0.2)
                self.death_timer.start()
            else:
                self.shown=False
        self.death_timer.onTimeout=death

        self.on_hit_timer=Timer(0.5)
        def end_cooltime():
            self.on_hit=False
            self.on_hit_timer.set(0.5)
        self.on_hit_timer.onTimeout=end_cooltime

        self.rullet_timer=Timer(0)
        def rullet():
            self.key=random.randint(0,2)
            self.rullet_timer.set(random.randint(1,3))
            self.rullet_timer.start()
        self.rullet_timer.onTimeout=rullet

        self.motion_timer=Timer(0.03)
        self.motion_count=0
        def motion_timer_onTimeout():
            self.motion_count+=1
            if not self.on_death:
                if self.control and not self.on_hit:
                    self.rullet_timer.start()
                    if self.key==1: 
                        self.move_right()
                    elif self.key==2:
                        self.move_left()
                    else:
                        self.stand()
                else:
                    self.stand()

                if self.on_hit and self.shown:
                    self.hit()

                if self.life==0:
                    self.death_timer.start()
                    self.location[0].kill_count+=1
                    self.on_hit=False
                    self.on_death=True

            character_locate(self)
            self.motion_timer.set(0.03)
            self.motion_timer.start()
        self.motion_timer.onTimeout=motion_timer_onTimeout
        self.motion_timer.start()

        def character_locate(self):
            self.setImage(self.images[self.state[0]][self.state[1]][self.state[2]])
            self.locate(self.location[0], self.location[1], self.location[2])
            if self.shown:
                self.show()
            else:
                self.hide()

    def stand(self):
        self.state[0]=0
        self.state[2]=int(self.motion_count%30/5)

    def move_right(self):
        self.state[0]=3
        self.state[1]=1
        self.state[2]=int(self.motion_count%30/5)
        if self.location[1]+self.x_speed<self.right_limit:
            self.location[1]+=self.x_speed

    def move_left(self):
        self.state[0]=3
        self.state[1]=0
        self.state[2]=int(self.motion_count%30/5)
        if self.location[1]-self.x_speed>self.left_limit:
            self.location[1]-=self.x_speed

    def hit(self):
        self.state[0]=1
        self.state[2]=0

    def hit_signal(self):
        self.life-=1
        self.on_hit=True
        self.on_hit_timer.start()

    def onMouseAction(self, x, y, action):
        self.hit_signal()



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
        hellgate_1.enter()
title_clk.onTimeout=title_change

intro_animator=Animator(intro)
intro_animator.fade_out(1, 2)
intro_animator.light_off(3, 1)
intro_animator.reserve(3, title_clk)
intro_animator.fade_out(5, 2)
intro_animator.light_off(7, 1)
intro_animator.reserve(7, title_clk)
intro_animator.fade_out(9, 2)
intro_animator.light_off(11, 1)
intro_animator.reserve(11, title_clk)
intro_animator.fade_out(13, 2)
intro_animator.light_off(15, 1)
intro_animator.reserve(15, title_clk)

def intro_onEnter():
    intro_animator.start()
intro.onEnter=intro_onEnter

def intro_onLeave():
    intro_animator.stop()
intro.onLeave=intro_onLeave
###________________________________________________________________________________________/인트로
###________________________________________________________________________________________지옥문1
def hellgate_1_ground(x, y):
    if x<450:
        return 130
    elif x<580:
        return int(130+7*(x-450)/13)
    elif x<810:
        return 200
    elif x<918:
        return int(200+70*(x-810)/108)
    else:
        return 270

hellgate_1=Stage("지옥문", "지옥문/1.png", hellgate_1_ground, 1137, 760-510, 0, 0)
hellgate_1_animator=Animator(hellgate_1)
hellgate_1_message=Message(hellgate_1, hellgate_1_animator, ["지옥문/대화 0.png", "지옥문/대화 1.png", "지옥문/대화 2.png","지옥문/대화 3.png","지옥문/대화 4.png","지옥문/대화 5.png","지옥문/대화 6.png", "지옥문/귀인이요.png", "end"])

leading_roll=Character(leading_roll_file_set, hellgate_1, 210, 135, 0, 0, 0, True, True)
deoksoon=Character(deoksoon_file_set, hellgate_1, -100, 135, 0, 0, 0, True, False)
haewonmaek=Character(haewonmaek_file_set, hellgate_1, -150, 135, 0, 0, 0, True, False)
gangrim=Character(gangrim_file_set, hellgate_1, -170, 135, 0, 0, 0, True, False)

control_character=leading_roll
def control(character):
    global control_character
    for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
        self.control=False
    character.control=True
    control_character=character
control(leading_roll)

on_event=False
on_pause=False

key=1
def press_key(scene, k, pressed):
    global key
    global on_event
    if not on_event:
        if pressed:
            key=k
        else:
            key=0   
Scene.onKeyboardDefault=press_key

def input_key(character, key):
    character.key=key

exam=Timer(key)
showTimer(exam)##______________________test 추후 삭제 요망


hellgate_1_timeline=Timer(0)
hellgate_1_timeline_count=0
def hellgate_1_timeline_next():
    global hellgate_1_animator
    global hellgate_1_timeline_count
    global on_event

    if hellgate_1_timeline_count==0:
        hellgate_1_message.show()
        hellgate_1_animator.stop()

    elif hellgate_1_timeline_count==1:
        input_key(leading_roll, 0)
        input_key(deoksoon, 83)
        input_key(haewonmaek, 83)
        input_key(gangrim, 83)

    elif hellgate_1_timeline_count==2:
        input_key(deoksoon, 0)
        input_key(haewonmaek, 0)
        input_key(gangrim, 0)
        hellgate_1_message.show()
        hellgate_1_animator.stop()

    elif hellgate_1_timeline_count<=7:
        hellgate_1_message.show()
        hellgate_1_animator.stop()

    elif hellgate_1_timeline_count==8:
        hellgate_1_message.show()
        hellgate_1_animator.stop()
        showMessage("이동: 방향키\n점프: alt\n다음 장소로 이동해주세요")
        on_event=False
        hellgate_1.clear=True

    hellgate_1_timeline_count+=1
hellgate_1_timeline.onTimeout=hellgate_1_timeline_next


hellgate_1_animator.fade_in(0,1)
hellgate_1_animator.reserve(1, hellgate_1_timeline)
hellgate_1_animator.reserve(2, hellgate_1_timeline)
hellgate_1_animator.reserve(4, hellgate_1_timeline)
hellgate_1_animator.reserve(5, hellgate_1_timeline)
hellgate_1_animator.reserve(6, hellgate_1_timeline)
hellgate_1_animator.reserve(7, hellgate_1_timeline)
hellgate_1_animator.reserve(8, hellgate_1_timeline)
hellgate_1_animator.reserve(9, hellgate_1_timeline)
hellgate_1_animator.reserve(10, hellgate_1_timeline)

def hellgate_1_onEnter():
    global on_event
    global hellgate_1

    character_enter(hellgate_1)
    if not hellgate_1.clear:
        hellgate_1_animator.start()
        on_event=True
        leading_roll.locate(hellgate_1, 200, 135)
        leading_roll.show()
        input_key(leading_roll, 85)
hellgate_1.self_set=hellgate_1_onEnter

###________________________________________________________________________________________지옥문1/지옥문2

def hellgate_2_ground(x, y):
    if x<380:
        return 270
    elif x<460:
        return int((x*(-1)*7/8)+7*380/8+270)
    elif x<610:
        return 200
    elif x<715:
        return int((x*(-1)*14/21)+14*610/21+200)
    else:
        return 130

hellgate_2=Stage("지옥문", "지옥문/2.png", hellgate_2_ground, 1090, 760-630, 60, 250)
hellgate_1.next_scene=hellgate_2
hellgate_2.before_scene=hellgate_1
hellgate_2_animator=Animator(hellgate_2)
hellgate_2_message=Message(hellgate_2, hellgate_2_animator, ["지옥문/대화 7.png", "지옥문/대화 8.png", "지옥문/대화 9.png", "end"])

hellgate_2_subtimer=Timer(0.1)
def hellgate_2_checker():
    if deoksoon.location[1]>=1200:
        input_key(deoksoon,0)
        deoksoon.state[2]=0
    hellgate_2_subtimer.set(0.1)
    hellgate_2_subtimer.start()
hellgate_2_subtimer.onTimeout=hellgate_2_checker

hellgate_2_timeline=Timer(0)
hellgate_2_timeline_count=0
def hellgate_2_timeline_next():
    global hellgate_2_animator
    global hellgate_2_timeline_count
    global on_event
    global hellgate_2_subtimer

    if hellgate_2_timeline_count==0:
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            input_key(self, 83)
        hellgate_2_subtimer.start()

    elif hellgate_2_timeline_count==1:
        for self in [gangrim, leading_roll, haewonmaek]:
            input_key(self, 0)
        gangrim.state[2]=0
        hellgate_2_message.show()
        hellgate_2_animator.stop()

    elif hellgate_2_timeline_count<=2:
        hellgate_2_message.show()
        hellgate_2_animator.stop()

    elif hellgate_2_timeline_count==3:
        leading_roll.state[2]=0
        hellgate_2_message.show()
        hellgate_2_animator.stop()

    elif hellgate_2_timeline_count==4:
        showMessage("다음 장소로 이동해주세요")
        hellgate_2.clear=True
        on_event=False

    hellgate_2_timeline_count+=1    
hellgate_2_timeline.onTimeout=hellgate_2_timeline_next

hellgate_2_animator.reserve(0, hellgate_2_timeline)
hellgate_2_animator.reserve(4, hellgate_2_timeline)
hellgate_2_animator.reserve(5, hellgate_2_timeline)
hellgate_2_animator.reserve(6, hellgate_2_timeline)
hellgate_2_animator.reserve(7, hellgate_2_timeline)


def hellgate_2_onEnter():
    global on_event
    global hellgate_2

    character_enter(hellgate_2)
    if not hellgate_2.clear:
        on_event=True
        deoksoon.location[1]=-50
        gangrim.location[1]=-150
        leading_roll.location[1]=-230
        haewonmaek.location[1]=-310
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            self.location[0]=hellgate_2
            self.location[2]=270
            self.locate(hellgate_2, self.location[1], 270)
            self.show()
        hellgate_2_animator.start()
hellgate_2.self_set=hellgate_2_onEnter
###________________________________________________________________________________________지옥문2/천륜지옥1
stormfox_file_set=[[['몹/돌풍여우/디폴트/좌/Frame0.png', '몹/돌풍여우/디폴트/좌/Frame1.png', '몹/돌풍여우/디폴트/좌/Frame2.png', '몹/돌풍여우/디폴트/좌/Frame3.png', '몹/돌풍여우/디폴트/좌/Frame4.png', '몹/돌풍여우/디폴트/좌/Frame5.png'],['몹/돌풍여우/디폴트/우/Frame0.png', '몹/돌풍여우/디폴트/우/Frame1.png', '몹/돌풍여우/디폴트/우/Frame2.png', '몹/돌풍여우/디폴트/우/Frame3.png', '몹/돌풍여우/디폴트/우/Frame4.png', '몹/돌풍여우/디폴트/우/Frame5.png']],[['몹/돌풍여우/맞음/좌/hit.png'],['몹/돌풍여우/맞음/우/hit.png']],[['몹/돌풍여우/죽음/좌/die0.png','몹/돌풍여우/죽음/좌/die1.png','몹/돌풍여우/죽음/좌/die2.png','몹/돌풍여우/죽음/좌/die3.png','몹/돌풍여우/죽음/좌/die4.png','몹/돌풍여우/죽음/좌/die5.png','몹/돌풍여우/죽음/좌/die6.png','몹/돌풍여우/죽음/좌/die7.png','몹/돌풍여우/죽음/좌/die8.png','몹/돌풍여우/죽음/좌/die9.png'],['몹/돌풍여우/죽음/우/die0.png','몹/돌풍여우/죽음/우/die1.png','몹/돌풍여우/죽음/우/die2.png','몹/돌풍여우/죽음/우/die3.png','몹/돌풍여우/죽음/우/die4.png','몹/돌풍여우/죽음/우/die5.png','몹/돌풍여우/죽음/우/die6.png','몹/돌풍여우/죽음/우/die7.png','몹/돌풍여우/죽음/우/die8.png','몹/돌풍여우/죽음/우/die9.png']],[['몹/돌풍여우/이동/좌/Frame0.png', '몹/돌풍여우/이동/좌/Frame1.png', '몹/돌풍여우/이동/좌/Frame2.png', '몹/돌풍여우/이동/좌/Frame3.png', '몹/돌풍여우/이동/좌/Frame4.png', '몹/돌풍여우/이동/좌/Frame5.png'],['몹/돌풍여우/이동/우/Frame0.png', '몹/돌풍여우/이동/우/Frame1.png', '몹/돌풍여우/이동/우/Frame2.png', '몹/돌풍여우/이동/우/Frame3.png', '몹/돌풍여우/이동/우/Frame4.png', '몹/돌풍여우/이동/우/Frame5.png']]]
def cheonryun_ground_1(x, y):
    return 130

cheonryun_1=Stage("천륜지옥", "천륜지옥/스테이지0.png", cheonryun_ground_1, 1090, 110, 60, 110)
hellgate_2.next_scene=cheonryun_1
cheonryun_1.before_scene=hellgate_2
cr1_animator=Animator(cheonryun_1)
cr1_message=Message(cheonryun_1, cr1_animator, ["천륜지옥/대화 0.png","천륜지옥/대화 1.png","천륜지옥/대화 2.png","천륜지옥/대화 3.png", "end"])

sf_0=Mob(stormfox_file_set, cheonryun_1, 800, 130, 1200, 50, 0, False, False)
sf_1=Mob(stormfox_file_set, cheonryun_1, 600, 130, 1200, 50, 0, False, False)
sf_2=Mob(stormfox_file_set, cheonryun_1, 700, 130, 1200, 50, 0, False, False)

cr1_timeline=Timer(0)
cr1_timeline_count=0
def cr1_timeline_next():
    global cr1_animator
    global cr1_timeline_count
    global on_event

    if cr1_timeline_count==0:
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            input_key(self, 83)

    elif cr1_timeline_count==1:
        input_key(deoksoon, 219)
        for self in [gangrim, leading_roll, haewonmaek]:
            input_key(self, 0)
        for mob in cheonryun_1.mob_list:
            mob.shown=True
        cr1_message.show()
        cr1_animator.stop()
        
    elif cr1_timeline_count<=3:
        input_key(deoksoon, 0)
        cr1_message.show()
        cr1_animator.stop()
    
    elif cr1_timeline_count==4:
        gangrim.state[2]=0
        cr1_message.show()
        cr1_animator.stop()

    elif cr1_timeline_count==5:
        for mob in cheonryun_1.mob_list:
            mob.control=True
        on_event=False
        control(gangrim)
    cr1_timeline_count+=1    
cr1_timeline.onTimeout=cr1_timeline_next

cr1_animator.reserve(0, cr1_timeline)
cr1_animator.reserve(3, cr1_timeline)
cr1_animator.reserve(4, cr1_timeline)
cr1_animator.reserve(5, cr1_timeline)
cr1_animator.reserve(6, cr1_timeline)
cr1_animator.reserve(7, cr1_timeline)


def cr1_onEnter():
    global on_event
    global cheonryun_1

    character_enter(cheonryun_1)
    if not cheonryun_1.clear:
        cheonryun_1.kill_quest=3
        on_event=True
        deoksoon.location[1]=-50
        gangrim.location[1]=-150
        leading_roll.location[1]=-220
        haewonmaek.location[1]=-290
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            self.location[0]=cheonryun_1
            self.location[2]=130
            self.locate(self.location[0], self.location[1], self.location[2])
            self.show()
        cr1_animator.start()
cheonryun_1.self_set=cr1_onEnter

###________________________________________________________________________________________천륜지옥1/천륜지옥2

def cheonryun_ground_2(x, y):
    if y>=360 and x>=740 and x<=1150:
        return 370
    elif y>=250 and x>=410 and x<=680:
        return 260
    else:
        return 50

cheonryun_2=Stage("천륜지옥", "천륜지옥/스테이지1.png", cheonryun_ground_2, 1090, 30, 60, 30)
cheonryun_1.next_scene=cheonryun_2
cheonryun_2.before_scene=cheonryun_1

sf_3=Mob(stormfox_file_set, cheonryun_2, 500, 50, 1200, 50, 0, True, True)
sf_4=Mob(stormfox_file_set, cheonryun_2, 900, 50, 1200, 50, 0, True, True)
sf_5=Mob(stormfox_file_set, cheonryun_2, 500, 260, 680, 420,  0, True, True)
sf_6=Mob(stormfox_file_set, cheonryun_2, 900, 370, 1150, 740, 0, True, True)

cheonryun_2.rope_location.append([520, 60, 260])
cheonryun_2.rope_location.append([950, 60, 370])


def cr2_onEnter():
    global on_event

    if not cheonryun_2.clear:
        cheonryun_2.kill_quest=4
cheonryun_2.self_set=cr2_onEnter

###________________________________________________________________________________________천륜지옥2/천륜지옥3

def cheonryun_ground_3(x, y):
    if y>=260 and x<=540:
        return 270
    elif y>=370 and x>=585 and x<=1015:
        return 380
    else:
        return 50

cheonryun_3=Stage("천륜지옥", "천륜지옥/스테이지2.png", cheonryun_ground_3, 1090, 30, 60, 30)
cheonryun_2.next_scene=cheonryun_3
cheonryun_3.before_scene=cheonryun_2

sf_7=Mob(stormfox_file_set, cheonryun_3, 540, 50, 1200, 50, 0, True, True)
sf_8=Mob(stormfox_file_set, cheonryun_3, 800, 50, 1200, 50, 0, True, True)
sf_9=Mob(stormfox_file_set, cheonryun_3, 90, 270, 540, 50, 0, True, True)
sf_10=Mob(stormfox_file_set, cheonryun_3, 360, 270, 540, 50, 0, True, True)
sf_11=Mob(stormfox_file_set, cheonryun_3, 800, 380, 1015, 585, 0, True, True)

cheonryun_3.rope_location.append([370, 60, 270])
cheonryun_3.rope_location.append([725, 60, 380])
#cheonryun_3.rope_location.append([200, 270, 760])

def cr3_onEnter():
    global on_event

    if not cheonryun_3.clear:
        cheonryun_3.kill_quest=5
cheonryun_3.self_set=cr3_onEnter


###________________________________________________________________________________________천륜지옥3/천륜지옥4
asf_file_set=[[['몹/사나운 돌풍여우/디폴트/좌/Frame0.png', '몹/사나운 돌풍여우/디폴트/좌/Frame1.png', '몹/사나운 돌풍여우/디폴트/좌/Frame2.png', '몹/사나운 돌풍여우/디폴트/좌/Frame3.png', '몹/사나운 돌풍여우/디폴트/좌/Frame4.png', '몹/사나운 돌풍여우/디폴트/좌/Frame5.png'],['몹/사나운 돌풍여우/디폴트/우/Frame0.png', '몹/사나운 돌풍여우/디폴트/우/Frame1.png', '몹/사나운 돌풍여우/디폴트/우/Frame2.png', '몹/사나운 돌풍여우/디폴트/우/Frame3.png', '몹/사나운 돌풍여우/디폴트/우/Frame4.png', '몹/사나운 돌풍여우/디폴트/우/Frame5.png']],[['몹/사나운 돌풍여우/맞음/좌/hit.png'],['몹/사나운 돌풍여우/맞음/우/hit.png']],[['몹/사나운 돌풍여우/죽음/좌/die0.png','몹/사나운 돌풍여우/죽음/좌/die1.png','몹/사나운 돌풍여우/죽음/좌/die2.png','몹/사나운 돌풍여우/죽음/좌/die3.png','몹/사나운 돌풍여우/죽음/좌/die4.png','몹/사나운 돌풍여우/죽음/좌/die5.png','몹/사나운 돌풍여우/죽음/좌/die6.png','몹/사나운 돌풍여우/죽음/좌/die7.png','몹/사나운 돌풍여우/죽음/좌/die8.png','몹/사나운 돌풍여우/죽음/좌/die9.png'],['몹/사나운 돌풍여우/죽음/우/die0.png','몹/사나운 돌풍여우/죽음/우/die1.png','몹/사나운 돌풍여우/죽음/우/die2.png','몹/사나운 돌풍여우/죽음/우/die3.png','몹/사나운 돌풍여우/죽음/우/die4.png','몹/사나운 돌풍여우/죽음/우/die5.png','몹/사나운 돌풍여우/죽음/우/die6.png','몹/사나운 돌풍여우/죽음/우/die7.png','몹/사나운 돌풍여우/죽음/우/die8.png','몹/사나운 돌풍여우/죽음/우/die9.png']],[['몹/사나운 돌풍여우/이동/좌/Frame0.png', '몹/사나운 돌풍여우/이동/좌/Frame1.png', '몹/사나운 돌풍여우/이동/좌/Frame2.png', '몹/사나운 돌풍여우/이동/좌/Frame3.png', '몹/사나운 돌풍여우/이동/좌/Frame4.png', '몹/사나운 돌풍여우/이동/좌/Frame5.png'],['몹/사나운 돌풍여우/이동/우/Frame0.png', '몹/사나운 돌풍여우/이동/우/Frame1.png', '몹/사나운 돌풍여우/이동/우/Frame2.png', '몹/사나운 돌풍여우/이동/우/Frame3.png', '몹/사나운 돌풍여우/이동/우/Frame4.png', '몹/사나운 돌풍여우/이동/우/Frame5.png']]]
def cheonryun_ground_4(x, y):
    if y>=340 and x>=480 and x<=900:
        return 350
    elif y>=280 and x>=955 and x<=1085:
        return 290
    elif y>=410 and x>=1115:
        return 420
    else:
        return 50

cheonryun_4=Stage("천륜지옥", "천륜지옥/스테이지3.png", cheonryun_ground_4, 1090, 30, 60, 30)
cheonryun_3.next_scene=cheonryun_4
cheonryun_4.before_scene=cheonryun_3

asf_0=Mob(asf_file_set, cheonryun_4, 450, 50, 1200, 50, 0, True, True)
asf_1=Mob(asf_file_set, cheonryun_4, 720, 50, 1200, 50, 0, True, True)
asf_2=Mob(asf_file_set, cheonryun_4, 1000, 50, 1200, 50, 0, True, True)
asf_3=Mob(asf_file_set, cheonryun_4, 500, 350, 900, 480, 0, True, True)

cheonryun_4.rope_location.append([1185, 60, 420])
cheonryun_4.rope_location.append([725, 60, 350])

def cr4_onEnter():
    global on_event

    if not cheonryun_4.clear:
        cheonryun_4.kill_quest=4
cheonryun_4.self_set=cr4_onEnter
###________________________________________________________________________________________천륜지옥4/천륜지옥5

def cheonryun_ground_5(x, y):
    if y>=350 and x>=200 and x<=760:
        return 360
    else:
        return 50

cheonryun_5=Stage("천륜지옥", "천륜지옥/스테이지4.png", cheonryun_ground_5, 1090, 30, 60, 30)
cheonryun_4.next_scene=cheonryun_5
cheonryun_5.before_scene=cheonryun_4

asf_4=Mob(asf_file_set, cheonryun_5, 450, 50, 1200, 50, 0, True, True)
asf_5=Mob(asf_file_set, cheonryun_5, 720, 50, 1200, 50, 0, True, True)
asf_6=Mob(asf_file_set, cheonryun_5, 300, 360, 760, 200, 0, True, True)
asf_7=Mob(asf_file_set, cheonryun_5, 600, 360, 760, 200, 0, True, True)

cheonryun_5.rope_location.append([560, 60, 360])

def cr5_onEnter():
    global on_event

    if not cheonryun_5.clear:
        cheonryun_5.kill_quest=4
cheonryun_5.self_set=cr5_onEnter
###________________________________________________________________________________________천륜지옥5/천륜지옥6
yeomla_file_set=[[[["캐릭터/염라대왕/정지/디폴트/좌/stand1_0.png", "캐릭터/염라대왕/정지/디폴트/좌/stand1_1.png", "캐릭터/염라대왕/정지/디폴트/좌/stand1_2.png", "캐릭터/염라대왕/정지/디폴트/좌/stand1_3.png"],["캐릭터/염라대왕/정지/디폴트/우/stand1_0.png", "캐릭터/염라대왕/정지/디폴트/우/stand1_1.png", "캐릭터/염라대왕/정지/디폴트/우/stand1_2.png", "캐릭터/염라대왕/정지/디폴트/우/stand1_3.png"]]],[[["캐릭터/염라대왕/이동/디폴트/좌/walk1_0.png","캐릭터/염라대왕/이동/디폴트/좌/walk1_1.png","캐릭터/염라대왕/이동/디폴트/좌/walk1_2.png","캐릭터/염라대왕/이동/디폴트/좌/walk1_3.png","캐릭터/염라대왕/이동/디폴트/좌/walk1_4.png"],["캐릭터/염라대왕/이동/디폴트/우/walk1_0.png","캐릭터/염라대왕/이동/디폴트/우/walk1_1.png","캐릭터/염라대왕/이동/디폴트/우/walk1_2.png","캐릭터/염라대왕/이동/디폴트/우/walk1_3.png","캐릭터/염라대왕/이동/디폴트/우/walk1_4.png"]]],[[["캐릭터/염라대왕/위/디폴트/좌/rope_0.png","캐릭터/염라대왕/위/디폴트/좌/rope_1.png","캐릭터/염라대왕/위/디폴트/좌/rope_2.png"],["캐릭터/염라대왕/위/디폴트/우/rope_0.png","캐릭터/염라대왕/위/디폴트/우/rope_1.png","캐릭터/염라대왕/위/디폴트/우/rope_2.png"]],[["캐릭터/염라대왕/위/사다리/좌/ladder_0.png","캐릭터/염라대왕/위/사다리/좌/ladder_1.png","캐릭터/염라대왕/위/사다리/좌/ladder_2.png"],["캐릭터/염라대왕/위/사다리/우/ladder_0.png","캐릭터/염라대왕/위/사다리/우/ladder_1.png","캐릭터/염라대왕/위/사다리/우/ladder_2.png"]]],[[["캐릭터/염라대왕/아래/디폴트/좌/prone_0.png"],["캐릭터/염라대왕/아래/디폴트/우/prone_0.png"]]],[[["캐릭터/염라대왕/점프/디폴트/좌/jump_0.png"],["캐릭터/염라대왕/점프/디폴트/우/jump_0.png"]]]]

def cheonryun_ground_6(x, y):
    if y>=270 and x>=900:
        return 280
    else:
        return 50

cheonryun_6=Stage("천륜지옥", "천륜지옥/배경1.png", cheonryun_ground_6, 1090, 30, 60, 30)
cheonryun_5.next_scene=cheonryun_6
cheonryun_6.before_scene=cheonryun_5
cr6_animator=Animator(cheonryun_6)
yeomla=Character(yeomla_file_set, cheonryun_6, 1040, 280, 0, 0, 0, True, False)
cr6_message=Message(cheonryun_6, cr6_animator, ["천륜지옥/대화 4.png","천륜지옥/대화 5.png","천륜지옥/대화 6.png","천륜지옥/대화 7.png", "천륜지옥/대화 8.png", "천륜지옥/대화 9.png", "end"])

cr6_timeline=Timer(0)
cr6_timeline_count=0
def cr6_timeline_next():
    global cr6_animator
    global cr6_timeline_count
    global on_event

    if cr6_timeline_count<=3:
        cr6_message.show()
        cr6_animator.stop()
    elif cr6_timeline_count==4:
        cr6_message.show()
        cr6_animator.stop()
        input_key(leading_roll, 0)
    elif cr6_timeline_count==5:
        input_key(gangrim, 83)
    elif cr6_timeline_count==6:
        cr6_message.show()
        cr6_animator.stop()
        input_key(gangrim, 0)
    elif cr6_timeline_count==7:
        cheonryun_6.clear=True
        on_event=False
        control(leading_roll)

    cr6_timeline_count+=1    
cr6_timeline.onTimeout=cr6_timeline_next

cr6_animator.fade_in(0, 1)
cr6_animator.reserve(1, cr6_timeline)
cr6_animator.reserve(2, cr6_timeline)
cr6_animator.reserve(3, cr6_timeline)
cr6_animator.reserve(4, cr6_timeline)
cr6_animator.reserve(5, cr6_timeline)
cr6_animator.reserve(6, cr6_timeline)
cr6_animator.reserve(9, cr6_timeline)
cr6_animator.reserve(10, cr6_timeline)


def cr6_onEnter():
    global on_event

    if not cheonryun_6.clear:
        on_event=True
        leading_roll.location[1]=690
        deoksoon.location[1]=400
        gangrim.location[1]=300
        haewonmaek.location[1]=250
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            self.location[0]=cheonryun_6
            self.location[2]=50
            self.state[2]=1
            self.show()
        input_key(leading_roll, 85)
        cr6_animator.start()
cheonryun_6.self_set=cr6_onEnter
###________________________________________________________________________________________천륜지옥6/살인지옥1
def_file_set=[[['몹/방패병/디폴트/좌/Frame0.png', '몹/방패병/디폴트/좌/Frame1.png', '몹/방패병/디폴트/좌/Frame2.png', '몹/방패병/디폴트/좌/Frame3.png', '몹/방패병/디폴트/좌/Frame4.png', '몹/방패병/디폴트/좌/Frame5.png'],['몹/방패병/디폴트/우/Frame0.png', '몹/방패병/디폴트/우/Frame1.png', '몹/방패병/디폴트/우/Frame2.png', '몹/방패병/디폴트/우/Frame3.png', '몹/방패병/디폴트/우/Frame4.png', '몹/방패병/디폴트/우/Frame5.png']],[['몹/방패병/맞음/좌/hit.png'],['몹/방패병/맞음/우/hit.png']],[['몹/방패병/죽음/좌/die0.png','몹/방패병/죽음/좌/die1.png','몹/방패병/죽음/좌/die2.png','몹/방패병/죽음/좌/die3.png','몹/방패병/죽음/좌/die4.png','몹/방패병/죽음/좌/die5.png','몹/방패병/죽음/좌/die6.png','몹/방패병/죽음/좌/die7.png','몹/방패병/죽음/좌/die8.png','몹/방패병/죽음/좌/die9.png'],['몹/방패병/죽음/우/die0.png','몹/방패병/죽음/우/die1.png','몹/방패병/죽음/우/die2.png','몹/방패병/죽음/우/die3.png','몹/방패병/죽음/우/die4.png','몹/방패병/죽음/우/die5.png','몹/방패병/죽음/우/die6.png','몹/방패병/죽음/우/die7.png','몹/방패병/죽음/우/die8.png','몹/방패병/죽음/우/die9.png']],[['몹/방패병/이동/좌/Frame0.png', '몹/방패병/이동/좌/Frame1.png', '몹/방패병/이동/좌/Frame2.png', '몹/방패병/이동/좌/Frame3.png', '몹/방패병/이동/좌/Frame4.png', '몹/방패병/이동/좌/Frame5.png'],['몹/방패병/이동/우/Frame0.png', '몹/방패병/이동/우/Frame1.png', '몹/방패병/이동/우/Frame2.png', '몹/방패병/이동/우/Frame3.png', '몹/방패병/이동/우/Frame4.png', '몹/방패병/이동/우/Frame5.png']]]
atk_file_set=[[['몹/공격병/디폴트/좌/Frame0.png', '몹/공격병/디폴트/좌/Frame1.png', '몹/공격병/디폴트/좌/Frame2.png', '몹/공격병/디폴트/좌/Frame3.png', '몹/공격병/디폴트/좌/Frame4.png', '몹/공격병/디폴트/좌/Frame5.png'],['몹/공격병/디폴트/우/Frame0.png', '몹/공격병/디폴트/우/Frame1.png', '몹/공격병/디폴트/우/Frame2.png', '몹/공격병/디폴트/우/Frame3.png', '몹/공격병/디폴트/우/Frame4.png', '몹/공격병/디폴트/우/Frame5.png']],[['몹/공격병/맞음/좌/hit.png'],['몹/공격병/맞음/우/hit.png']],[['몹/공격병/죽음/좌/die0.png','몹/공격병/죽음/좌/die1.png','몹/공격병/죽음/좌/die2.png','몹/공격병/죽음/좌/die3.png','몹/공격병/죽음/좌/die4.png','몹/공격병/죽음/좌/die5.png','몹/공격병/죽음/좌/die6.png','몹/공격병/죽음/좌/die7.png','몹/공격병/죽음/좌/die8.png','몹/공격병/죽음/좌/die9.png'],['몹/공격병/죽음/우/die0.png','몹/공격병/죽음/우/die1.png','몹/공격병/죽음/우/die2.png','몹/공격병/죽음/우/die3.png','몹/공격병/죽음/우/die4.png','몹/공격병/죽음/우/die5.png','몹/공격병/죽음/우/die6.png','몹/공격병/죽음/우/die7.png','몹/공격병/죽음/우/die8.png','몹/공격병/죽음/우/die9.png']],[['몹/공격병/이동/좌/Frame0.png', '몹/공격병/이동/좌/Frame1.png', '몹/공격병/이동/좌/Frame2.png', '몹/공격병/이동/좌/Frame3.png', '몹/공격병/이동/좌/Frame4.png', '몹/공격병/이동/좌/Frame5.png'],['몹/공격병/이동/우/Frame0.png', '몹/공격병/이동/우/Frame1.png', '몹/공격병/이동/우/Frame2.png', '몹/공격병/이동/우/Frame3.png', '몹/공격병/이동/우/Frame4.png', '몹/공격병/이동/우/Frame5.png']]]

def md1_ground(x, y):
    if y>=635 and x<=330:
        return 640
    elif y>=520 and x>=365 and x<=1080:
        return 530
    elif y>=340 and x<=460:
        return 345
    else:
        return 160

md1=Stage("살인지옥", "살인지옥/스테이지 0.png", md1_ground, 1110, 140, 40, 140)
cheonryun_6.next_scene=md1
md1.before_scene=cheonryun_6
md1_animator=Animator(md1)
md1_message=Message(md1, md1_animator, ["살인지옥/대화 0.png","살인지옥/대화 1.png","살인지옥/대화 2.png","살인지옥/대화 3.png", "살인지옥/대화 4.png", "end"])

md1.rope_location.append([235, 170, 350])
md1.rope_location.append([948, 170, 530])
md1.rope_location.append([110, 350, 645])
md1.rope_location.append([440, 350, 530])

def_0=Mob(def_file_set, md1, 800, 170, 1200, 50, 0, False, False)
def_1=Mob(def_file_set, md1, 300, 350, 460, 50, 1, False, False)
def_2=Mob(def_file_set, md1, 600, 540, 1080, 365, 0, False, False)
def_3=Mob(def_file_set, md1, 950, 540, 1080, 365, 0, False, False)
def_4=Mob(def_file_set, md1, 300, 170, 1200, 50, 1, False, False)

md1_timeline=Timer(0)
md1_timeline_count=0
def md1_timeline_next():
    global md1_animator
    global md1_timeline_count
    global on_event

    if md1_timeline_count==0:
        for self in [gangrim, leading_roll, haewonmaek, deoksoon]:
            input_key(self, 0)
        md1_message.show()
        md1_animator.stop()
        
    elif md1_timeline_count==1:
        md1_message.show()
        md1_animator.stop()

    elif md1_timeline_count==2:
        md1_message.show()
        md1_animator.stop()
    
    elif md1_timeline_count==3:
        gangrim.state[2]=1
        haewonmaek.state[2]=0
        deoksoon.state[2]=1
        leading_roll.state[2]=0
        for mob in md1.mob_list:
            mob.shown=True
        md1_message.show()
        md1_animator.stop()

    elif md1_timeline_count==4:
        haewonmaek.state[2]=1
        gangrim.state[2]=0
        deoksoon.state[2]=0
        leading_roll.state[2]=1
        md1_message.show()
        md1_animator.stop()

    elif md1_timeline_count==5:
        for mob in md1.mob_list:
            mob.control=True
        on_event=False
        control(haewonmaek)
    md1_timeline_count+=1    
md1_timeline.onTimeout=md1_timeline_next

md1_animator.reserve(0, md1_timeline)
md1_animator.reserve(1, md1_timeline)
md1_animator.reserve(2, md1_timeline)
md1_animator.reserve(3, md1_timeline)
md1_animator.reserve(4, md1_timeline)
md1_animator.reserve(5, md1_timeline)
md1_animator.reserve(6, md1_timeline)


def md1_onEnter():
    global on_event

    character_enter(md1)
    if not md1.clear:
        md1.kill_quest=5
        on_event=True
        deoksoon.location[1]=600
        gangrim.location[1]=670
        leading_roll.location[1]=500
        haewonmaek.location[1]=430
        gangrim.state[2]=0
        deoksoon.state[2]=0
        haewonmaek.state[2]=1
        leading_roll.state[2]=1
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            self.location[0]=md1
            self.location[2]=160
            self.locate(self.location[0], self.location[1], self.location[2])
            self.show()
        md1_animator.start()
md1.self_set=md1_onEnter
###________________________________________________________________________________________살인지옥1/살인지옥2
def md2_ground(x, y):
    if y>=585 and x<=480:
        return 595
    elif y>=565 and x>=580:
        return 575
    elif y>=365 and x<=250:
        return 375
    elif y>=365 and x>=360 and x<=1070:
        return 375
    elif y>=300 and x>=1110:
        return 310
    else:
        return 130

md2=Stage("살인지옥", "살인지옥/스테이지 1.png", md2_ground, 1110, 110, 40, 110)
md1.next_scene=md2
md2.before_scene=md1
md2_animator=Animator(md2)

md2.rope_location.append([510, 140, 375])
md2.rope_location.append([990, 140, 375])
md2.rope_location.append([325, 320, 595])
md2.rope_location.append([630, 370, 575])
md2.rope_location.append([1090, 270, 575])

def_5=Mob(def_file_set, md2, 400, 130, 1200, 50, 0, True, True)
def_6=Mob(def_file_set, md2, 800, 130, 1200, 50, 0, True, True)
def_7=Mob(def_file_set, md2, 700, 375, 1070, 360, 0, True, True)
def_8=Mob(def_file_set, md2, 1000, 575, 1200, 580, 0, True, True)

def md2_onEnter():
    global on_event

    if not md2.clear:
        md2.kill_quest=4
md2.self_set=md2_onEnter
###________________________________________________________________________________________살인지옥2/살인지옥3
def md3_ground(x, y):
    if y>=610 and x<=285:
        return 620
    elif y>=495 and x>=255 and x<=765:
        return 505
    elif y>=440 and x<=210:
        return 450
    elif y>=300 and x>=100 and x<=1030:
        return 310
    else:
        return 130

md3=Stage("살인지옥", "살인지옥/스테이지 2.png", md3_ground, 1110, 110, 40, 110)
md2.next_scene=md3
md3.before_scene=md2
md3_animator=Animator(md3)

md3.rope_location.append([480, 140, 310])
md3.rope_location.append([535, 320, 505])
md3.rope_location.append([235, 330, 620])

def_9=Mob(def_file_set, md3, 450, 130, 1200, 50, 0, True, True)
def_10=Mob(def_file_set, md3, 850, 130, 1200, 50, 0, True, True)
def_11=Mob(def_file_set, md3, 300, 310, 1030, 100, 0, True, True)
def_12=Mob(def_file_set, md3, 700, 310, 1030, 100, 0, True, True)
def_13=Mob(def_file_set, md3, 500, 505, 765, 255, 0, True, True)

def md3_onEnter():
    global on_event

    if not md3.clear:
        md3.kill_quest=5
md3.self_set=md3_onEnter
###________________________________________________________________________________________살인지옥3/살인지옥4

def md4_ground(x, y):
        return 60

md4=Stage("살인지옥", "살인지옥/배경1.png", md4_ground, 1110, 40, 40, 40)
md3.next_scene=md4
md4.before_scene=md3
md4_animator=Animator(md4)
md4_message=Message(md4, md4_animator, ["살인지옥/대화 5.png","살인지옥/대화 6.png","살인지옥/대화 7.png","살인지옥/대화 8.png", "살인지옥/대화 9.png", "살인지옥/대화 10.png", "살인지옥/대화 11.png", "살인지옥/대화 12.png", "end"])
byeonsung=Object("캐릭터/변성대왕/sit.png")
byeonsung.locate(md4, 810, 230)
byeonsung.show()

md4_timeline=Timer(0)
md4_timeline_count=0
def md4_timeline_next():
    global md4_animator
    global md4_timeline_count
    global on_event

    if md4_timeline_count==0:
        input_key(gangrim, 83)
        
    elif md4_timeline_count<=6:
        input_key(gangrim, 0)
        md4_message.show()
        md4_animator.stop()

    elif md4_timeline_count==7:
        input_key(leading_roll, 0)
        md4_message.show()
        md4_animator.stop()

    elif md4_timeline_count==8:
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            input_key(self, 83)

    elif md4_timeline_count==9:
        input_key(gangrim, 80)
        gangrim.state[2]=0
        md4_message.show()
        md4_animator.stop()

    elif md4_timeline_count==10:
        for self in [deoksoon, leading_roll, haewonmaek]:
            input_key(self, 0)
            self.shown=False
        showMessage("다음 장소로 이동해주세요.")
        on_event=False
        control(gangrim)
    md4_timeline_count+=1    
md4_timeline.onTimeout=md4_timeline_next

md4_animator.reserve(0, md4_timeline)
md4_animator.reserve(2, md4_timeline)
md4_animator.reserve(3, md4_timeline)
md4_animator.reserve(4, md4_timeline)
md4_animator.reserve(5, md4_timeline)
md4_animator.reserve(6, md4_timeline)
md4_animator.reserve(7, md4_timeline)
md4_animator.reserve(8, md4_timeline)
md4_animator.reserve(9, md4_timeline)
md4_animator.reserve(12, md4_timeline)
md4_animator.reserve(13, md4_timeline)


def md4_onEnter():
    global on_event

    character_enter(md4)
    if not md4.clear:
        on_event=True
        leading_roll.location[1]=690
        deoksoon.location[1]=350
        gangrim.location[1]=300
        haewonmaek.location[1]=250
        for self in [deoksoon, gangrim, leading_roll, haewonmaek]:
            self.location[0]=md4
            self.location[2]=50
            self.state[2]=1
            self.show()
        input_key(leading_roll, 85)
        md4_animator.start()
md4.self_set=md4_onEnter

startGame(intro)