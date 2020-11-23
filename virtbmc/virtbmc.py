# 
# This builds off of pyghmi to virtualize BMC functionality for both Openstack
# and RHV
#

import argparse
import sys
from multiprocessing import Pool
import os
import rhvm
import osp
import configparser

import pyghmi.ipmi.bmc as bmc

class VirtBmc(bmc.Bmc):
    backend = None
    instance = None

    def __init__(self, authdata, port):
        super(VirtBmc, self).__init__(authdata, port)
        self.powerstate = 'off'
        self.bootdevice = 'default'

    def get_boot_device(self):
        return self.bootdevice

    def set_boot_device(self, bootdevice):
        self.bootdevice = bootdevice
        self.backend.boot_device(self.instance, self.bootdevice)

    def cold_reset(self):
        # Reset of the BMC, not managed system, here we will exit the demo
        print('shutting down in response to BMC cold reset request')
        sys.exit(0)

    def get_power_state(self):
        return self.backend.status(self.instance)

    def power_off(self):
        # this should be power down without waiting for clean shutdown
        self.backend.power_off(self.instance)
        self.powerstate = 'off'

    def power_on(self):
        self.backend.power_on(self.instance)
        self.powerstate = 'on'

    def power_reset(self):
        pass

    def power_shutdown(self):
        # should attempt a clean shutdown
        self.backend.power_off(self.instance)
        self.powerstate = 'off'

    def is_active(self):
        return self.powerstate == 'on'

    def iohandler(self, data):
        print(data)
        if self.sol:
            self.sol.send_data(data)

    def set_backend(self, backend):
        if backend == 'RHV':
            self.backend = rhvm.RHVM('/etc/virtbmc/virtbmc.conf')
            self.backend.connect()
        if backend == 'OSP':
            self.backend = osp.OSP('/etc/virtbmc/virtbmc.conf')
            self.backend.connect()

    def set_instance(self, instance_name):
        self.instance = instance_name

def spawn_listener(instance_data):
    (backend, instance_name, port) = instance_data.split(':')
    parser = argparse.ArgumentParser(
        prog='virtbmc',
        description='Pretend to be a BMC',
    )
    parser.add_argument('--port',
                        dest='port',
                        type=int,
                        default=port,
                        help='Port to listen on; defaults to 623')
    args = parser.parse_args()
    mybmc = VirtBmc({'admin': 'password'}, port=args.port) 
    mybmc.set_backend(backend)
    mybmc.set_instance(instance_name)
    print("[" + backend + "] Spawning instance for " + instance_name + " on port " + port)
    mybmc.listen()

def main():
    config = configparser.ConfigParser()
    config.read('/etc/virtbmc/virtbmc.conf')

    instance_list = config['Global']['BMCMap'].split(',')
    with Pool(len(instance_list)) as p:
      p.map(spawn_listener, instance_list)

if __name__ == '__main__':
    sys.exit(main())

