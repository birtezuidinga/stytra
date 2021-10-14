import numpy as np
import pandas as pd
from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import SeamlessImageStimulus, InterpolatedStimulus
import qimage2ndarray
from lightparam import Param


def create_pattern(side_len, grating_period, grating_period_unit="degree", wave_shape="sine", color_1=(255, 255, 255), color_2=(0, 0, 0)):

    grating_period_px = 0
    if grating_period_unit == "degree":
        grating_period_mm = grating_period / 180 * (side_len * 0.165)  # 0.165 = mm_px
        grating_period_px = grating_period_mm / 0.165
    elif grating_period_unit == "px":
        grating_period_px = grating_period
    elif grating_period_unit == "mm":
        grating_period_px = grating_period / 0.165

    screen_width_px = 960
    n_periods = np.ceil(screen_width_px / grating_period_px)

    new_side_len = n_periods * grating_period_px
    print(new_side_len)
    x = (np.arange(new_side_len) - new_side_len / 2) / new_side_len
    xx, yy = np.meshgrid(x, x)  # grid of points
    W = np.sin(xx * n_periods * 2 * np.pi)
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
        create_pattern(side_len=960, grating_period=50, grating_period_unit="mm", wave_shape="square", color_1=(255, 255, 255), color_2=(0, 0, 0))

    def get_stim_sequence(self):
        Stim = type("stim", (SeamlessImageStimulus, InterpolatedStimulus), {})

        return [
            Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 10], vel_x=[10, 10], vel_y=[0, 0])),
                rotation=0)]


if __name__ == "__main__":
    s = Stytra(protocol=MovingTiledGrating())
