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
        self.display_width_px = Param(960, limits=(10, 5000))
        self.wave_shape = Param("sine", limits=["sine", "square"])
        self.contrast = Param(100, limits=(0, 255))
        self.velocity = Param(20, limits=(-1000, 1000))

    def get_stim_sequence(self):
        display_width_px = self.display_width_px
        shape = self.wave_shape
        contrast = self.contrast
        vel = self.velocity

        c1 = 127.5 + contrast / 2
        c2 = 127.5 - contrast / 2

        Stim = type("stim", (SeamlessImageStimulus, InterpolatedStimulus), {})

        create_pattern(side_len=display_width_px, wave_shape=shape, color_1=(c1, c1, c1), color_2=(c2, c2, c2),
                       path="assets/generated_pattern.png")

        s_a = Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 30], vel_x=[vel, vel], vel_y=[0, 0])),
                clip_mask=[0, 0, 0.5, 1],
                rotation=np.pi)

        s_b = Stim(
                background="generated_pattern.png",
                df_param=pd.DataFrame(dict(t=[0, 30], vel_x=[vel, vel], vel_y=[0, 0])),
                clip_mask=[0.5, 0, 0.5, 1],
                rotation=0)

        stimuli = [CombinerStimulus([s_a, s_b])]
        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=CombinedMovingTiledGrating())

