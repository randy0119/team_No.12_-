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
            gravity(self)

            if (self.control or on_event) and not self.on_attack:
                if self.key==83:
                    move_right(self)
                elif self.key==82:
                    move_left(self)
                elif self.key==84:   ##사다리타기
                    up(self)
                elif self.key==85:
                    prone(self)
                elif self.key==217:      ##공격
                    attack(self)
                elif self.key==219:      ##점프
                    jump(self)
                else:
                    stand(self)

            elif self.on_attack:
                attack(self)
            else:
                stand(self)

            if self.control==True:
                self.location[0].player_location[0]=self.location[1]
                self.location[0].player_location[1]=self.location[2]
                exam.set(self.location[1])##______________________test 추후 삭제 요망
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
            if self.location[0].portal(self.location[1], self.location[2]) and self.location[0].kill_count==self.location[0].kill_quest:
                target=self.location[0].portal(self.location[1], self.location[2])
                target.enter()
            elif False:
                pass        #사다리or로프
            else:
                self.state[0]=0
                self.state[3]=int(self.motion_count%20/5)

        def move_right(self):
            self.state[0]=1
            self.state[2]=1
            self.state[3]=int(self.motion_count%25/5)
            if self.location[1]+self.x_speed<1240:
                self.location[1]+=self.x_speed
                if self.on_jump==False:
                    self.location[2]=self.location[0].ground(self.location[1], self.location[2])

        def move_left(self):
            self.state[0]=1
            self.state[2]=0
            self.state[3]=int(self.motion_count%25/5)
            if self.location[1]-self.x_speed>0:
                self.location[1]-=self.x_speed
                if self.on_jump==False:
                    self.location[2]=self.location[0].ground(self.location[1], self.location[2])

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
        super().onEnter()

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
        self.state[0]=0
        self.state[1]=1
        self.state[2]=int(self.motion_count%30/5)
        if self.location[1]+self.x_speed<self.right_limit:
            self.location[1]+=self.x_speed

    def move_left(self):
        self.state[0]=0
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

leading_roll=Character(leading_roll_file_set, hellgate_1, 200, 135, 0, 0, 0, True, True)
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
        input_key(leading_roll, 85)
hellgate_1.onEnter=hellgate_1_onEnter

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
hellgate_2.onEnter=hellgate_2_onEnter
###________________________________________________________________________________________지옥문2/천륜지옥1
stormfox_file_set=[[['몹/돌풍여우/디폴트/좌/Frame0.png', '몹/돌풍여우/디폴트/좌/Frame1.png', '몹/돌풍여우/디폴트/좌/Frame2.png', '몹/돌풍여우/디폴트/좌/Frame3.png', '몹/돌풍여우/디폴트/좌/Frame4.png', '몹/돌풍여우/디폴트/좌/Frame5.png'],['몹/돌풍여우/디폴트/우/Frame0.png', '몹/돌풍여우/디폴트/우/Frame1.png', '몹/돌풍여우/디폴트/우/Frame2.png', '몹/돌풍여우/디폴트/우/Frame3.png', '몹/돌풍여우/디폴트/우/Frame4.png', '몹/돌풍여우/디폴트/우/Frame5.png']],[['몹/돌풍여우/맞음/좌/hit.png'],['몹/돌풍여우/맞음/우/hit.png']],[['몹/돌풍여우/죽음/좌/die0.png','몹/돌풍여우/죽음/좌/die1.png','몹/돌풍여우/죽음/좌/die2.png','몹/돌풍여우/죽음/좌/die3.png','몹/돌풍여우/죽음/좌/die4.png','몹/돌풍여우/죽음/좌/die5.png','몹/돌풍여우/죽음/좌/die6.png','몹/돌풍여우/죽음/좌/die7.png','몹/돌풍여우/죽음/좌/die8.png','몹/돌풍여우/죽음/좌/die9.png'],['몹/돌풍여우/죽음/우/die0.png','몹/돌풍여우/죽음/우/die1.png','몹/돌풍여우/죽음/우/die2.png','몹/돌풍여우/죽음/우/die3.png','몹/돌풍여우/죽음/우/die4.png','몹/돌풍여우/죽음/우/die5.png','몹/돌풍여우/죽음/우/die6.png','몹/돌풍여우/죽음/우/die7.png','몹/돌풍여우/죽음/우/die8.png','몹/돌풍여우/죽음/우/die9.png']]]

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
cheonryun_1.onEnter=cr1_onEnter

###________________________________________________________________________________________천륜지옥1/천륜지옥2

def cheonryun_ground_2(x, y):
    return 50

cheonryun_2=Stage("천륜지옥", "천륜지옥/스테이지1.png", cheonryun_ground_2, 1090, 30, 60, 30)
cheonryun_1.next_scene=cheonryun_2
cheonryun_2.before_scene=cheonryun_1
cheonryun_animator_2=Animator(cheonryun_2)

###________________________________________________________________________________________천륜지옥2/천륜지옥3

def cheonryun_ground_3(x, y):
    return 50

cheonryun_3=Stage("천륜지옥", "천륜지옥/스테이지2.png", cheonryun_ground_3, 1090, 30, 60, 30)
cheonryun_2.next_scene=cheonryun_3
cheonryun_3.before_scene=cheonryun_2
cheonryun_animator_3=Animator(cheonryun_3)

###________________________________________________________________________________________천륜지옥3/천륜지옥4

def cheonryun_ground_4(x, y):
    return 50

cheonryun_4=Stage("천륜지옥", "천륜지옥/스테이지3.png", cheonryun_ground_4, 1090, 30, 60, 30)
cheonryun_3.next_scene=cheonryun_4
cheonryun_4.before_scene=cheonryun_3
cheonryun_animator_4=Animator(cheonryun_4)

###________________________________________________________________________________________천륜지옥4/천륜지옥5

def cheonryun_ground_5(x, y):
    return 50

cheonryun_5=Stage("천륜지옥", "천륜지옥/스테이지4.png", cheonryun_ground_4, 1090, 30, 60, 30)
cheonryun_4.next_scene=cheonryun_5
cheonryun_5.before_scene=cheonryun_4
cheonryun_animator_5=Animator(cheonryun_5)

###________________________________________________________________________________________천륜지옥5/천륜지옥6

def cheonryun_ground_6(x, y):
    return 50

cheonryun_6=Stage("천륜지옥", "천륜지옥/배경1.png", cheonryun_ground_5, 1090, 30, 60, 30)
cheonryun_5.next_scene=cheonryun_6
cheonryun_6.before_scene=cheonryun_5
cheonryun_animator_6=Animator(cheonryun_6)

startGame(cheonryun_1)