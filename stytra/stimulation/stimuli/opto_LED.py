from stytra.stimulation.stimuli import Stimulus, InterpolatedStimulus

try:
    from stytra.hardware.USB_PI_PICO_36 import *
except ImportError:
    print("Raspberri PI pico connection failed")


class WritePiPicoPin(Stimulus):
    """Simple class to write a value on an arduino pin. Mostly a simple example to implement
    your own fancy arduino classes.

    Parameters
    ----------
    pin : int
        Pin number.
    value : float or int
        Value to be set on the pin.
    """

    name = "set_pipico_pin"
    # def __init__(self, pin_values_dict, *args, **kwargs):
    #     self.pin_values = pin_values_dict
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, pin_value, **kwargs):
        self.Pico = PiPico()  # instance of raspberry pi pico
        # error = self.Pico.init("COM3")  # init the Com Port (Device Manager to see which com port is used)
        # print("inst: ", error)  # printing the connection Settings
        # self.Pico.clear_Pin(0) # 0 is the opto-pin
        self.pin_value = pin_value

        super().__init__(*args, **kwargs)

    def initialise_external(self, experiment):

        # Initialize serial connection and set it as experiment attribute to make
        # it available for other stimuli:
        try:
            self._pyb = getattr(experiment, "_pyb")
        except AttributeError:
            experiment._pyb = self.Pico.init("COM3")
            self._pyb = getattr(experiment, "_pyb")

    def start(self):
        print("done")
        super().start()
        if self.pin_value == 0:
            self.Pico.clear_Pin(0)
        else:
            self.Pico.set_Pin(0)

    def stop(self):
        super().stop()
        self.Pico.close()


class ContinuousWritePiPicoPin(InterpolatedStimulus):
    """Class to turn on or off a PiPico pin dynamically during the experiment.

    Parameters
    ----------
    ### outdated ###
    # pin : int
    #     Pin number.
    # value : float or int
    #     Value to be set on the pin.
    """

    name = "set_pipico_pin_continuous"

    def __init__(self, *args, **kwargs):
        self.Pico = PiPico()  # instance of raspberry pi pico
        error = self.Pico.init("COM3")  # init the Com Port (Device Manager to see which com port is used)
        print("inst: ", error)  # printing the connection Settings
        self.Pico.clear_Pin(0) # 0 is the opto-pin

        self.pin_value = 0
        super().__init__(*args, dynamic_parameters=["pin_value"], **kwargs)

    def update(self):
        super().update()
        if self.pin_value == 1:
            self.Pico.set_Pin(0)
        if self.pin_value == 0:
            self.Pico.clear_Pin(0)

    def stop(self):
        super().update()
        self.Pico.close()
