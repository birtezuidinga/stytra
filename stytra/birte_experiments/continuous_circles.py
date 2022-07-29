import numpy as np
import pandas as pd
import math

from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import InterpolatedStimulus, ContinuousCirclesStimulus, CombinerStimulus, TriggerSquare
from lightparam import Param


class ContinuousMovingCirclesStimulus(InterpolatedStimulus, ContinuousCirclesStimulus):
    name = "continuous_circles"


class ContinuousCirclesTriggerPixel(Protocol):
    name = "continuous_circles_protocol"

    def __init__(self):

        super().__init__()

        self.x_pos = Param(0.5, limits=(0.0, 1.0))
        self.y_pos = Param(0.5, limits=(0.0, 1.0))
        self.expansion_velocity = Param(60, limits=(-1000, 1000), unit="deg/s")
        self.period = Param(90, limits=(1,1000), unit="deg")
        self.circles_n = Param(200, limits=(1, 1000))
        self.contrast = Param(100, limits=(0, 255))
        self.duration = Param(25, limits=(1, 1000.0), unit="s")
        self.wave_type = Param("sine", limits=["sine", "square"])

    def get_stim_sequence(self):
        start_trigger_duration = 2
        duration = self.duration
        velocity = self.expansion_velocity

        stimuli = []

        # Circles stimulus
        time = start_trigger_duration + duration

        last_t = time
        expansion_velocity = pd.DataFrame(
            dict(
                t=[0, start_trigger_duration, start_trigger_duration, last_t, last_t, last_t + 4],
                expansion_velocity=[0, 0, velocity, velocity, 0, 0]))

        stimulus_circles = ContinuousMovingCirclesStimulus(
            df_param=expansion_velocity,
            contrast=self.contrast,
            period=self.period,
            wave_type=self.wave_type,
            origin=(self.x_pos, self.y_pos),
            circles_n=self.circles_n,
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
    s = Stytra(protocol=ContinuousCirclesTriggerPixel())#, record_stim_framerate=30, stim_movie_format="mp4")
