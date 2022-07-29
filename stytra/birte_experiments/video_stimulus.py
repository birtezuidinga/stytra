from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.visual import (
    VideoStimulus
)
import pandas as pd
import numpy as np


class VideoProtocol(Protocol):
    name = "video_stimulus"

    def __init__(self):

        super().__init__()

    def get_stim_sequence(self):
        stimuli = []
        path = '131729_stim_movie.mp4'
        stimuli.append(VideoStimulus(video_path=path, framerate=9, duration=16))

        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=VideoProtocol())
