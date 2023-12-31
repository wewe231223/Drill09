# 이것은 각 상태들을 객체로 구현한 것임.


# 2020182009 김승범 Drill09

from pico2d import load_image, SDL_KEYDOWN, SDLK_SPACE, get_time, SDLK_a, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP , delay
import math
import random

def space_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == "TIME_OUT"

def a_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_a

def right_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT
def left_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT
def right_up(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT
def left_up(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.wait_time = 0
        self.dx = 0
        self.dir = 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(event)

    def draw(self):
        self.state_machine.draw()


class Idle:

    @staticmethod
    def enter(b_: Boy):
        b_.action = 3
        b_.dir = 0
        b_.frame = 0
        b_.wait_time = get_time()
        print('Idle Enter')

    @staticmethod
    def exit(b_: Boy):
        print('Idle Exit')

    @staticmethod
    def do(b_: Boy):
        b_.frame = (b_.frame + 1) % 8
        if get_time() - b_.wait_time > 2:
            b_.state_machine.handle_event(("TIME_OUT",0))
        print('Idle Do')

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_draw(boy_.frame * 100, boy_.action * 100, 100, 100, boy_.x, boy_.y)
        pass


class Sleep:

    @staticmethod
    def enter(b_: Boy):
        b_.action = 3
        pass

    @staticmethod
    def exit(b_: Boy):
        pass

    @staticmethod
    def do(b_: Boy):
        b_.frame = (b_.frame + 1) % 8

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_composite_draw(boy_.frame * 100, 300 , 100, 100, math.pi / 2, '', boy_.x - 25, boy_.y - 25, 100, 100)
        pass

class Autorun:

    @staticmethod
    def enter(b_: Boy):
        print("Run enter")
        b_.action = 1
        b_.dx = random.randint(20,30)
        b_.dir = 1
        b_.wait_time = get_time()

        pass

    @staticmethod
    def exit(b_: Boy):

        pass

    @staticmethod
    def do(b_: Boy):

        if get_time() - b_.wait_time > 5:
            b_.state_machine.handle_event(("TIME_OUT",0))


        b_.frame = (b_.frame + 1) % 8

        if b_.x >= 800:
            b_.action = 0
            b_.dir = -1
        elif b_.x <= 0:
            b_.action = 1
            b_.dir = 1

        b_.x += b_.dx * b_.dir

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_draw(boy_.frame * 100, boy_.action * 100 , 100, 100, boy_.x, boy_.y * 1.4, 200, 200)
        pass
class Leftrun:

    @staticmethod
    def enter(b_: Boy):
        print("Run enter")
        b_.action = 0
        b_.dx = 10
        b_.dir = -1

        pass

    @staticmethod
    def exit(b_: Boy):

        pass

    @staticmethod
    def do(b_: Boy):



        b_.frame = (b_.frame + 1) % 8
        b_.x += b_.dx * b_.dir

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_draw(boy_.frame * 100, boy_.action * 100 , 100, 100, boy_.x, boy_.y , 100, 100)
        pass
class Rightrun:

    @staticmethod
    def enter(b_: Boy):
        print("Run enter")
        b_.action = 1
        b_.dx = 10
        b_.dir = 1


        pass

    @staticmethod
    def exit(b_: Boy):

        pass

    @staticmethod
    def do(b_: Boy):

        b_.frame = (b_.frame + 1) % 8
        b_.x += b_.dx * b_.dir

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_draw(boy_.frame * 100, boy_.action * 100 , 100, 100, boy_.x, boy_.y, 100, 100)
        pass


class StateMachine:
    def __init__(self, b: Boy):
        self.cur_state = Sleep
        self.boy = b
        self.transitions = {
            Sleep: {space_down : Idle},
            Idle : {time_out : Sleep, a_down : Autorun, right_down : Rightrun, left_down : Leftrun},
            Rightrun : {right_up : Idle},
            Leftrun : {left_up : Idle},
            Autorun : {time_out : Idle, right_down : Rightrun, left_down : Leftrun}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.enter(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)
        delay(0.028)
