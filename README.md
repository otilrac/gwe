# GWE
GWE is a GTK system utility designed to provide information, control the fans and overclock your NVIDIA video card 
and graphics processor.

<img src="/art/screenshot-1.png" width="800"/>

## TODO

- [x] Show general GPU info
- [x] Show power info
- [x] Show clocks info
- [x] Show GPU temp in both app and app indicator
- [x] Show fan info
- [x] Allow to hide main app window
- [x] Add command line option to start the app hidden
- [x] Add Refresh timeout to settings 
- [x] Add command line option to add desktop entry
- [x] About dialog
- [x] Distributing with PyPI
- [x] Show chart of selected fan profile
- [x] Allow to select and apply a fan profile
- [x] Add/Delete/Edit multi speed fan profiles (fan curve)
- [x] Add option to restore last applied profile on startup
- [x] Find better icons for app indicator
- [x] Try to lower resource consumption (mostly caused by `nvidia-settings` invocations)
- [x] Show historical data of most important values in a separate dialog (requires GTK 3.24/GNOME 3.30)
- [ ] Disable unsupported preferences
- [x] Distributing with Flatpack
- [ ] Publishing on Flathub
- [ ] Distributing with Snap
- [ ] Add support for multi-GPU
- [ ] Allow to select profiles from app indicator
- [ ] Add support for i18n (internationalization and localization)

## How to help the project
### Discord server
If you want to help testing or developing it would be easier to get in touch using the discord server of the project: https://discord.gg/YjPdNff  
Just write a message on the general channel saying how you want to help (test, dev, etc) and quoting @leinardi. If you don't use discor but still want to help just open a new issue here.

### We need people with experience in at least one of these topics:
 - X-Protocol (see [#15](https://gitlab.com/leinardi/gwe/issues/15) and [#16](https://gitlab.com/leinardi/gwe/issues/16))
 - Flatpak (see [#17](https://gitlab.com/leinardi/gwe/issues/17))
 - Snap (see [#18](https://gitlab.com/leinardi/gwe/issues/18))
 - Meson (see [#2](https://gitlab.com/leinardi/gwe/issues/2))

Knowing Python will be also very helpful but not strictly necessary.
 
### Why do we need it?
Currently there are some roadblocks that are preventing GWE to move to stable and have an official launch.  
The biggest issues right now are related to the X-Protocol implementation and the distribution of the application.

#### X-Protocol
To make the app as lightweight as possible, GWE uses the X-Protocol to communicate directly with [NV-CONTROL](https://github.com/NVIDIA/nvidia-settings/blob/master/doc/NV-CONTROL-API.txt).  
The code that implements the X-Protocol was taken form [disper](https://github.com/phatina/disperd/blob/master/src/nvidia/minx.py),
a Python 2 software, and ported to Python 3. The current implementation is only able to read data ([#16](https://gitlab.com/leinardi/gwe/issues/16)) and has to relay
on the `nvidia-settings` binary to set values (e.g. fan speed or overclock). Also the reading is not 100% reliable due to [#15](https://gitlab.com/leinardi/gwe/issues/15).  
It would be really helpful if someone with more knowledge of the X-Protocol or Python could help fixing these two issues.

## Dropped PyPI support
Development builds were distributed using PyPI. This way of distributing the software is quite simple
but requires the user to manually install all the non Python dependencies like cairo, glib, appindicator3, etc.  
The current implementation of the historical data uses a new library, Dazzle, that requires Gnome 3.30 which is only
available, for example, with Ubuntu 18.10 making the latest Ubuntu LTS unsupported.  
A possible solution for all this problems could be distributing the app via Flatpak, since with it all the dependencies
will be bundled and provided automatically.
**No new build will be published on PyPI**.

## Installing the app via Flatpak
Until the app will be published on Flathub, to install it you have do manually download the latest `.flatpak` file
and install it with command:
```bash
flatpak --user install <path to the file .flatpak>
```
If you don't have Flatpak installed you can find step by step instructions [here](https://flatpak.org/setup/).

## Application entry
To add a desktop entry for the application run the following command (not supported by Flatpak):
```bash
gwe --application-entry 
```
If you don't want to create this custom rule you can run gwe as root 
(using sudo) but we advise against this solution.

## Command line options

  | Parameter                 | Description|                              | Flatpak | 
  |---------------------------|-------------------------------------------|---------|
  |-v, --version              |Show the app version                       |    x    |
  |--debug                    |Show debug messages                        |    x    |
  |--hide-window              |Start with the main window hidden          |    x    |
  |--application-entry        |Add a desktop entry for the application    |         |
  |--autostart-on             |Enable automatic start of the app on login |         |
  |--autostart-off            |Disable automatic start of the app on login|         |


## How to run the repository sources
If you wnat to clone the project and run directly from the source you need to manually install all the needed
dependencies.
 
### (K/X)Ubuntu 18.04 or newer
```bash
sudo apt install python3-pip libcairo2-dev libgirepository1.0-dev libglib2.0-dev libdazzle-1.0-dev gir1.2-gtksource-3.0 gir1.2-appindicator3-0.1 python3-gi-cairo python3-pip
```
### Fedora 28+ (outdated, please let me know if new dependencies are needed)
Install [(K)StatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/)

### Arch Linux (Gnome)
```bash
sudo pacman -Syu python-pip libdazzle libappindicator-gtk3
```

### Python dependencies
```
git clone https://gitlab.com/leinardi/gwe.git
cd gwe
pip3 install -r requirements.txt
./run.sh
```

## FAQ
### Why the memory overclock offsets effectively applied do not match the one set in the Nvidia Settings app?
Because Memory Transfer Rate, what Nvidia Settings reports and changes, 
is different from the effective Memory Clock, what is actually being 
displayed by GWE. It is also what other Windows applications like MSI Afterburner show.
The Memory Transfer Rate is simply double the Memory Clock.

## How can I support this project?

The best way to support this plugin is to star it on both [GitLab](https://gitlab.com/leinardi/gwe) and [GitHub](https://github.com/leinardi/gwe).
Feedback is always welcome: if you found a bug or would like to suggest a feature,
feel free to open an issue on the [issue tracker](https://gitlab.com/leinardi/gwe/issues).

## License
```
This file is part of gwe.

Copyright (c) 2018 Roberto Leinardi

gwe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gwe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gwe.  If not, see <http://www.gnu.org/licenses/>.
```