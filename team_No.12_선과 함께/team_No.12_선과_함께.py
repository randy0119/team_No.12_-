from bangtal import *
import keyboard as kb
from animator import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

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
    intro_title.setImage(title[title_count])
    intro_title.show()
title_clk.onTimeout=title_change

intro_animator=Animator(intro)
intro_animator.fade_out(1, 2)
intro_animator.reserve(3, title_clk)
intro_animator.fade_out(4, 2)
intro_animator.reserve(6, title_clk)
intro_animator.fade_out(7, 2)
intro_animator.reserve(9, title_clk)
intro_animator.fade_out(10, 2)

def intro_onEnter():
    intro_animator.start()
intro.onEnter=intro_onEnter

def intro_onLeave():
    intro_animator.stop()
intro.onLeave=intro_onLeave

startGame(intro)