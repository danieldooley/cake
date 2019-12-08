# Birthday Cake

## Anaconda

Should be able to use `environment.yml` to setup a conda environment to be able to run `main.py`:
```
$ conda env create -f environment.yml
```

## Fonts

`main.py` references a system font `Seven Segment` which can be downloaded from: https://www.dafont.com/seven-segment.font

How to install this font will vary based on your OS

## Quitting

Pressing the *Escape* key will cause the program to exit.

# The RPi Saga

This was required to run on a Raspberry Pi. Some things that needed to be installed:

Tk for use with tkinter:
```
sudo apt-get install tk-dev
```

After downloading the `Seven Segment` font:
```
$ mkdir ~/.fonts
$ mv Seven\ Segment.ttf ~/.fonts/
$ ch ~/.fonts ; mkfontscale ; mkfontdir ; xset fp+ `pwd`
```

We also need `Arial` from:
```
$ sudo apt-get install ttf-mscorefonts-installer
```

## Anaconda Problems

I tried installing miniconda but quickly ran into issues that the version of `tkinter` that Anaconda installs (builds?) does not support the right font things to be able to load custom (or even remotely nice looking) fonts. So I fell back to the default `python3` install (3.7.3?) which has the right font things in `tkinter`.
