import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # runner와 chaser 초기화
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # 점수 및 시간 표시용 터틀
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # 게임 시작 시간과 점수 초기화
        self.start_time = time.time()
        self.score = 0

        # 타이머 설정
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # runner가 잡혔는지 확인
        is_catched = self.is_catched()
        if not is_catched:
            self.score += 1  # runner가 살아남을 때마다 점수 증가

        # 경과 시간 계산
        elapsed_time = time.time() - self.start_time

        # 화면에 점수와 시간 표시
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'점수: {self.score}  경과 시간: {elapsed_time:.2f}초  잡혔나?: {is_catched}')

        # 게임 계속 진행
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # 키보드 이벤트 핸들러 등록
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class IntelligentMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        # 상대방 터틀의 위치를 추적하여 그 방향으로 이동
        runner_x, runner_y = opp_pos
        chaser_x, chaser_y = self.pos()
        angle_to_runner = self.towards(runner_x, runner_y)
        self.setheading(angle_to_runner)
        self.forward(self.step_move)

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # IntelligentMover가 chaser로 설정됨
    runner = ManualMover(screen)
    chaser = IntelligentMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
