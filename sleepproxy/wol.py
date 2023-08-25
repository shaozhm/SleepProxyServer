import logging
import subprocess
from scapy.all import sendp,  Ether, IP, UDP, Raw

def wake(mac):
    logging.warning("Sending WOL packet to %s" % (mac, ))
    mac = mac.decode("hex")
    # sendp(Ether(dst='ff:ff:ff:ff:ff:ff') / IP(dst='255.255.255.255', flags="DF") / UDP(dport=9, sport=39227) / Raw('\xff' * 6 + mac * 16))
    callfun = subprocess.run([
    "/home/pi/blynk-library/scripts/blynk_ctrl.py", 
    "-s",
    "sonospi.local",
    "-p",
    "8442",
    "-t",
    "BO9Ej28AzpoEsaCs0WXiS3mqSO2KE8mZ",
    "-vw",
    "73",
    "1"], stdout=subprocess.DEVNULL)
    print("The exit code was: %d" % callfun.returncode)

if __name__ == '__main__':
    import sys
    wake(sys.argv[1])
