#!/bin/bash

if [[ ! -z "$(grep 'Red Hat Enterprise Linux release 8' /etc/redhat-release)" ]]
then
  RHV_REPO=rhv-4.4-manager-for-rhel-8-x86_64-rpms
  OSP_REPO=openstack-16.1-for-rhel-8-x86_64-rpms
  sudo subscription-manager repos --enable=${RHV_REPO} --enable=${OSP_REPO}
elif [[ ! -z "$(grep 'CentOS Linux release 8' /etc/redhat-release)" ]]
then
  OVIRT_REPO=https://resources.ovirt.org/pub/yum-repo/ovirt-release44.rpm
  sudo yum install -y ${OVIRT_REPO}
  sudo yum install -y centos-release-openstack-train
else
  echo "[ERROR] Unsure how to install necessary repositories."
  exit 2
fi

sudo yum install git rpm-build python3 python3-ovirt-engine-sdk4 python3-openstackclient -y
sudo pip3 install six cryptography python-dateutil
rm -rf pyghmi 2>/dev/null
git clone https://opendev.org/x/pyghmi.git
cd pyghmi
python3 setup.py bdist_rpm
sudo yum remove pyghmi -y
sudo rpm -ivh dist/pyghmi-*.noarch.rpm

echo "In order for this to work with Openstack, you must copy the CA certificate to /etc/pki/ca-trust/source/anchors/ and run update-ca-trust extract as root prior to using virtbmc.py"
