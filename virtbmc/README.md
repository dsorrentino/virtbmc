The goal of virtbmc.py is to utilize modular backends to support basic BMC functionality. The expectation is each backend would be a python class that supports the following methods:

.connect()                        - Establish the connection/authentication to the backend
.power_on(vmname)                - Power on an instance in the backend that matches the vmname passed to this method. Expectation is vmname is a string.
.power_off(vmname)               - Power off an instance in the backend that matches the vmname passed to this method. Expectation is vmname is a string.
.status(vmname)                  - Returns either 'on' or 'off' representing the power state of the vmname passed to this method. Expectation is vmname is a string.
.boot_device(vmname, bootdevice) - Sets the boot device for vmname to the passed bootdevice. Valid values for bootdevice are:
                                   "network" - Boot from PXE
                                   "hd"      - Boot from HDD
                                   "optical" - Boot from CDROM
                                   Expectation is vmname and bootdevice are both strings.

Backends such as Openstack, don't support setting of the boot device, however, it is possible to create a PXE image in
Openstack and have the instance boot with that.  The backend driver for Openstack rebuilds the image with the provided
PXE image (per the config file) in order to replicate the PXE boot process.

One could also incorporate a VMWare backend to this as well, however, I don't have a VMWare environment to test with in order
to write this myself.
