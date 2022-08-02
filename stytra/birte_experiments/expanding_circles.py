import pandas as pd
from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import InterpolatedStimulus, RadialSineExpansionStimulus, CombinerStimulus, TriggerSquare
from lightparam import Param


class ExpandingCirclesStimulus(InterpolatedStimulus, RadialSineExpansionStimulus):
    name = "expanding_circles_stimulus"


class CombinedExpandingCirclesTriggerPixel(Protocol):
    name = "combined_expanding_circles_triggerpixel_protocol"

    def __init__(self):

        super().__init__()

        self.x_pos = Param(0.5, limits=(0.0, 1.0))
        self.y_pos = Param(0.5, limits=(0.0, 1.0))
        self.velocity = Param(30, limits=(-1000, 1000), unit="deg/s")
        self.contrast = Param(50, limits=(0, 255))
        self.duration = Param(10, limits=(1, 1000.0), unit="s")
        self.period = Param(8, limits=(1, 1000), unit="deg")
        self.wave_type = Param("sine", limits=["sine", "square"])
        self.x_pos = Param(0.5, limits=(0.0, 1.0))
        self.y_pos = Param(0.5, limits=(0.0, 1.0))

    def get_stim_sequence(self):
        start_trigger_duration = 2
        velocity = self.velocity
        duration = self.duration

        stimuli = []

        # Looming stimulus
        time = start_trigger_duration + duration

        last_t = time
        velocity_circles = pd.DataFrame(
            dict(
                t=[0, start_trigger_duration, start_trigger_duration, last_t, last_t, last_t + 4],
                velocity=[0, 0, velocity, velocity, 0, 0]))

        stimulus_circles = ExpandingCirclesStimulus(
                contrast=self.contrast,
                df_param=velocity_circles,
                period=self.period,
                wave_type=self.wave_type,
                origin=(self.x_pos, self.y_pos),
            )

        # Trigger pixel
        active_df = pd.DataFrame(
            dict(
                t=[0, 1, 1, 1.2, 1.2, 1.3, 1.3, 1.5, 1.5, 1.6, 1.6, 1.8, 1.8, start_trigger_duration,
                   last_t + 3, last_t + 3, last_t + 3.2, last_t + 3.2,
                   last_t + 3.3, last_t + 3.3, last_t + 3.5, last_t + 3.5, last_t + 4],
                active=[False, False, True, True, False, False, True, True, False, False, True, True, False, False,
                        False, True, True, False, False, True, True, False, False]
            )
        )

        triggerpixel = TriggerSquare(df_param=active_df)

        stimuli.append(CombinerStimulus([stimulus_circles, triggerpixel]))
        return stimuli


if __name__ == "__main__":
    # We make a new instance of Stytra with this protocol as the only option:
    s = Stytra(protocol=CombinedExpandingCirclesTriggerPixel())
