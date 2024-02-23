# Run this script to configure the environment for the project
echo '-------------------------------------'
echo 'Setup utility ------- beginning configuration process'
echo '-------------------------------------'

wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh

echo '-------------------------------------'
echo 'Setup utility ------- updating system'
echo '-------------------------------------'

sudo apt-get update && apt-get upgrade

echo '-------------------------------------'
echo 'Setup utility ------- installing camera packages'
echo '-------------------------------------'

# Setup the environment for running the Pi cameras
# https://dronebotworkshop.com/pi-autofocus/
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
./install_pivariety_pkgs.sh -p imx519_kernel_driver_low_speed
./install_pivariety_pkgs.sh -p imx519_kernel_driver
git clone https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver.git

echo '-------------------------------------'
echo 'Setup utility ------- initializing camera startup script'
echo '-------------------------------------'

rm -rf ~/stereo-stream
rm -rf ~/camera_startup
cp ./scripts/camera_startup.sh ~/camera_startup
cp ./logic/stereo-stream.py ~/stereo-stream
chmod +x ~/stereo-stream
chmod +x ~/camera_startup
sudo cp ./scripts/system_startup.sh /etc/rc.local

echo '-------------------------------------'
echo 'Setup utility ------- forcing Pi into readonly mode'
echo '-------------------------------------'

# Setup the environment for readonly operations
chmod +x readonly_setup.sh
sudo ./readonly_setup.sh

echo '-------------------------------------'
echo 'Setup utility ------- finished configuration, restarting system'
echo '-------------------------------------'

sudo reboot


