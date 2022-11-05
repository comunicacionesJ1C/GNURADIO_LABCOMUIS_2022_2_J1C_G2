#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: calculo_de_potencia
# Author: uis
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from Envolvente_DSB import Envolvente_DSB  # grc-generated hier_block
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from lab2_punto1 import lab2_punto1  # grc-generated hier_block



from gnuradio import qtgui

class calculo_de_potencia(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "calculo_de_potencia", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("calculo_de_potencia")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "calculo_de_potencia")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.KA = KA = 1
        self.AP = AP = 0.1
        self.A = A = 1

        ##################################################
        # Blocks
        ##################################################
        self._KA_range = Range(0, 4, 0.00001, 1, 200)
        self._KA_win = RangeWidget(self._KA_range, self.set_KA, "Coeficiente KA", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._KA_win)
        self._AP_range = Range(0, 1, 0.0001, 0.1, 200)
        self._AP_win = RangeWidget(self._AP_range, self.set_AP, "amplitud Portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._AP_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(50000000, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.lab2_punto1_0 = lab2_punto1(
            I_vect=1024,
        )

        self.top_layout.addWidget(self.lab2_punto1_0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        self.Envolvente_DSB_0 = Envolvente_DSB(
            Ac=AP,
            Ka=KA,
        )
        self._A_range = Range(0, 1, 0.00001, 1, 200)
        self._A_win = RangeWidget(self._A_range, self.set_A, "amplitud", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._A_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Envolvente_DSB_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.Envolvente_DSB_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.lab2_punto1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "calculo_de_potencia")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_KA(self):
        return self.KA

    def set_KA(self, KA):
        self.KA = KA
        self.Envolvente_DSB_0.set_Ka(self.KA)

    def get_AP(self):
        return self.AP

    def set_AP(self, AP):
        self.AP = AP
        self.Envolvente_DSB_0.set_Ac(self.AP)

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A




def main(top_block_cls=calculo_de_potencia, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
