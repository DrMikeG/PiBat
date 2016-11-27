# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 400)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        #self.pbLevel = QtGui.QProgressBar(self.centralwidget)
        #self.pbLevel.setMaximum(1000)
        #self.pbLevel.setProperty("value", 123)
        #self.pbLevel.setTextVisible(False)
        #self.pbLevel.setOrientation(QtCore.Qt.Vertical)
        #self.pbLevel.setObjectName(_fromUtf8("pbLevel"))
        #self.horizontalLayout.addWidget(self.pbLevel)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        #self.label = QtGui.QLabel(self.frame)
        #self.label.setObjectName(_fromUtf8("label"))
        #self.verticalLayout.addWidget(self.label)
        self.grFFT = PlotWidget(self.frame)
        self.grFFT.setObjectName(_fromUtf8("grFFT"))
        

        self.grFFT.img = pg.ImageItem()
        self.grFFT.addItem(self.grFFT.img)
        #CHUNKSZ = 500
        #FS = 192000
        #self.grFFT.img_array = np.zeros((1000, CHUNKSZ/2+1))
        fftImgHeight = 512
        self.grFFT.img_array = np.zeros((1000, fftImgHeight))

        # bipolar colormap
        #pos = np.array([0., 1., 0.5, 0.25, 0.75])
        #color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255],(0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        #cmap = pg.ColorMap(pos, color)
        #lut = cmap.getLookupTable(0.0, 1.0, 256)

        #pos2 = np.array([0.0, 0.2, 0.4, 0.6, 0.8])
        #color2 = np.array([[75,64,128,255],[64,107,128,255],[64,128,96,255],[85,128,64,255],[128,117,64,255],[128,64,64,255]],dtype=np.ubyte)
        pos2 = np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
        color2 = np.array([[51,000,51,255],[127,000,255,255],[000,000,255,255],[000,128,255,255],[000,255,255,255],[000,255,128,255],[000,255,000,255],[128,255,000,255],[255,255,000,255],[255,128,000,255],[255,000,000,255]],dtype=np.ubyte)
        cmap2 = pg.ColorMap(pos2,color2)
        lut = cmap2.getLookupTable(0.0, 1.0, 512) # get lookup table from 0 to 1 (512 pts)


        # set colormap
        self.grFFT.img.setLookupTable(lut)
        self.grFFT.img.setLevels([0,1])

        # setup the correct scaling for y-axis
        #freq = np.arange((CHUNKSZ/2)+1)/(float(CHUNKSZ)/FS)
        #yscale = 1.0/(self.grFFT.img_array.shape[1]/freq[-1])
        #self.grFFT.img.scale((1./FS)*CHUNKSZ, yscale)
        
        self.verticalLayout.addWidget(self.grFFT)
        #self.label_2 = QtGui.QLabel(self.frame)
        #self.label_2.setObjectName(_fromUtf8("label_2"))
        #self.verticalLayout.addWidget(self.label_2)
        
        #self.grPCM = PlotWidget(self.frame)
        #self.grPCM.setObjectName(_fromUtf8("grPCM"))
        #self.verticalLayout.addWidget(self.grPCM)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        #self.label.setText(_translate("MainWindow", "frequency data (FFT):", None))
        #self.label_2.setText(_translate("MainWindow", "raw data (PCM):", None))

from pyqtgraph import PlotWidget
