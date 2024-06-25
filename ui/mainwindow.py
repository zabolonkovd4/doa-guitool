from PyQt5 import QtWidgets as qtw
from generated_doa_main import Ui_MainWindow
from generated_doa_about import Ui_AboutWindow
from doa_processor import DoAMethod as doa_method
from doa_processor import set_array
from doatools.plotting import plot_array
import matplotlib.pyplot as plt

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mw = Ui_MainWindow()
        # Attributes
        self.array_index = 0

        # About
        self.about_window = qtw.QMainWindow()
        self.about_window_ui = Ui_AboutWindow()
        self.about_window_ui.setupUi(self.about_window)

        self.mw.setupUi(self)
        self.mw.algo.addItem(doa_method.MUSIC)
        self.mw.algo.addItem(doa_method.ROOT_MUSIC)

        # Array configuration
        array_type = self.array_type()
        arr = set_array(self.mw.antennas.value(), self.mw.wavelength.value(), array_type)
        self.draw_array(arr)

        # Signals and slot connections
        self.mw.wavelength.valueChanged.connect(self.recalc_spacing)
        self.mw.start_processing_btn.clicked.connect(self.process)
        self.mw.uca_radio_btn.clicked.connect(self.uca_choosed)
        self.mw.ula_radio_btn.clicked.connect(self.ula_choosed)
        self.mw.antennas.valueChanged.connect(self.antennas_count_changed)

    def draw_array(self, array):
        self.mw.arrayWidget.canvas.ax.clear()
        self.mw.arrayWidget.canvas.ax.set_title(array.name)
        plot_array(array, ax=self.mw.arrayWidget.canvas.ax)
        if not self.mw.arrayWidget.canvas.ax:
            self.mw.arrayWidget.canvas.ax = plt.subplot(1, 2, 1)
        self.mw.arrayWidget.canvas.ax.plot(8, 4)
        self.mw.arrayWidget.canvas.draw()

    def antennas_count_changed(self, new_count):
        arr = set_array(new_count, self.mw.wavelength.value(), self.array_type())
        self.draw_array(arr)

    def recalc_spacing(self, arg):
        self.mw.spacing.setValue(arg / 2)
        arr = set_array(self.mw.antennas.value(), self.mw.wavelength.value(), self.array_type())
        self.draw_array(arr)

    def array_type(self):
        array_type = self.mw.uca_radio_btn.text() if self.mw.uca_radio_btn.isChecked() else self.mw.ula_radio_btn.text()
        return array_type

    def process(self):
        pass

    def uca_choosed(self):
        arr = set_array(self.mw.antennas.value(), self.mw.wavelength.value(), arr_type='UCA')
        self.draw_array(arr)

    def ula_choosed(self):
        arr = set_array(self.mw.antennas.value(), self.mw.wavelength.value(), arr_type='ULA')
        self.draw_array(arr)


if __name__ == "__main__":
    app = qtw.QApplication([])
    app.setApplicationName("DoA")
    mw = MainWindow()
    mw.show()
    app.exec_()
