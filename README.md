# virtbmc - Extension of pyghmi project (https://opendev.org/x/pyghmi.git) to provide basic BMC functionalities for instances on RHV/oVirt & Openstack

**Configuration:**

Clone this repository:
```
git clone https://github.com/dsorrentino/virtbmc.git
```

Execute Setup:
```
cd virtbmc
./setup.sh
```

Create the basic configuration file:
```
sudo mkdir -p /etc/virtbmc
sudo cp etc/sample_virtbmc.conf /etc/virtbmc/virtbmc.conf
```

Configure virtbmc for your environment:
```
sudo vi /etc/vurtbmc/virtbmc.conf
```

**Execution:**

Once you have configured virtbmc for you environment, execute the program:
```
sudo python3 ./virtbmc.py
```
