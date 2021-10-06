from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.visual import (
    CombinerStimulus,
    MovingGratingStimulus,
    MovingGratingStimulus2
)
import pandas as pd
import numpy as np


class CombinedProtocol(Protocol):
    name = "bilateral_moving_gratings"

    def get_stim_sequence(self):
        # This is the
        # Use six points to specify the velocity step to be interpolated:
        t = [0, 1, 1, 6, 6, 7]
        vel = np.array([0, 0, 10, 10, 0, 0])

        df = pd.DataFrame(dict(t=t, vel_x=vel))

        s_a = MovingGratingStimulus2(df_param=df, grating_angle=np.pi, grating_period=20, wave_shape="sine", clip_mask=[0, 0, 0.5, 1])

        df = pd.DataFrame(dict(t=t, vel_x=-vel))
        s_b = MovingGratingStimulus2(df_param=df, grating_angle=np.pi, wave_shape="sine", clip_mask=[0.5, 0, 0.5, 1])

        stimuli = [CombinerStimulus([s_a, s_b])]
        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=CombinedProtocol())
