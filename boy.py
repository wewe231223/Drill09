# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, SDL_KEYDOWN, SDLK_SPACE, get_time, SDLK_a
import math
import random

def space_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == "TIME_OUT"

def a_down(event):
    return event[0] == "INPUT" and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_a



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
        b_.action = 0
        b_.dx = random.randint(5,20)
        pass

    @staticmethod
    def exit(b_: Boy):

        pass

    @staticmethod
    def do(b_: Boy):
        b_.frame = (b_.frame + 1) % 8
        b_.x += b_.dx

    @staticmethod
    def draw(boy_: Boy):
        boy_.image.clip_composite_draw(boy_.frame * 100, boy_.action * 100 , 100, 100, 0, 'h', boy_.x, boy_.y * 1.4, 200, 200)
        pass


class StateMachine:
    def __init__(self, b: Boy):
        self.cur_state = Sleep
        self.boy = b
        self.transitions = {
            Sleep: {a_down: Autorun , space_down : Idle},


            Idle : {time_out : Sleep},

            Autorun : {time_out : Sleep}
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
