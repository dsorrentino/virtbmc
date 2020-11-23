#
# The idea is to have a class module for each backend which supports the following methods:
#
# connect() - To establish the connection to the backend
# power_on(instance_name) - To power on an instance
# power_off(instance_name) - To power off an instance
# status(instance_name) - This will return the power state of the instance

from openstack import connection
import logging
import time

import configparser

class OSP():
  """A class to connect to Openstack"""
  config = None
  URL = None
  username = None
  password = None
  CA = None
  connection = None
  project = None
  region = None
  userdomain = None
  projectdomain = None
  pxeimage = None

  def __init__(self, config_file):
    self.config = config_file
    config = configparser.ConfigParser()
    config.read(config_file)
    self.URL = config['OSP']['ConnectionURL']
    self.username = config['OSP']['ConnectionUsername']
    self.password = config['OSP']['ConnectionPassword']
    #self.CA = config['OSP']['CaFile']
    self.projectname = config['OSP']['ProjectName']
    self.regionname = config['OSP']['RegionName']
    self.userdomain = config['OSP']['UserDomainName']
    self.projectdomain = config['OSP']['ProjectDomainName']
    self.pxeimage = config['OSP']['PXEImage']

  def connect(self):
    self.connection = connection.Connection(
        auth_url=self.URL,
        project_name=self.projectname,
        username=self.username,
        password=self.password,
        region_name=self.regionname,
        user_domain_name=self.userdomain,
        project_domain_name=self.projectdomain,
        app_name='virtbmc',
        app_version='1.0',
    )
    return

  def power_on(self,vmname):
    server_instance = self.connection.compute.find_server(vmname, True)
    if server_instance:
      server_instance = self.connection.compute.get_server(server_instance)
      if server_instance.status != "ACTIVE" and server_instance.task_state != "powering-on":
        self.connection.compute.start_server(server_instance)
    return

  def power_off(self,vmname):
    server_instance = self.connection.compute.find_server(vmname, True)
    if server_instance:
      server_instance = self.connection.compute.get_server(server_instance)
      if server_instance.status != "SHUTOFF" and server_instance.status != "STOPPED" and server_instance.task_state != "powering-off":
        self.connection.compute.stop_server(server_instance)
    return

  def status(self,vmname):
    power_state = 'on'
    server_instance = self.connection.compute.find_server(vmname, True)
    if server_instance:
      server_instance = self.connection.compute.get_server(server_instance)
      # Status that may be returned: ACTIVE, BUILDING, DELETED, ERROR, HARD_REBOOT, PASSWORD, PAUSED, REBOOT, REBUILD, RESCUED, RESIZED, REVERT_RESIZE, SHUTOFF, SOFT_DELETED, STOPPED, SUSPENDED, UNKNOWN, or VERIFY_RESIZE.
      if server_instance.status == "SHUTOFF":
        power_state = 'off'
    return power_state

  def boot_device(self,vmname,bootdevice):
    if bootdevice == "network":
      server_instance = self.connection.compute.find_server(vmname, True)
      if server_instance:
        server_instance = self.connection.compute.get_server(server_instance)
        pxeimage = self.connection.compute.find_image(self.pxeimage)
        if pxeimage:
          self.connection.compute.rebuild_server(server_instance, vmname, self.password, image=pxeimage)

  def disconnect(self):
    return
