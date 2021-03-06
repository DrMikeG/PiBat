"""
this is a stripped down version of the SWHear class.
It's designed to hold only a single audio sample in memory.
check my githib for a more complete version:
    http://github.com/swharden
"""

import pyaudio
import time
import pylab
import numpy as np
import threading
import scipy
import scipy.fftpack

def getFFT(data,rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    #data=data*np.hamming(len(data))
    fft=np.fft.fft(data)
    fft=np.abs(fft)
    #fft=10*np.log10(fft)
    freq=np.fft.fftfreq(len(fft),1.0/rate)
    return freq[:int(len(freq)/2)],fft[:int(len(fft)/2)]

class SWHear(object):
    """
    The SWHear class is made to provide access to continuously recorded
    (and mathematically processed) microphone data.
    """

    def __init__(self,device=None,rate=None):
        """fire up the SWHear class."""
        self.p=pyaudio.PyAudio()
        #self.chunk = 4096 # number of data points to read at a time
        self.chunk = 8192
        self.device=device
        self.rate=rate
        self.dropped=0
        self.fHandle=None
        self.recording = False

    ### SYSTEM TESTS

    def valid_low_rate(self,device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [192000]:
            if self.valid_test(device,testrate):
                return testrate
        print("SOMETHING'S WRONG! I can't figure out how to use DEV",device)
        return None

    def valid_test(self,device,rate=192000):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        try:
            self.info=self.p.get_device_info_by_index(device)
            if not self.info["maxInputChannels"]>0:
                return False
            stream=self.p.open(format=pyaudio.paInt16,channels=1,
               input_device_index=device,frames_per_buffer=self.chunk,
               rate=int(self.info["defaultSampleRate"]),input=True)
            stream.close()
            return True
        except:
            return False

    def valid_input_devices(self):
        """
        See which devices can be opened for microphone input.
        call this when no PyAudio object is loaded.
        """
        mics=[]
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                mics.append(device)
        if len(mics)==0:
            print("no microphone devices found!")
        else:
            print("found %d microphone devices: %s"%(len(mics),mics))
        return mics

    ### SETUP AND SHUTDOWN

    def initiate(self):
        """run this after changing settings (like rate) before recording"""
        if self.device is None:
            self.device=self.valid_input_devices()[0] #pick the first one
        if self.rate is None:
            self.rate=self.valid_low_rate(self.device)
        if not self.valid_test(self.device,self.rate):
            print("guessing a valid microphone device/rate...")
            self.device=self.valid_input_devices()[0] #pick the first one
            self.rate=self.valid_low_rate(self.device)
        self.datax=np.arange(self.chunk)/float(self.rate)
        msg='recording from "%s" '%self.info["name"]
        msg+='(device %d) '%self.device
        msg+='at %d Hz'%self.rate
        print(msg)

    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording=False #the threads should self-close
        while(self.t.isAlive()): #wait for all threads to close
            time.sleep(.1)
        self.stream.stop_stream()
        self.p.terminate()

    ### STREAM HANDLING

    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.rawData = self.stream.read(self.chunk)
            if self.recording:
                if not self.fHandle is None:
                    try:
                        #print("write to file")
                        self.fHandle.writeframes(b''.join(self.rawData))
                    except Exception as F:
                        print str(F)
            self.data = np.fromstring(self.rawData,dtype=np.int16)
            self.fftx, self.fft = getFFT(self.data,self.rate)

        except Exception as E:
            self.dropped = self.dropped + 1
            print "%d -- exception! terminating..." % self.dropped
            print "I/O error({0}): {1}".format(E.errno, E.strerror)
            self.keepRecording=True
        if self.keepRecording:
            self.stream_thread_new()
        else:
            self.stream.close()
            self.p.terminate()
            print(" -- stream STOPPED")

    def stream_thread_new(self):
        self.t=threading.Thread(target=self.stream_readchunk)
        self.t.start()

    def stream_start(self):
        """adds data to self.data until termination signal"""
        self.initiate()
        print(" -- starting stream")
        self.keepRecording=True # set this to False later to terminate stream
        self.data=None # will fill up with threaded recording data
        self.fft=None
        self.dataFiltered=None #same
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,
                      rate=self.rate,input=True,frames_per_buffer=self.chunk)
        self.stream_thread_new()

if __name__=="__main__":
    ear=SWHear()
    ear.stream_start() #goes forever
    while True:
        print(ear.data)
        time.sleep(.1)
    print("DONE")
