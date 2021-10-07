import numpy as np
import pandas as pd
from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import MovingSineGrating
from lightparam import Param


class MovingSineGratingProtocol(Protocol):
    name = "moving_sine_grating_protocol"

    def __init__(self):
        super().__init__()

        self.inter_stim_pause = Param(2.0)
        self.theta_amp = Param(np.pi / 2)
        self.windmill_freq = Param(0.2)
        self.stim_duration = Param(5.0)
        self.wave_shape = Param(value="sinusoidal", limits=["square", "sinusoidal"])
        self.n_arms = Param(10)

    def get_stim_sequence(self):
        stimuli = []
        p = self.inter_stim_pause / 2
        d = self.stim_duration

        # Windmill
        STEPS = 0.005
        t = np.arange(0, d, STEPS)
        phase = np.sin(2 * np.pi * t * self.windmill_freq) * self.theta_amp

        t = [t[0]] + list(t + p) + [(t + 2 * p)[-1]]
        phase = [phase[0]] + list(phase) + [phase[-1]]
        df = pd.DataFrame(dict(t=t, theta=phase))
        stimuli.append(
            MovingSineGrating(
                df_param=df, n_arms=self.n_arms, wave_shape=self.wave_shape
            )
        )
        return stimuli
    #
    #     self.t_pre = Param(5.0)  # time of still gratings before they move
    #     self.t_move = Param(5.0)  # time of gratings movement
    #     self.grating_vel = Param(-10.0)  # gratings velocity
    #     self.grating_period = Param(10)  # grating spatial period
    #     self.grating_angle_deg = Param(90.0)  # grating orientation

    # def get_stim_sequence(self):
    #     # Use six points to specify the velocity step to be interpolated:
    #     t = [
    #         0,
    #         self.t_pre,
    #         self.t_pre,
    #         self.t_pre + self.t_move,
    #         self.t_pre + self.t_move,
    #         2 * self.t_pre + self.t_move,
    #     ]
    #
    #     vel = [0, 0, self.grating_vel, self.grating_vel, 0, 0]
    #
    #     df = pd.DataFrame(dict(t=t, vel_x=vel))
    #
    #     return [
    #         MovingSineGrating(
    #             df_param=df,
    #             grating_angle=self.grating_angle_deg * np.pi / 180,
    #             grating_period=self.grating_period,
    #         )
    #     ]

if __name__ == "__main__":
    # We make a new instance of Stytra with this protocol as the only option:
    s = Stytra(protocol=MovingSineGratingProtocol())
