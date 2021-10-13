import numpy as np
import pandas as pd
from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import SeamlessImageStimulus, InterpolatedStimulus, CombinerStimulus
import qimage2ndarray
from lightparam import Param


def create_pattern(side_len=1000, wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0), path="generated_pattern.png"):
    x = (np.arange(side_len) - side_len / 2) / side_len
    xx, yy = np.meshgrid(x, x)  # grid of points
    W = np.sin(xx * 4 * 2 * np.pi)
    W = ((W + 1) / 2)[:, :, np.newaxis]  # normalize and add color axis

    if wave_shape == "square":
        W = (W > 0.5).astype(np.uint8)  # binarize for square gratings

    # Multiply by color:
    _pattern = W * color_1 + (1 - W) * color_2

    _qbackground = qimage2ndarray.array2qimage(_pattern)
    _qbackground.save(path)


class CombinedMovingTiledGrating(Protocol):
    name = "bilateral_tiled_moving_gratings"

    def __init__(self):
        super().__init__()
        # create_pattern(side_len=1000, wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0))

    def get_stim_sequence(self):
        Stim = type("stim", (SeamlessImageStimulus, InterpolatedStimulus), {})

        create_pattern(side_len=960, wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0), path="assets/generated_pattern.png")
        s_a = Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 10], vel_x=[10, 10], vel_y=[0, 0])),
                clip_mask=[0, 0, 0.5, 1],
                rotation=np.pi)

        s_b = Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 10], vel_x=[10, 10], vel_y=[0, 0])),
                clip_mask=[0.5, 0, 0.5, 1],
                rotation=0)

        stimuli = [CombinerStimulus([s_a, s_b])]
        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=CombinedMovingTiledGrating())

