# Nictotine+ for Raspberry Pi

Yet another [realies/soulseek-docker](https://github.com/realies/soulseek-docker ) fork! 
kokmok made a great RPI fork, but unfortunately hasn't updated it in 5 years, so that's where this repo comes in! Latest image uses Nicotine+ v3.3.2, and the Dockerfile allows for rebuilding with future versions. Huge thanks again to [realies](https://github.com/realies) for all the hard work of getting soulseek to work over noVNC, and [kokmok](https://github.com/kokmok/rpi-nicotine-novnc) for giving me clues to get this working.


![image](https://github.com/hockeygoalie35/nicotine-novnc-rpi/assets/7758029/2aab8653-9dd9-49c5-95a3-802acb4e9c29)



## Setup

Here's a recommended file structure on your raspberry pi:

```
home/pi/Appdata
  -> nicotine
     -->downloads
     -->incomplete  # Optional
     -->received    # Optional
     -->shares
```
Here's a bash script that will do just that in `home/pi/`
```bash
cd
mkdir Appdata
cd Appdata
mkdir nicotine
cd nicotine
mkdir downloads
mkdir incomplete
mkdir received
mkdir shares
```

# Container Setup
## Docker Compose
Now edit docker-compose.yml, changing the `- /path/to/Nicotine/data` to your newly created data directory, etc.
If needed, change the UID and GID to match your user. It is advised not to run this container as root.
Then in the project directory, run `docker compose up`

## Portainer
Copy the contents of docker-compose.yml and paste it into a stack, changing the paths and UID/GID as above. 

Once the container is up and running, in your web browser go to RPIHOSTNAME:6080 and you should be greeted with Nicotine+

# *Important*
After the first boot up, Nicotine will create a default config file, which sets header_bar to TRUE. For whatever reason, this header bar doesn't show up in the noVNC window. I've written a python script that monitors the file and sets header_bar to FALSE, which brings the search bar and other tabs back into the GUI. Once it changes the config, restart the container with `docker restart nicotine`


## Before - Lack of search bar
![image](https://github.com/hockeygoalie35/nicotine-novnc-rpi/assets/7758029/03142e3d-2786-4eb3-bbaa-eac91898ea70)



## Container STDOUT - py script fixing config
![image](https://github.com/hockeygoalie35/nicotine-novnc-rpi/assets/7758029/8b17c14d-c562-46bd-95bd-387918107de2)


## After - Search bar restored after restart

![image](https://github.com/hockeygoalie35/nicotine-novnc-rpi/assets/7758029/76a59778-0133-4950-8a9b-e5fdf7e289d5)


If for whatever reason the script doesn't fix it, you can go to: data/.config/nicotine/ and edit config, setting: header_bar = False


