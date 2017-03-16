from PyQt4 import QtGui,QtCore
import sys
import subprocess
import ui_main
import numpy as np
import pyqtgraph
import SWHear
import pyaudio
import wave
import os
 
outFORMAT = pyaudio.paInt16
outCHANNELS = 1
outRATE = 192000
#outCHUNK = 1024
#outCHUNK = 8192
outRECORD_SECONDS = 5
outWAVE_OUTPUT_FILENAME = "/home/pi/bat"


# This displays a pyQt widget with a left scrolling windows
# Y axis is frequency
# Colour is intensity

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        #self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=1.0
        self.maxPCM=0
        self.roll=0.0
        self.ear = SWHear.SWHear()
        self.ear.stream_start()
        self.maxFFTRollCount=0
        self.maxFFTRoll=0.1
        self.recording=False
        #self.waveFile = wave.open(outWAVE_OUTPUT_FILENAME, 'wb')
        #self.waveFile.setnchannels(outCHANNELS)
        #audio = pyaudio.PyAudio()
        #self.waveFile.setsampwidth(audio.get_sample_size(outFORMAT))
        #self.waveFile.setframerate(outRATE)
        #waveFile.writeframes(b''.join(frames))
        #waveFile.close()
        self.centralwidget.mousePressEvent=self.toggle_recording

    #def __del__(self):
        #if not self.waveFile is None:
        #    self.waveFile.close()


    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            
            if self.recording:
                self.waveFile.writeframes(b''.join(self.ear.rawData))    
            #pcmMax=np.max(np.abs(self.ear.data))
            #if pcmMax>self.maxPCM:
                #self.maxPCM=pcmMax
                #self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            # Ignore first value
            self.ear.fft[1:10] = 0
            # Get the current max value
            thisMax = np.max(np.abs(self.ear.fft))
            
            if thisMax > self.maxFFTRoll:
             self.maxFFTRoll = thisMax            

            self.maxFFTRollCount+=1
            if self.maxFFTRollCount == 15:
                self.maxFFTRollCount=0 # reset every 15
                self.maxFFT = (self.maxFFT +self.maxFFTRoll) / 2.0 # use the max value from the last 15 as the new value
                self.maxFFTRoll = 0.0 # start collecting new values
                    
                #self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
            #self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            #pen=pyqtgraph.mkPen(color='b')
            #self.grPCM.plot(self.ear.datax,self.ear.data,
            #                pen=pen,clear=True)
            #pen=pyqtgraph.mkPen(color='r')
            #self.grFFT.plot(self.ear.fftx[:500],self.ear.fft[:500],
            #                pen=pen,clear=True)
           
            #spec = np.fft.rfft(chunk*self.win) / CHUNKSZ
            # get magnitude
            #spec = self.ear.fft[:500]
            #psd = abs(spec)
            # convert to dB scale
            #psd = 20 * np.log10(psd)
            #normalise to put data in range 0 to maxFFT
            psd = self.ear.fft[0:4096:8]
            #psd = abs(psd)
            #psd /= self.maxFFT
            #psd.fill(self.roll)
            #self.roll += 0.01
            #if self.roll >= 1.0:
            #    self.roll = 0.0
            #psd.fill(self.maxFFT)
            psd /= self.maxFFT
            #np.clip(psd[0:25],0.0,0.1)
            np.clip(psd,0.0,1.0)
            #psd = 20 * np.log10(psd)
            # roll down one and replace leading edge with new data
            self.grFFT.img_array = np.roll(self.grFFT.img_array, -2, 0)
            self.grFFT.img_array[-2:] = psd
            self.grFFT.img_array[-1:] = psd
            self.grFFT.img.setImage(self.grFFT.img_array, autoLevels=False)

        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def nextFilename(self):
        for i in range(1,50):
            string=outWAVE_OUTPUT_FILENAME+str(i)+".wav"
            if not os.path.exists(string):
                return string
        return ""


    def beginRecording(self):
        print "beginRecording()"
        string = self.nextFilename()
        self.waveFile = wave.open(string, 'wb')
        self.waveFile.setnchannels(outCHANNELS)
        audio = pyaudio.PyAudio()
        self.waveFile.setsampwidth(audio.get_sample_size(outFORMAT))
        self.waveFile.setframerate(outRATE)
        self.setWindowTitle("Recording...")

    def endRecording(self):
        print "endRecording()"
        if not self.waveFile is None:
            self.waveFile.close()
            self.setWindowTitle("Recording ended...")


    def toggle_recording(self, event):
       print "Widget clicked - toggle recording"
       if self.recording:
          self.endRecording()
          self.recording = False
       else:
          self.beginRecording()
          self.recording = True
       #string = self.nextFilename()
       #print string

if __name__=="__main__":
    subprocess.call ("/home/pi/Record_from_Headset.sh", shell=True) #set up to record from headphone mic
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
