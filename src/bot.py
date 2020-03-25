import pathlib

from rlbot.agents.base_agent import BaseAgent
from rlbot.botmanager.helper_process_request import HelperProcessRequest


class Agent(BaseAgent):
    def get_helper_process_request(self) -> HelperProcessRequest:
        controller_path = pathlib.Path(__file__).parent.joinpath("controller.py")
        return HelperProcessRequest(python_file_path=controller_path, key="controller")
