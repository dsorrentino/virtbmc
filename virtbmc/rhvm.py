#
# The idea is to have a class module for each backend which supports the following methods:
#
# connect() - To establish the connection to the backend
# power_on(instance_name) - To power on an instance
# power_off(instance_name) - To power off an instance
# status(instance_name) - This will return the power state of the instance


import logging
import time

import ovirtsdk4 as sdk
from ovirtsdk4 import types
import configparser

class RHVM():
  """A class to connect to RHVM"""
  config = None
  URL = None
  username = None
  password = None
  CA = None
  connection = None
  vms_service = None

  def __init__(self, config_file):
    self.config = config_file
    config = configparser.ConfigParser()
    config.read(config_file)
    self.URL = config['RHV']['ConnectionURL']
    self.username = config['RHV']['ConnectionUsername']
    self.password = config['RHV']['ConnectionPassword']
    self.CA = config['RHV']['CaFile']

  def connect(self):
    self.connection = sdk.Connection(url=self.URL, username=self.username, password=self.password, ca_file=self.CA, debug=True, log=logging.getLogger(),)
    self.vms_service = self.connection.system_service().vms_service()
    return

  def find_vm(self,vmname):
    search_string = 'name=' + vmname
    return self.vms_service.list(search=search_string)[0]

  def power_on(self,vmname):
    vm = self.find_vm(vmname)
    vm_service = self.vms_service.vm_service(vm.id)
    vm_service.start()

  def power_off(self,vmname):
    vm = self.find_vm(vmname)
    vm_service = self.vms_service.vm_service(vm.id)
    vm_service.stop()

  def status(self,vmname):
    vm = self.find_vm(vmname)
    vm_service = self.vms_service.vm_service(vm.id)
    vm = vm_service.get()
    power_state = 'on'
    # States which might be returned:
    #  DOWN
    #  IMAGE_LOCKED
    #  MIGRATING
    #  NOT_RESPONDING
    #  PAUSED
    #  POWERING_DOWN
    #  POWERING_UP
    #  REBOOT_IN_PROGRESS
    #  RESTORING_STATE
    #  SAVING_STATE
    #  SUSPENDED
    #  UNASSIGNED
    #  UNKNOWN
    #  UP
    #  WAIT_FOR_LAUNCH
    if vm.status == sdk.types.VmStatus.DOWN:
      power_state = 'off'
    if vm.status == sdk.types.VmStatus.UNKNOWN:
      power_state = 'unknown'
    if vm.status == sdk.types.VmStatus.UNASSIGNED:
      power_state = 'unknown'
    return power_state

  def boot_device(self,vmname,bootdevice):
    if bootdevice == "network":
      vm = self.find_vm(vmname)
      vm_service = self.vms_service.vm_service(vm.id)
      vm_service.update(vm=types.Vm(os=types.OperatingSystem(boot=types.Boot(devices=[types.BootDevice.NETWORK]))))
    if bootdevice == "hd":
      vm = self.find_vm(vmname)
      vm_service = self.vms_service.vm_service(vm.id)
      vm_service.update(vm=types.Vm(os=types.OperatingSystem(boot=types.Boot(devices=[types.BootDevice.HD]))))
    if bootdevice == "optical":
      vm = self.find_vm(vmname)
      vm_service = self.vms_service.vm_service(vm.id)
      vm_service.update(vm=types.Vm(os=types.OperatingSystem(boot=types.Boot(devices=[types.BootDevice.CDROM]))))
    return

  def disconnect(self):
    self.connection.close()
