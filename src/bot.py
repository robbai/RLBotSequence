import pathlib

from rlbot.agents.base_independent_agent import BaseIndependentAgent
from rlbot.botmanager.helper_process_request import HelperProcessRequest


class Agent(BaseIndependentAgent):
    def get_helper_process_request(self) -> HelperProcessRequest:
        controller_path = pathlib.Path(__file__).parent.joinpath("controller.py")
        options = {"index": self.index}
        return HelperProcessRequest(
            python_file_path=controller_path, key=self.name, options=options
        )

    def run_independently(self, terminate_request_event):
        pass
