#!/bin/sh

#Fetch and build rtl-sdr
echo "***** building rtl-sdr *****"
cd /usr/src/app
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr/
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
make
sudo make install
sudo ldconfig
cd ../..
echo "***** finished building rtl-sdr *****"

echo "***** building rtl-433 *****"
git clone https://github.com/merbanan/rtl_433.git
cd rtl_433
mkdir build
cd build
cmake ..
make
make install
cd ../..
echo "***** done building rtl_433"
pip3 install influxdb3-python
pip3 install requests


