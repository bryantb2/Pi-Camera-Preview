# Run this script to configure the environment for the project
echo '-------------------------------------'
echo 'Setup utility ------- beginning configuration process'
echo '-------------------------------------'

wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
chmod +x copy_and_fill.sh

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
./install_pivariety_pkgs.sh -p imx519_kernel_driver
git clone https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver.git

echo '-------------------------------------'
echo 'Setup utility ------- initializing camera startup script'
echo '-------------------------------------'

cp ./scripts/camera_startup.sh s/home/pi/startup_camera
chmod +x startup_camera

echo '-------------------------------------'
echo 'Setup utility ------- forcing Pi into readonly mode'
echo '-------------------------------------'

# Setup the environment for readonly operations
chmod +x configure_readonly.sh
sudo ./configure_readonly.sh

echo '-------------------------------------'
echo 'Setup utility ------- finished configuration, restarting system'
echo '-------------------------------------'

sudo reboot


