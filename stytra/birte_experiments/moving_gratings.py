from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.visual import (
    MovingGratingStimulus2
)
from lightparam import Param
import pandas as pd
import numpy as np


class CombinedProtocol(Protocol):
    name = "moving_gratings"

    def __init__(self):

        super().__init__()

        self.grating_period_deg = Param(45, limits=(1.0, 360.0))  # degrees azimuth
        self.grating_velocity_deg_s = Param(90, limits=(0.0, 1000.0))  # degrees/s

    def get_stim_sequence(self):

        grating_period_deg = self.grating_period_deg
        grating_velocity_deg = self.grating_velocity_deg_s

        mm_px = 0.0825  # hardcoded for use with curved Royole screen (1920 x 1440)
        w = 1920
        grating_period_mm = grating_period_deg / 180 * w * mm_px
        velocity_mm = grating_velocity_deg / 180 * w * mm_px

        # Use six points to specify the velocity step to be interpolated:
        t = [0, 3, 3, 6, 6, 9, 9, 12, 12, 15]
        vel = np.array([0, 0, velocity_mm, velocity_mm, 0, 0, -velocity_mm, -velocity_mm, 0, 0])

        df = pd.DataFrame(dict(t=t, vel_x=vel))
        s_a = MovingGratingStimulus2(df_param=df, grating_angle=0, grating_period=grating_period_mm, wave_shape="square",
                                     clip_mask=[0, 0, 1, 1], grating_col_1=(150, 150, 150), grating_col_2=(50, 50, 50))

        stimuli = [s_a]
        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=CombinedProtocol())
