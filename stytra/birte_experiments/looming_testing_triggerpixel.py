import numpy as np
import pandas as pd
import math

from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import InterpolatedStimulus, CalibratedCircleStimulus, CombinerStimulus, TriggerSquare
from lightparam import Param


class LoomingStimulus(InterpolatedStimulus, CalibratedCircleStimulus):
    name = "looming_stimulus"


class CombinedLoomingTriggerPixel(Protocol):
    name = "combined_looming_triggerpixel_protocol"

    def __init__(self):

        super().__init__()

        self.x_pos_pix = Param(79.20, limits=(0.0, 2000.0))
        self.y_pos_pix = Param(59.40, limits=(0.0, 2000.0))
        self.ratio_lv = Param(10, limits=(1, 500))
        self.min_contrast = Param(50, limits=(1, 255))
        self.max_contrast = Param(100, limits=(1, 255))
        self.n_contrasts = Param(4, limits=(2, 100))

    def get_stim_sequence(self):
        stimuli = []
        contrast_step = (self.max_contrast - self.min_contrast) / (self.n_contrasts - 1)

        contrasts = np.arange(self.min_contrast, self.max_contrast + contrast_step, contrast_step)

        # Looming stimulus
        for contrast in contrasts:
            time = np.arange(-25.000, 0, 0.0005)
            df = pd.DataFrame(dict(time_ms=time * 1000))
            df['angle'] = df.apply(lambda row: 2 * math.atan(-self.ratio_lv / row.time_ms) * (180 / np.pi), axis=1)
            df['include'] = df['angle'].apply(lambda x: 'True' if 5 <= x <= 180 else 'False')
            df_include = df.query("include == 'True'")
            df_include['radius'] = df_include['angle'] / 2
            radius_df = df_include.drop(columns=['include', 'angle']).rename(columns={'time_ms': 't'})
            radius_df['t'] = radius_df['t'] / 1000 + 27
            radius_df = radius_df.reset_index(drop=True)

            bc = 127.5 + contrast/2
            cc = 127.5 - contrast/2

            stimuli_loom = LoomingStimulus(
                    background_color=(bc, bc, bc),
                    circle_color=(cc, cc, cc),
                    df_param=radius_df,
                    origin=(self.x_pos_pix, self.y_pos_pix),
                    curved_screen=True
                )

            # Trigger pixel
            last_looming_t = radius_df.iloc[-1, 0]
            active_df = pd.DataFrame(
                dict(
                    t=[0, 1, 1, 1.03, 1.03, 1.06, 1.06, 1.09, 1.09, 1.12, 1.12, 1.15, 1.15, 2,
                       last_looming_t + 1, last_looming_t + 1, last_looming_t + 1.04, last_looming_t + 1.04,
                       last_looming_t + 1.08, last_looming_t + 1.08, last_looming_t + 1.12, last_looming_t + 1.12,
                       last_looming_t + 2],
                    active=[False, False, True, True, False, False, True, True, False, False, True, True, False, False,
                            False, True, True, False, False, True, True, False, False]
                )
            )

            triggerpixel = TriggerSquare(df_param=active_df)

            stimuli.append(CombinerStimulus([stimuli_loom, triggerpixel]))

        return stimuli


if __name__ == "__main__":
    # We make a new instance of Stytra with this protocol as the only option:
    s = Stytra(protocol=CombinedLoomingTriggerPixel())
