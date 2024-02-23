# Use this file to start the preview window on boot


# Extract width and height from the resolution
resolution=$(fbset -s | grep "geometry" | awk '{print $2, $3}')
width=$(echo $resolution | cut -d ' ' -f 1)
height=$(echo $resolution | cut -d ' ' -f 2)

# Open Pi camera preview
# OLD WAY: rpicam-hello -t 0 --info-text 0 -f --flush --denoise auto --width $(($width)) --height $(($height)) --autofocus-speed fast

# TEMP: /usr/bin/python3 ~/stereo-stream.py $(($width)) $(($height))