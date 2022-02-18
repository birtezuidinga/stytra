from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.opto_LED import WritePiPicoPin
from lightparam import Param
import pandas as pd

REQUIRES_EXTERNAL_HARDWARE = True


class PiPicoProtocol(Protocol):
    name = "pipico_protocol"

    def __init__(self):
        super(PiPicoProtocol, self).__init__()
        self.pre_duration = Param(3.0, limits=(0.0, 1000.0))
        self.opto_duration = Param(1.0, limits=(0.0, 1000.0))
        self.post_duration = Param(3.0, limits=(0.0, 1000.0))

    def get_stim_sequence(self):

        stimuli = [
            #WritePiPicoPin(pin_value=0, duration=self.pre_duration),
            WritePiPicoPin(pin_value=1, duration=self.opto_duration),
            #WritePiPicoPin(pin_value=0, duration=self.post_duration),
        ]
        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=PiPicoProtocol())
