from PyQt5.QtWidgets import QApplication, QDialog

from stytra.stimulation.stimuli import Pause, Flash, MovingSeamless
from stytra.stimulation import Protocol
from stytra.gui.display_gui import StimulusDisplayWindow
from stytra.gui.control_gui import ProtocolControlWindow
from stytra.triggering import ZmqLightsheetTrigger
from stytra.metadata import DataCollector, MetadataFish, MetadataLightsheet, MetadataGeneral

import qdarkstyle
import deepdish as dd
import os



if __name__ == '__main__':
    experiment_folder = 'C:/Users/lpetrucco/Desktop/metadata/'

    stim_duration = 0.5
    pause_duration = 1
    n_repeats = 3
    flash_color = (255, 0, 0)
    refresh_rate = 1 / 60.
    initial_pause = 5

    # Generate stimulus protocol
    stimuli = []
    stimuli.append(Pause(duration=initial_pause-2))
    for i in range(n_repeats):
        stimuli.append(Flash(duration=stim_duration, color=flash_color))
        stimuli.append(Pause(duration=pause_duration))
    protocol = Protocol(stimuli, refresh_rate)

    # Set connection with the 'evil LabView' computer
    zmq_trigger = ZmqLightsheetTrigger(pause=initial_pause, tcp_address='tcp://192.168.233.156:5555')

    protocol.sig_protocol_started.connect(zmq_trigger.start)
    protocol.sig_protocol_finished.connect(zmq_trigger.stop)

    # Prepare control window and window for displaying the  stimulus
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Instantiate display window and control window:
    win_stim_disp = StimulusDisplayWindow(protocol)
    win_control = ProtocolControlWindow(app, protocol, win_stim_disp)

    # Take care of metadata:
    general_data = MetadataGeneral(experiment_name='only_flashes', experimenter_name='Luigi Petrucco')
    fish_data = MetadataFish()
    imaging_data = MetadataLightsheet()

    # Get info from microscope
    # dict_lightsheet_info = zmq_trigger.get_ls_data()
    # imaging_data.set_fix_value('scanning_profile', dict_lightsheet_info['Sawtooth Wave'])
    # imaging_data.set_fix_value('piezo_frequency', dict_lightsheet_info['Piezo Frequency'])
    # imaging_data.set_fix_value('piezo_amplitude', dict_lightsheet_info['Piezo Top and Bottom']['1'])

    data_collector = DataCollector(fish_data, imaging_data, general_data, folder_path=experiment_folder)
    data_collector.add_data_source('stimulus', 'log', protocol.log)
    data_collector.add_data_source('stimulus', 'window_pos', win_control.widget_view.roi_box.state, 'pos')
    data_collector.add_data_source('stimulus', 'window_size', win_control.widget_view.roi_box.state, 'size')

    win_control.button_metadata.clicked.connect(fish_data.show_gui)
    protocol.sig_protocol_finished.connect(data_collector.save)


    # Display windows:
    win_stim_disp.show()
    win_control.show()
    win_control.windowHandle().setScreen(app.screens()[0])
    win_stim_disp.windowHandle().setScreen(app.screens()[1])
    win_control.widget_view.repaint()
    win_stim_disp.showFullScreen()
    win_control.update_ROI()

    app.exec_()

    list_metadata = [fn for fn in os.listdir(experiment_folder) if fn.endswith('metadata.h5')]
    if len(list_metadata) > 0:
        last_metadata = dd.io.load(experiment_folder + list_metadata[-1])
        print(last_metadata)
