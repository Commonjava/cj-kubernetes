import os
import sys
import subprocess
import kubesvc

REJECT_CMD = "INPUT -j REJECT --reject-with icmp-host-prohibited"

def mod_chains(chain, delete=False, fail=True):
    if delete is True:
        cmd = "/sbin/iptables -D %s" % chain
    else:
        cmd = "/sbin/iptables -A %s" % chain

    print "\n%s" % cmd
    ret = os.system(cmd)
    if ret != 0:
        print "FAILED: %s (code: %s)\n" % (cmd, ret)
        if fail is True:
             sys.exit(ret)


def get_service_port(service):
    iptables=subprocess.check_output('/sbin/iptables-save')
    for line in iptables.splitlines():
        if service in line and 'KUBE-NODEPORT-HOST' in line and 'to-destination' in line:
            return line.split()[15].split(':')[1]
    return None

def expose_service_port(service, port):
    print "Exposing service: %s on port: %s" % (service, port)

    addCmd = "INPUT -p tcp -m state --state NEW -m tcp --dport %s -j ACCEPT" % port

    mod_chains(addCmd, delete=True, fail=False)
    mod_chains(REJECT_CMD, delete=True, fail=False)
    mod_chains(addCmd, fail=False)
    mod_chains(REJECT_CMD)

def protect_service_port(service, port):
    print "Deleting service: %s on port: %s" % (service, port)

    addCmd = "INPUT -p tcp -m state --state NEW -m tcp --dport %s -j ACCEPT" % port

    mod_chains(addCmd, delete=True, fail=False)
