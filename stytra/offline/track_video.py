from pathlib import Path
from stytra import Stytra
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog, QPushButton,\
    QComboBox, QGridLayout, QLabel
import qdarkstyle
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import Stimulus
from stytra.experiments.fish_pipelines import pipeline_dict
import imageio
import pandas as pd


class EmptyProtocol(Protocol):
    name = "parameters"

    def get_stim_sequence(self):
        return [Stimulus(duration=5.),]


class StytraLoader(QDialog):
    """ A quick-and-dirty monkey-patch of Stytra for easy offline tracking

    """
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Select video for offline tracking")
        self.app = app

        self.btn_vid = QPushButton("Select video")
        self.btn_vid.clicked.connect(self.select_video)
        self.filename = None
        self.lbl_filename = QLabel("")

        self.lbl_whattrack = QLabel("What to track")
        self.cmb_tracking = QComboBox()
        self.cmb_tracking.addItems(list(pipeline_dict.keys()))

        self.lbl_outformat = QLabel("Tracking output format")
        self.cmb_fmt = QComboBox()
        self.cmb_fmt.addItems([
            "csv", "feather", "hdf5", "json"])

        self.btn_start = QPushButton("Start stytra")
        self.btn_start.clicked.connect(self.run_stytra)
        self.btn_start.setEnabled(False)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.btn_vid, 0, 0)
        self.layout().addWidget(self.lbl_filename, 0, 1)

        self.layout().addWidget(self.lbl_whattrack, 1, 0)
        self.layout().addWidget(self.cmb_tracking, 1, 1)

        self.layout().addWidget(self.lbl_outformat, 2, 0)
        self.layout().addWidget(self.cmb_fmt, 2, 1)

        self.layout().addWidget(self.btn_start, 3, 0, 1, 2)

        self.stytra = None

    def select_video(self):
        fn, _ = QFileDialog.getOpenFileName(None, "Select video file",
                                            filter="Videos (*.avi *.mov *.mp4)")
        self.filename = fn
        self.lbl_filename.setText(self.filename)
        self.btn_start.setEnabled(True)

    def run_stytra(self):
        self.stytra = Stytra(app=self.app, protocol=EmptyProtocol(),
                             camera=dict(video_file=self.filename),
                             tracking=dict(method=self.cmb_tracking.currentText()),
                             log_format=self.cmb_fmt.currentText(),
                             exec=False)
        btn_track = QPushButton("Track video")
        self.stytra.exp.window_main.toolbar_control.addWidget(btn_track)
        btn_track.clicked.connect(self.track)
        self.stytra.exp.window_display.hide()
        self.close()

    def track(self):
        assert isinstance(self.stytra, Stytra)
        self.stytra.exp.camera.kill_event.set()
        reader = imageio.get_reader(self.filename)
        data = []
        self.stytra.exp.window_main.stream_plot.toggle_freeze()
        self.stytra.exp.window_main.toolbar_control.progress_bar.setMaximum(reader.get_length())
        self.stytra.exp.window_main.toolbar_control.progress_bar.setFormat("%v / %m")
        for i, frame in enumerate(reader):
            data.append(self.stytra.exp.pipeline.run(frame[:, :, 0]).data)
            self.stytra.exp.window_main.toolbar_control.progress_bar.setValue(i)
            if i % 100 == 0:
                self.app.processEvents()
        df = pd.DataFrame.from_records(data, columns=data[0]._fields)
        out_path = Path(self.filename)
        df.to_csv(out_path.parent / (out_path.stem + ".csv"))
        self.stytra.exp.wrap_up()
        self.app.quit()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ld = StytraLoader(app)
    ld.show()
    app.exec()


