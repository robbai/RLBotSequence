import pathlib
import pickle
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


class Playback(BaseAgent):
    def initialize_agent(self):
        self.recording = Playback.read("recordings/bdkawwendm.obj")

        self.time_started = 0

        self.delay = 0.5

    def get_output(self, packet: GameTickPacket):
        current_time = packet.game_info.seconds_elapsed % (
            self.delay + self.recording[-1][0]
        )

        # State-set and wait.
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
            return self.convert_output_to_v4([0] * 8)

        current_time -= self.delay

        # Render.
        self.renderer.begin_rendering()
        self.renderer.draw_string_2d(
            20, 20, 4, 4, str(round(current_time, 3)), self.renderer.white(),
        )
        self.renderer.end_rendering()

        # Controls.
        return self.find_controls(current_time)

    def find_controls(self, current_time: float):
        low, high = 0, len(self.recording) - 1
        while low < high:
            mid = (low + high) // 2 + 1
            if self.recording[mid][0] > current_time:
                high = mid - 1
            else:
                low = mid
        return self.recording[low][1]

    @staticmethod
    def read(file_name: str):
        file_path = pathlib.Path(__file__).parent.joinpath(file_name)
        file_handler = open(file_path, "rb")
        recording = pickle.load(file_handler)
        file_handler.close()
        return recording
