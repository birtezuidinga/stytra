import numpy as np
import pandas as pd
from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import SeamlessImageStimulus, InterpolatedStimulus
import qimage2ndarray
from lightparam import Param


def create_pattern(side_len=1000, wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0)):
    x = (np.arange(side_len) - side_len / 2) / side_len
    xx, yy = np.meshgrid(x, x)  # grid of points
    W = np.cos(xx * 6 * 2 * np.pi)
    W = ((W + 1) / 2)[:, :, np.newaxis]  # normalize and add color axis

    if wave_shape == "square":
        W = (W > 0.5).astype(np.uint8)  # binarize for square gratings

    # Multiply by color:
    _pattern = W * color_1 + (1 - W) * color_2
    _qbackground = qimage2ndarray.array2qimage(_pattern)
    _qbackground.save("assets/generated_pattern.png")


class MovingTiledGrating(Protocol):
    name = "moving_sine_grating_tiled_protocol"

    def __init__(self):
        super().__init__()
        create_pattern(side_len=1000, wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0))

    def get_stim_sequence(self):
        Stim = type("stim", (SeamlessImageStimulus, InterpolatedStimulus), {})

        return [
            Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 10], vel_x=[10, 10], vel_y=[0, 0])),
                rotation=30)]


if __name__ == "__main__":
    s = Stytra(protocol=MovingTiledGrating())
