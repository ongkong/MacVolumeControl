# MacVolumeControl
Python class to fine tune system volume and individual app volume. GUI by Tkinter included that mimics Windows Volume Mixer behavior.

# Disclaimer
The class can only set volumes of compatible apps (known so far: Spotify and iTunes). Unfortunately, setting the volume of every app individually would require C or C++ according to my limited understanding. So, sorry you can't set the individual volumes of web browsers. :disappointed_relieved: 

# General Usage
Creating a new class.
````
control = Volume()
````
Enter only the first parameter in setvol() to set System Volume.
````
control.setvol(50)
````
Enter the name of the app as the second parameter.
````
control.setvol(70, 'itunes')
````
NOTE: If the System Volume is 50 as set by the previous line of code, this line of code would raise the System Volume to 70 as well. If the number was lower than the System Volume, then only the app's volume will be affected.

# GUI Making
The class tries to compile a list of apps whose volumes can be set with
````
control.updateapps()
````
and stores the volumes in the variable applist.

Likewise, the value of System Volume is stored in the variable systemvol and set by
````
control.getsysvol()
````

# Problems with Included Tkinter GUI
Simply put, it is not smooth like the Volume Mixer in Windows. There is always a slight delay.

The GUI also often freezes at the below lines of code, but sometimes is able to solve itself.
````
for app in applist:
    termcommand = ['osascript','-e', 'tell application "%s" to set sound volume to 100' % app]
    if subprocess.Popen(termcommand, stderr=subprocess.PIPE).communicate()[1]:
        novolapps.append(app)
````

The reason for this delay is that the GUI has to constantly call a function to check any volume changes and update the visual bars (like if you changed the volume using the buttons on the keyboard). 
