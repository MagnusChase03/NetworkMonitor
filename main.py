import time
import threading
from tkinter import *
from tkinter import scrolledtext
import tkinter
import pyshark
import psutil

class Application:
    # Create GUI
    def __init__(self):

        self.downloadBandwidth = 0
        self.uploadBandwidth = 0
        self.latestPacket = "None"

        self.window = tkinter.Tk()
        self.window.geometry("720x480")
        self.window.title("Bandwidth Monitor");
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window, width=720, height=480, bg="White")

        self.canvas.create_text(200, 50, text="Download", fill="black", font=('Monospace 15 bold'))
        self.downloadBandwidthLable = self.canvas.create_text(200, 100, text=self.downloadBandwidth, fill="black", font=('Monospace 15 bold'))

        self.canvas.create_text(500, 50, text="Upload", fill="black", font=('Monospace 15 bold'))
        self.uploadBandwidthLable = self.canvas.create_text(500, 100, text=self.uploadBandwidth, fill="black", font=('Monospace 15 bold'))

        self.canvas.create_text(350, 250, text="Latest Packet", fill="black", font=('Monospace 15 bold'))
        self.latestPacketLable = self.canvas.create_text(350, 350, text=self.latestPacket, fill="black", font=('Monospace 10 bold'))

    # Gets network packets
    def updateNetworkPackets(self):

        capture = pyshark.LiveCapture(interface="wlp0s20f3")

        for packet in capture.sniff_continuously():
            try:

                protocol = packet.transport_layer
                sourceIP = packet.ip.src
                dstIP = packet.ip.dst
                sourcePort = packet[protocol].srcport
                dstPort = packet[protocol].dstport

                self.latestPacket = "Protocol: %s / Source: %s:%s / Destination: %s:%s" % (protocol, sourceIP, sourcePort, dstIP, dstPort)
                self.canvas.itemconfigure(self.latestPacketLable, text=self.latestPacket)

                time.sleep(1)

            except AttributeError:
                pass
            

    # Updates download bandwith in megabytes
    def updateDownloadBandwidth(self):
        self.downloadBandwidth = psutil.net_io_counters().bytes_recv / 1024 / 1024
        self.canvas.itemconfigure(self.downloadBandwidthLable, text="%.2fMB" % self.downloadBandwidth)

    # Updates upload bandwith in megabytes
    def updateUploadBandwidth(self):
        self.uploadBandwidth = psutil.net_io_counters().bytes_sent / 1024 / 1024
        self.canvas.itemconfigure(self.uploadBandwidthLable, text="%.2fMB" % self.uploadBandwidth)

    # Update function
    def update(self):
        while True:
            self.updateDownloadBandwidth()
            self.updateUploadBandwidth()
            self.updateNetworkPackets()
            time.sleep(1)

    # Runs the application
    def run(self):

        updateThread = threading.Thread(target=self.update)
        updateThread.start()

        self.canvas.pack()
        self.window.mainloop()


def main():
    app = Application()
    app.run()

main()