# Emulate Android apps on Ubuntu Linux

When demoing the DHIS 2 Capture Android application (and other Android apps), it is quite useful to be able to display the phone screen on your local machine, so that the screen can be shared on video conference calls or projectors. A great way to do so is to emulate the Android app on your local machine. The [scrcpy](https://github.com/Genymobile/scrcpy) application from *Genymotion* is a good choice as it works on Windows, Mac and Linux. For Ubuntu 18.04 and later it is available as a *snap* package. This guide explains how to install scrcpy on Ubuntu from the command line and connect to your Android device.

## Steps

1. Ensure you have *snapd* installed on your system. If not, install it with:

   ```
   $ sudo apt update
   $ sudo apt install snapd
   ```

2. Install scrcpy with this command:

   ```
   $ sudo snap install scrcpy
   ```

   Verify the location of the scrcpy installation with this command:

   ```
   $ which scrcpy
   ```

4. Connect your Android device to your local machine using a USB cable.

5. A dialog called **Use USB to** will appear. Select the **Transfer files** option.

6. Enable USB debugging on the Android device. 

   1. On the Android device, open the **Settings** app.
   2. In the settings app, search for **About phone** and navigate to that screen.
   3. Tap the **Build number** option 7 times.
   4. Search for **Developer options** and navigate to that screen.
   5. Under **Debugging**, enable **USB debugging**.

6. Start scrcpy with this command:

   ```
   scrcpy
   ```

   This will open the scrcpy app and display the Android device on your local machine.