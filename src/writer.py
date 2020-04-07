from glob import iglob

from recorder_process import controls_attributes
from playback import read


if __name__ == "__main__":
    recording_folder = "recordings/"

    recording_files = (
        path.replace("\\", "/") for path in iglob(recording_folder + "*.obj")
    )

    for recording_file in recording_files:
        recording = read(recording_file)
        file = open(recording_file[:-3] + "py", "w")

        # Write.
        file.write("from typing import Optional\n\n")
        file.write("from rlbot.agents.base_agent import SimpleControllerState\n\n\n")
        file.write("class " + recording_file[len(recording_folder) : -4] + ":\n")
        file.write("    def __init__(self):\n")
        file.write("        self.timer: float = 0.0\n")
        file.write("        self.finished: bool = False\n")
        file.write("        self.controls: Optional[SimpleControllerState] = None\n\n")
        file.write("    def step(self, dt: float):\n")
        for i, record in enumerate(recording):
            controls_line = (
                "            self.controls = SimpleControllerState("
                + ", ".join(
                    (
                        attribute + "=" + str(getattr(record[1], attribute))
                        for attribute in controls_attributes
                    )
                )
                + ")\n"
            )
            if i == 0:
                file.write("        if self.timer == " + str(record[0]) + ":\n")
                file.write(controls_line)
            elif i + 1 != len(recording):
                file.write("        elif self.timer <= " + str(record[0]) + ":\n")
                file.write(controls_line)
            else:
                file.write("        else:\n")
                file.write(controls_line)
                file.write(
                    "            self.finished = self.timer > "
                    + str(record[0])
                    + "\n\n"
                )
        file.write("        self.timer += dt\n")

        file.close()
