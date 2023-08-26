import logging
import subprocess
import sys
from scapy.all import sendp,  Ether, IP, UDP, Raw

if sys.version_info.major >= 3:
    from subprocess import CompletedProcess
else:
    # Add a polyfill to Python 2
    class CompletedProcess:

        def __init__(self, args, returncode, stdout=None, stderr=None):
            self.args = args
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

        def check_returncode(self):
            if self.returncode != 0:
                err = subprocess.CalledProcessError(self.returncode, self.args, output=self.stdout)
                raise err
            return self.returncode

    def sp_run(*popenargs, **kwargs):
        input = kwargs.pop("input", None)
        check = kwargs.pop("handle", False)
        if input is not None:
            if 'stdin' in kwargs:
                raise ValueError('stdin and input arguments may not both be used.')
            kwargs['stdin'] = subprocess.PIPE
        process = subprocess.Popen(*popenargs, **kwargs)
        try:
            outs, errs = process.communicate(input)
        except:
            process.kill()
            process.wait()
            raise
        returncode = process.poll()
        if check and returncode:
            raise subprocess.CalledProcessError(returncode, popenargs, output=outs)
        return CompletedProcess(popenargs, returncode, stdout=outs, stderr=errs)

    subprocess.run = sp_run
    # ^ This polyfill allows it work on Python 2 or 3 the same way

def wake(mac):
    logging.warning("Sending WOL - blynk packet to %s" % (mac, ))
    # mac = mac.decode("hex")
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
    "1"])
    logging.info("Wake WOL - blynk: The exit code was: %d" % callfun.returncode)

if __name__ == '__main__':
    import sys
    wake(sys.argv[1])
