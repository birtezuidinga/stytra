from stytra import Stytra, Protocol
from stytra.stimulation.stimuli.generic_stimuli import Stimulus
from stytra.stimulation.stimuli.visual import Pause
from stytra.hardware.serial import SerialConnection
from lightparam import Param

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
        self._Pico = None
        self.com_port = com_port
        self.baudrate = baudrate

    def initialise_external(self, experiment):
        # Initialize serial connection and set it as experiment attribute to make
        # it available for other stimuli:
        try:
            self._Pico = getattr(experiment, "_Pico")
        except AttributeError:
            experiment._Pico = PiPico(self.com_port,self.baudrate)
            self._Pico = getattr(experiment, "_Pico")
            print(getattr(experiment, "_Pico"))

    def start(self):
        """ """
        # we have to use the Pin value to decide if set or clear has to be done
        # self._pyb.write("b")  # send blinking command at stimulus start
        if self.pin_value == 1:
            print(self._Pico)
            self._Pico.set_Pin(0)
        else:
            self._Pico.clear_Pin(0)

    def update(self):
        super().update()
        if self.pin_value == 1:
            print(self._Pico)
            self._Pico.set_Pin(0)
        else:
            self._Pico.clear_Pin(0)


# also change names here
class PiPicoCommProtocol(Protocol):
    name = "pipico_comm_protocol"  # every protocol must have a name.

    def __init__(self):
        super().__init__()
        self.pre_duration = Param(3.0, limits=(0.0, 1000.0))
        self.opto_duration = Param(1.0, limits=(0.0, 1000.0))
        self.post_duration = Param(3.0, limits=(0.0, 1000.0))

    def get_stim_sequence(self):
        # stimuli = PiPicoCommStimulus(pin_value=1, duration=self.opto_duration)
        stimuli = []
        stimuli.append(Pause(duration=4))
        stimuli.append(PiPicoCommStimulus(pin_value=1, duration=5))
        stimuli.append(PiPicoCommStimulus(pin_value=0, duration=5))

        return stimuli
# i think that they call here  ArduinoCommStimulus one time to write "b" in our case we have to give here a value
# to the function which allows us to set or clear the pin stimuli.append(ArduinoCommStimulus(duration=0, pin_value = 1)) or
# to make a second class which then clears the pin


if __name__ == "__main__":
    st = Stytra(protocol=PiPicoCommProtocol())
