gif-music-visualizer
====================
Visualization of live audio using gifs. This is based on Scott W Harden's ["Realtime FFT Audio Visualization with Python"](http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/).

Prepare gif
-----------
#### You can use dough, watermelon or add a new gif like this:

Use ImageMagick:
`convert -coalesce image.gif image.jpg`

Create a directory in the `frames` subdirectory and copy the image frames into it.

**If you found a cool gif, please send me a message/pull request. Thanks!**

Dependencies
------------
* pygame
* scipy
* numpy
* pyaudio

#### Debian:
```
apt-get install python-pygame python-scipy python-numpy python-pyaudio
```

Usage
-----
Play some audio and run visualizer.py. Press F11 to toggle full-screen mode. Use Escape to exit.

> Visualization moves but no audio playing?

I had to use pavucontrol (PulseAudio Volume Control `apt-get install pavucontrol`) to select "Analog Stereo Output" instead of "Analog Stereo Duplex" (Configuration tab). If you want to use an external input device (like a microphone) use "Analog Stereo Input".

Demo
----
I uploaded some demos to [YouTube](https://www.youtube.com/channel/UC_ndlMTsT9kaZq_8uoC3RiQ).

Links
-----
Read the [corresponding blog post](http://randomprojects.de/blog/gif-music-visualization/) for further details.
