![](https://raw.githubusercontent.com/nikgapps/nikgapps.github.io/master/images/nikgapps-logo.webp)

## Introduction

NikGapps project started with the goal to provide custom gapps packages that suits everyone's needs. A gapps package which is completely configurable, allows you to install exactly the set of google apps you want and It comes in 6 variants.   

Here are some feature highlights:
- NikGapps is a gapps package built from my own device. As my device is always updated with the latest version of Google Apps, every time I build a new package, I am on latest and stable version of Google Apps
- NikGapps also comes with Android Go package for low-end devices.
- NikGapps is a bit different from other Gapps packages (written from scratch, it isn't a port of OpenGapps). It focuses on providing apps that most of the people uses but can't find it in other Gapps packages and ends up installing the apps manually
- NikGapps doesn't have stock YouTube, instead it has YouTube vanced (v14 with separate addons for v15). It doesn't have Pixel Launcher, instead it has Lawnchair launcher (Till Android Q, discontinued starting Android R)
- NikGapps supports split-apks
- NikGapps also comes with nikgapps.config and debloater.config which allows you to control your installation and de-bloat unnecessary stuff from your Rom respectively.
- NikGapps is built on a different architecture, the installation method is completely different (Every Package comes with a installer.sh that installs itself). Also, it installs the gapps to /product partition instead of /system partition
- NikGapps also allows you to configure the installation, it can be installed to any partition (be it /system or /product or any other partition which may get added in future)
- NikGapps also allows you to keep the aosp counterpart of google app if you want (just by using nikgapps.config you can choose whether to remove the aosp counterpart or remove it)
- NikGapps allows you to dirty flash it anytime you want, it also supports installing on top of Roms with Gapps (except for the pixel flavored Roms)
- NikGapps also comes with addon packages (useful ones) so that users don't have to flash the whole gapps package just to have the app installed.
- Unlike few other gapps packages, NikGapps doesn't disable the Privileged Permission Whitelisting property, providing the necessary permissions to the privileged apps.
- It supports addon.d, so you need not flash the package again and again after every nightly flash
- NikGapps addon.d functionality is built from scratch which allows you to completely control which app you want to back up/restore on dirty flash.
- It also allows optimizing Google Play Services (when you turn off Find My Device) so that you can sleep with peace without having to worry about Google play services eating your battery. (Requires support from Rom too in order to work)

## For Developers
[![](https://img.shields.io/badge/NikGapps%20-How%20to%20fetch%20App%20Updates-blue)](https://github.com/nikgapps/build)

## Total Downloads  
<img alt="SourceForge" src="https://img.shields.io/sourceforge/dt/nikgapps?label=Total%20Downloads&color=red"> <img alt="SourceForge" src="https://img.shields.io/sourceforge/dd/nikgapps?label=Downloads%20Per%20Day&color=blue">