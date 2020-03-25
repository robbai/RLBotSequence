import pathlib
import math

from rlbot.agents.base_agent import BaseAgent
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import (
    GameState,
    BallState,
    CarState,
    Physics,
    Vector3,
    Rotator,
)


def parse(val):
    try:
        return float(val)
    except:
        return val == "True"


class Playback(BaseAgent):
    def initialize_agent(self):
        file_name = "recordings/1585179356.txt"

        file_path = pathlib.Path(__file__).parent.joinpath(file_name)
        self.recording = [
            [parse(val) for val in line.strip().split(":")]
            for line in open(file_path, "r").readlines()
        ]
        self.time_started = 0

        self.delay = 0.5
        self.last_i = -1

    def get_output(self, packet: GameTickPacket):
        current_time = packet.game_info.seconds_elapsed % (
            self.delay + self.recording[-1][0]
        )
        if current_time < self.delay:
            if current_time < self.delay / 10:
                car_state = CarState(
                    boost_amount=100,
                    physics=Physics(
                        location=Vector3(0, -4500, 18),
                        velocity=Vector3(0, 0, -100),
                        rotation=Rotator(0, math.pi / 2, 0),
                        angular_velocity=Vector3(0, 0, 0),
                    ),
                )
                ball_state = BallState(
                    Physics(
                        location=Vector3(0, 4500, 92.75),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0),
                    )
                )
                game_state = GameState(ball=ball_state, cars={self.index: car_state})
                self.set_game_state(game_state)
            self.last_i = -1
            return self.convert_output_to_v4([0] * 8)

        self.renderer.begin_rendering()
        self.renderer.draw_string_2d(
            20,
            20,
            4,
            4,
            str(round(current_time - self.delay, 3)),
            self.renderer.white(),
        )
        self.renderer.end_rendering()

        current_time -= self.delay
        for i, data in enumerate(self.recording[1:]):
            if data[0] > current_time:
                record = self.recording[i][1:]
                controls = self.convert_output_to_v4(record)
                return controls
        return self.convert_output_to_v4([0] * 8)
