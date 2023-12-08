# Raspberry Pi Camera Preview Setup

This script initializes a camera preview on boot for a Raspberry Pi 4 with a connected camera module. It is designed to work with a clean Raspberry Pi OS Lite installation (without a desktop environment) on an SD card. Follow the steps below to set up the camera preview:

1. **Prepare Your Raspberry Pi:**
   - Begin with a clean Raspberry Pi OS Lite installation on an SD card.
   - Plug in your camera module and SD card to the Pi, then boot up the Pi.
   - Information on setting up the OS can be found [here](https://www.raspberrypi.com/software/).

2. **Clone the Git Repository:**
   - Open a terminal on your Raspberry Pi.
   - Clone this git repository using the following command:

     ```bash
     git clone https://github.com/bryantb2/Pi-Camera-Preview.git
     ```

3. **Run the Setup Script:**
   - Navigate to the cloned repository:

     ```bash
     cd Pi-Camera-Preview
     ```

   - Make the setup script executable:

     ```bash
     chmod +x configure_readonly.sh
     ```

   - Execute the setup script with root privileges:

     ```bash
     sudo ./configure_readonly.sh
     ```

   The script will install the necessary packages, configure the camera startup behavior, and set the Pi into "kiosk mode," preventing users from tampering with the configuration.

Note: Ensure that you have a basic understanding of the Raspberry Pi and its setup before proceeding with these steps.