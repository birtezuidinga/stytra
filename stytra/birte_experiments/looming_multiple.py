import numpy as np
import pandas as pd
import math

from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import InterpolatedStimulus, CurvedScreenMultipleCirclesStimulus, CombinerStimulus, TriggerSquare
from lightparam import Param


class LoomingMultipleStimulus(InterpolatedStimulus, CurvedScreenMultipleCirclesStimulus):
    name = "looming_multiple"


class CombinedMultipleLoomingTriggerPixel(Protocol):
    name = "looming_multiple_protocol"

    def __init__(self):

        super().__init__()

        self.x_pos = Param(0.5, limits=(0.0, 1.0))
        self.y_pos = Param(0.5, limits=(0.0, 1.0))
        self.ratio_lv = Param(100, limits=(1, 1000), unit="ms")
        self.max_loom_diameter = Param(180, limits=(1, 180))
        self.circle_background_contrast = Param(100, limits=(0, 255))
        self.circle_inner_contrast = Param(50, limits=(0, 255))
        self.looming_duration = Param(25, limits=(1, 1000.0), unit="s")
        self.single_or_multiple_circles = Param("multiple", limits=["single", "multiple"])
        self.inner_circles_velocity = Param("constant", limits=["constant", "faster", "slower"])
        self.constant_circles_interval = Param(10, limits=(0, 1000), unit="deg")
        self.faster_circles_start_interval = Param(10, limits=(0, 1000), unit="deg")
        self.faster_circles_end_interval = Param(5, limits=(0, 1000), unit="deg")
        self.slower_circles_slowing_rate = Param(0.5, limits=(0, 1))
        self.slower_circles_n = Param(200, limits=(1, 1000))

    def get_stim_sequence(self):
        start_trigger_duration = 2
        ratio_lv = self.ratio_lv
        looming_duration = self.looming_duration
        max_loom_diameter = self.max_loom_diameter
        circle_background_contrast = self.circle_background_contrast
        circle_inner_contrast = self.circle_inner_contrast

        stimuli = []

        # Looming stimulus
        time = np.arange(-looming_duration, 0, 0.0005)
        df = pd.DataFrame(dict(time_ms=time * 1000))
        df['angle'] = df.apply(lambda row: 2 * math.atan(-ratio_lv / row.time_ms) * (180 / np.pi), axis=1)
        df['include'] = df['angle'].apply(lambda x: 'True' if x <= max_loom_diameter else 'False')
        df_include = df.query("include == 'True'")
        df_include['radius'] = df_include['angle'] / 2
        radius_df = df_include.drop(columns=['include', 'angle']).rename(columns={'time_ms': 't'})
        radius_df['t'] = radius_df['t'] / 1000 + looming_duration + start_trigger_duration
        radius_df = radius_df.reset_index(drop=True)

        bc = 127.5 + circle_background_contrast/2
        cc1 = 127.5 - circle_background_contrast/2 - circle_inner_contrast/2
        cc2 = 127.5 - circle_background_contrast/2 + circle_inner_contrast/2
        cc3 = 127.5 - circle_background_contrast/2

        stimuli_loom = LoomingMultipleStimulus(
                background_color=(bc, bc, bc),
                circle_darkest_color=(cc1, cc1, cc1),
                circle_brightest_color=(cc2, cc2, cc2),
                circle_average_color=(cc3, cc3, cc3),
                df_param=radius_df,
                origin=(self.x_pos, self.y_pos),
                curved_screen=True,
                max_loom_diameter=self.max_loom_diameter,
                single_or_multiple_circles=self.single_or_multiple_circles,
                inner_circles_velocity=self.inner_circles_velocity,
                constant_circles_interval=self.constant_circles_interval,
                faster_circles_start_interval=self.faster_circles_start_interval,
                faster_circles_end_interval=self.faster_circles_end_interval,
                slower_circles_slowing_rate=self.slower_circles_slowing_rate,
                slower_circles_n=self.slower_circles_n,
            )

        # Trigger pixel
        last_t = radius_df.iloc[-1, 0]
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

        stimuli.append(CombinerStimulus([stimuli_loom, triggerpixel]))
        return stimuli


if __name__ == "__main__":
    # We make a new instance of Stytra with this protocol as the only option:
    s = Stytra(protocol=CombinedMultipleLoomingTriggerPixel())#, record_stim_framerate=30, stim_movie_format="mp4")
