__author__ = 'Ongkong'
import subprocess
# the system volume is universal ie 100 vol for itunes and 50 vol systemwide is 50vol for itunes
class volume:
    applist = []
    systemvol = None

    def __init__(self):
        self.updateapps()
        self.getsysvol()

    def getsysvol(self):
        termcommand = ['osascript','-e','set ovol to output volume of (get volume settings)']
        volume.systemvol = float(subprocess.check_output(termcommand))

    def updateapps(self):
        print 'not freeze'
        applist = []
        termcommand = ['osascript','-e','tell application "System Events" to get name of (processes where background only is false)']
        applist = subprocess.check_output(termcommand).split(', ')
        # creates list of opened doc apps
        print 'not freeze 1'
        applist[len(applist)-1] = applist[len(applist)-1]\
            [0:len(applist[len(applist)-1])-1]
        print 'not freeze 2'
        # takes away new line char at the end of last list item
        #if 'Python' in applist:
            #volume.applist.remove('Python')
        novolapps = []
        # list of unusable apps
        for app in applist:
            termcommand = ['osascript','-e', 'tell application "%s" to set sound volume to 100' % app]
            if subprocess.Popen(termcommand, stderr=subprocess.PIPE).communicate()[1]:
                novolapps.append(app)
            # try:
            #     subprocess.check_output(termcommand)
            # except:
            #     novolapps.append(app)
        print 'not freeze 3'
        # determine unusable apps
        for app in novolapps:
            applist.remove(app)
        # remove unusable apps from applist
        volume.applist = applist
        # assign applist to global applist varibale(volume.applist)

    def setvol(self, vol, app=None):
        vol = float(vol)
        if app:
            # app volume is relative to system volume
            if vol >= volume.systemvol:
                termcommand = ['osascript','-e', 'set volume output volume %d' % vol]
                subprocess.call(termcommand)
                volume.systemvol = vol
                # change system volume
                termcommand = ['osascript','-e', 'tell application "%s" to set sound volume to %d' % (app,100)]
                subprocess.call(termcommand)
                # makes sure app volume is 100% of system volume (or follows system volume)
            else:
                relativevol = (vol/volume.systemvol)*100
                volume.applist
                termcommand = ['osascript','-e', 'tell application "%s" to set sound volume to %d' % (app,relativevol)]
                subprocess.call(termcommand)
                # changes the vol of application RELATIVE to the systemvol

        # all volume (system or app) is based on a system volume number.
        # ex: say system volume is at 50 and you want app volume to be 50% of that or 25. all you type
        # is setvol(25, app) instead of setvol(50, app).
        # It's easier for the user to follow and is more natural in logic.
        # (windows volume mixer implements the same logic)
        else:
            termcommand = ['osascript','-e', 'set volume output volume %d' % vol]
            subprocess.Popen(termcommand)
            volume.systemvol = vol

if __name__ == '__main__':
    new = volume()
    print new.systemvol
    new.setvol(50)
    print new.systemvol
    new.setvol(50, 'itunes')
    print new.systemvol, 'supposed to be 50 still'
    new.setvol(25, 'itunes')
    print new.systemvol, 'supposed to be 50 still (relative itunes vol is 25)'
    new.setvol(100, 'itunes')
    print new.systemvol, 'supposed to be 100'
