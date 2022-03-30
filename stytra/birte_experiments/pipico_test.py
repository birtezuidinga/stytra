from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.generic_stimuli import Stimulus
from stytra.stimulation.stimuli.visual import Pause
from lightparam import Param
import datetime

try:
   from stytra.hardware.USB_PI_PICO_36 import *
except ImportError:
   print("Raspberri PI pico connection failed")

REQUIRES_EXTERNAL_HARDWARE = True


class PiPicoCommStimulus(Stimulus):
    name = "pipico_comm_stimulus"

    def __init__(self, com_port="COM3", baudrate=76800, pin_value=0, **kwargs):
        self.pin_value = pin_value

        super().__init__(**kwargs)
        self.name = "opto_light"
        self._Pico = None
        self._com_port = com_port
        self._baudrate = baudrate
        self.real_time_start = None # adding start time to the stimulus logger
        # self.real_time_stop = None # adding stop time to stimulus logger

    def get_state(self):
        """Returns a dictionary with stimulus features for logging.
        Ignores the properties which are private (start with _)
        Parameters
        ----------
        Returns
        -------
        dict :
            dictionary with all the current parameters of the stimulus
        """
        state_dict = dict()
        for key, value in self.__dict__.items():
            if not callable(value) and key[0] != "_":
                state_dict[key] = value
        return state_dict

    def initialise_external(self, experiment):
        # Initialize serial connection and set it as experiment attribute to make
        # it available for other stimuli:
        try:
            self._Pico = getattr(experiment, "_Pico")
        except AttributeError:
            experiment._Pico = PiPico(self._com_port,self._baudrate)
            self._Pico = getattr(experiment, "_Pico")
            print(getattr(experiment, "_Pico"))

    def start(self):
        """ """
        if self.pin_value == 1:
            self._Pico.set_Pin(0)
            print("start")
        else:
            self._Pico.clear_Pin(0)
            print("start_clear")
        self.real_time_start = datetime.datetime.now() # getting starttime after pin is set

# also change names here
class PiPicoCommProtocol(Protocol):
    name = "pipico_comm_protocol"  # every protocol must have a name.

    def __init__(self):
        super().__init__()
        self.pre_duration = Param(10.0, limits=(0.0, 1000.0), unit="s")  #, loadable=False)
        self.opto_duration = Param(2.0, limits=(0.0, 1000.0), unit="s")  #, loadable=False)
        self.post_duration = Param(3.0, limits=(0.0, 1000.0), unit="s")  #, loadable=False)

    def get_stim_sequence(self):
        stimuli = []
        stimuli.append(Pause(duration=self.pre_duration))
        stimuli.append(PiPicoCommStimulus(pin_value=1, duration=self.opto_duration))
        stimuli.append(PiPicoCommStimulus(pin_value=0, duration=self.post_duration))

        return stimuli


if __name__ == "__main__":
    st = Stytra(protocol=PiPicoCommProtocol())
