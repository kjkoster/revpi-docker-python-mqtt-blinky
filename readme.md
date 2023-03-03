# A Revolution Pi Blinky in Python with Docker and MQTT

This is a showcase project, to get you started with Python on Docker on a
Revolution Pi, using MQTT as the communications backbone.

If you follow this tutorial, you will end up with a blinking LED on the front of
our Revolution Pi, controlled from a Python program, running in a Docker
container, sending commands to revpipyload via MQTT.

Before you can use this blinky, we have to install Docker and Docker Compose. I
suggest you update your system to the latest using `apt`, but that is really up
to you. I always do, but others prefer otherwise.

## Set System Timezone to UTC (Optional)

Older Revolution Pi images use a non-UTC timezone, which is not ideal for system
components. Setting your system to use UTC is optional, but highly advisable.

```
$ sudo timedatectl set-timezone UTC
```

See also https://www.youtube.com/watch?v=-5wpm-gesOY

## Install Docker and Docker Compose

To install Docker, we use Docker's convenience script. That seems to be the most
reliable way to install Docker. It is generally not a good idea to pipe the
output of a file downloaded from the Internet into a `sudo` shell, yet here we
are...

```
$ curl -fsSL https://get.docker.com | sudo sh
```

After the installation is complete, we have to grant the `pi` user the
privileges to run docker containers.

```
$ sudo usermod -aG docker ${USER}
$ exit
```

Log off and log in again for the change in groups to take effect.

```
$ docker run hello-world
```

Fix any issues you see before proceeding. If this works nicely, you can proceed
to installing Docker Compose. If not, did you log out and in again?

```
$ sudo apt install docker-compose
```

## Configure RevPiPyLoad

The interface between the Revolution Pi hardware and MQTT is handled by
[RevPiPyLoad](https://revpimodio.org/en/revpipyplc-2/revpipyload/). It will need
to know where to find the MQTT broker and what the broker's password is. MQTT is
not enabled by default, so you will have to enable it too.

This project includes a working copy of `revpipyload.conf`, but it is probably
better that you make these changes yourself. You need four changes and I
included an optional one.

`mqtt = 1` enables the MQTT bridge. `write_outputs = 1` allows you to not just
read data from MQTT, but also control outputs via MQTT. This demo project uses
that to control the leds on the front of your Revolution Pi. `username` and
`password` should match the ones in your `.env` file and in
`mosquitto/config/password.txt`.

Optionally, you can set `sendinterval` to a lower value, in seconds. I usually
set it to 1 second. If you need higher resolution logging, you can experiment
with `send_on_event`.

After making changes, restart the hardware to MQTT bridge as follows:

```
$ sudo vi /etc/revpipyload/revpipyload.conf
$ sudo service revpipyload restart
```

## Start the Blinky

Running the blinky is now a matter of starting the Docker containers:

```
$ docker-compose up
```

## Configure PiCtory

While the factory default settings for PiCtory is enough to make this tutorial
work, you will probably have to make changes as you add I/O modules or rename
ports. Whether or not data is exposed on MQTT is controlled by the `Export`
checkboxes, on the bottom right of PiCtory.

After toggling a checkbox, be sure `file -> save as start config` and
`tools -> reset driver`.

## MQTT Snooping

There are many good MQTT tools out there. My personal favourite is
[MQTT Explorer](http://mqtt-explorer.com), which I recommend you try out now. It
will give you good insight in what your Revolution Pi is doing.

This ends the blinky tutorial. Please let me know what you think.

