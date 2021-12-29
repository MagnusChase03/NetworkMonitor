import time
import threading
import pyshark
import psutil

# Gets network packets
def getNetworkPackets():
    capture = pyshark.LiveCapture(interface="wlp0s20f3")

    for packet in capture.sniff_continuously():
        try:

            protocol = packet.transport_layer
            sourceIP = packet.ip.src
            dstIP = packet.ip.dst
            sourcePort = packet[protocol].srcport
            dstPort = packet[protocol].dstport

            print("Protocol: %s / Source: %s:%s / Destination: %s:%s" % (protocol, sourceIP, sourcePort, dstIP, dstPort))

        except AttributeError:
            pass
        

# Returns download bandwith in megabytes
def getDownloadBandwidth():
    return psutil.net_io_counters().bytes_recv / 1024 / 1024

# Returns upload bandwith in megabytes
def getUploadBandwidth():
    return psutil.net_io_counters().bytes_sent / 1024 / 1024

# Displays bandwidth
def displayBandwidth():
    downlodBandwidth = 0
    uploadBandwidth = 0

    while True:

        newDownlodBandwidth = getDownloadBandwidth()
        newUploadBandwidth = getUploadBandwidth()

        if not downlodBandwidth == newDownlodBandwidth and not uploadBandwidth == newUploadBandwidth:

            downlodBandwidth = newUploadBandwidth
            uploadBandwidth = newUploadBandwidth

            print("> Download: %.2fMB / Upload: %.2fMB / Total: %.2fMB" % (downlodBandwidth, uploadBandwidth, downlodBandwidth + uploadBandwidth))

        time.sleep(1)

def main():
    bandwidthThread = threading.Thread(target=displayBandwidth)
    packetThread = threading.Thread(target=getNetworkPackets)

    bandwidthThread.start()
    packetThread.start()

main()