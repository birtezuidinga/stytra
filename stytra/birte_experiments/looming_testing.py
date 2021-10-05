import numpy as np
import pandas as pd
import math

from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import InterpolatedStimulus, CalibratedCircleStimulus
from lightparam import Param


# A looming stimulus is an expanding circle. Stimuli which contain
# some kind of parameter change inherit from InterpolatedStimulus
# which allows for specifying the values of parameters of the
# stimulus at certain time points, with the intermediate
# values interpolated

# Use the 3-argument version of the Python type function to
# make a temporary class combining two classes


class LoomingStimulus(InterpolatedStimulus, CalibratedCircleStimulus):
    name = "looming_stimulus"


# Let's define a simple protocol consisting of looms at random locations,
# of random durations and maximal sizes

# First, we inherit from the Protocol class
class LoomingProtocol(Protocol):

    # We specify the name for the dropdown in the GUI
    name = "looming_protocol"
    # stytra_config = dict(
    #     camera=dict(type="spinnaker"), recording=dict(extension="mp4"), tracking=dict(method="tail"),
    #     dir_save=r'C:\Users\zuidinga\Data\20210916_Test')

    def __init__(self):
        super().__init__()

        # It is convenient for a protocol to be parametrized, so
        # we name the parameters we might want to change,
        # along with specifying the the default values.
        # This automatically creates a GUI to change them
        # (more elaborate ways of adding parameters are supported,
        # see the documentation of lightparam)

        # if you are not interested in parametrizing your
        # protocol the the whole __init__ definition
        # can be skipped

        self.n_looms = Param(10, limits=(0, 1000))
        self.max_loom_size = Param(60, limits=(0, 100))
        self.max_loom_duration = Param(5, limits=(0, 100))
        self.x_pos_pix = Param(79.20, limits=(0.0, 2000.0))
        self.y_pos_pix = Param(59.40, limits=(0.0, 2000.0))
        self.ratio_lm = Param(10, limits=(1, 500))

    # This is the only function we need to define for a custom protocol
    def get_stim_sequence(self):
        stimuli = []

        for i in range(self.n_looms):
            # The radius is only specified at the beginning and at the
            # end of expansion. More elaborate functional relationships
            # than linear can be implemented by specifying a more
            # detailed interpolation table

            # radius_df = pd.DataFrame(
            #     dict(
            #         t=[0, np.random.rand() * self.max_loom_duration],
            #         radius=[0, np.random.rand() * self.max_loom_size],
            #     )
            # )

            time = np.arange(-3.000, 0, 0.0005)
            df = pd.DataFrame(dict(time_ms=time * 1000))
            df['angle'] = df.apply(lambda row: 2 * math.atan(-self.ratio_lm / row.time_ms) * (180 / np.pi), axis=1)
            df['include'] = df['angle'].apply(lambda x: 'True' if 5 <= x <= 180 else 'False')
            df_include = df.query("include == 'True'")
            df_include['radius'] = df_include['angle'] / 2
            radius_df = df_include.drop(columns=['include', 'angle']).rename(columns={'time_ms': 't'})
            radius_df['t'] = radius_df['t'] / 1000 + 5
            radius_df['radius'] = radius_df['radius'] * (158.4 / 180)


            # We construct looming stimuli with the radius change specification
            # and a random point of origin within the projection area
            # (specified in fractions from 0 to 1 for each dimension)
            stimuli.append(
                LoomingStimulus(
                    background_color=(255, 255, 255),
                    circle_color=(0, 0, 0),
                    df_param=radius_df,
                    origin=(self.x_pos_pix, self.y_pos_pix),
                )
            )

        return stimuli

if __name__ == "__main__":
    # We make a new instance of Stytra with this protocol as the only option:
    s = Stytra(protocol=LoomingProtocol())#, display=dict(full_screen=True, window_size=(1920, 1440)))
