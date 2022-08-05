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
        path = 'test3.mp4'
        stimuli.append(VideoStimulus(video_path=path, framerate=50, duration=10))

        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=VideoProtocol())
