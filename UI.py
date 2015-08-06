from ttk import *
import Tkinter as tk
from Volume import volume

def smallest(list1,list2):
    if len(list1)<=len(list2):
        return len(list1)
    if len(list2)<len(list1):
        return len(list2)

def syssetvol(*args):
    if len(applayout):
        for index in xrange(len(applayout)):
            actualappvol = (applayout[index][1].get() / volcontrol.systemvol)
            if actualappvol >= 1:
                volcontrol.setvol(args[0])
                sysvol.set(int((float(args[0]))))
                applayout[index][1].set(volcontrol.systemvol)
                print 'if is happening'
            else:
                volcontrol.setvol(args[0])
                sysvol.set(int((float(args[0]))))
                applayout[index][1].set(actualappvol * volcontrol.systemvol)
                print 'else is happening'
    else:
        volcontrol.setvol(args[0])
        sysvol.set(int((float(args[0]))))

    # extra code to ensure app vol scale and system vol scale are synchronized (like Windows volume mixer)

def getsysvolloop():
    if len(applayout):
        for index in xrange(len(applayout)):
            actualappvol = (applayout[index][1].get() / volcontrol.systemvol)
            if actualappvol >= 1:
                volcontrol.getsysvol()
                sysvolscale.set(volcontrol.systemvol)
                applayout[index][1].set(volcontrol.systemvol)
            else:
                volcontrol.getsysvol()
                sysvolscale.set(volcontrol.systemvol)
                applayout[index][1].set(actualappvol * volcontrol.systemvol)
    else:
        volcontrol.getsysvol()
        sysvolscale.set(volcontrol.systemvol)

    root.after(1000, getsysvolloop)

    # extra code to ensure app vol scale and system vol scale are synchronized (like Windows volume mixer)

def createlayout():
    if len(applayout):
        oldlist = volcontrol.applist
        volcontrol.updateapps()
        for index in xrange(smallest(oldlist,volcontrol.applist)):
            if oldlist[index] == volcontrol.applist[index]:
                pass
            else:
                volcontrol.getsysvol()
                applayout[index][1].set(volcontrol.systemvol)
                applayout[index][0].destroy()
                applayout[index][1].destroy()
                applayout[index][2].destroy()
                exec ('def vol(*args):\n    applayout[%d][2].set( int((float(args[0]))) )\n    volcontrol.setvol\
                (%s, args[0])' % (index, volcontrol.applist[index]))
                appfunc[index] = vol
                applayout[index] = [Label(sysvolframe, text=volcontrol.applist[index]), \
                                    Scale(sysvolframe, from_=100, to=0, orient='vertical', command=appfunc[index]), \
                                    Label(sysvolframe), \
                                    tk.StringVar()]
                applayout[index][2]['textvariable']= applayout[index][3]
                applayout[index][0].grid(column=(index + 1), row=0)
                applayout[index][1].grid(column=(index + 1), row=1)
                applayout[index][2].grid(column=(index + 1), row=2)
                volcontrol.getsysvol()
                applayout[index][1].set(volcontrol.systemvol)
        if len(oldlist) > len(volcontrol.applist):
            for index in xrange(len(volcontrol.applist, len(oldlist))):
                volcontrol.getsysvol()
                applayout[index][1].set(volcontrol.systemvol)
                applayout[index][0].destroy()
                applayout[index][1].destroy()
                applayout[index][2].destroy()
                del applayout[index]
                del appfunc[index]
        if len(oldlist) < len(volcontrol.applist):
            for index in xrange(len(oldlist, len(volcontrol.applist))):
                exec ('def vol(*args):\n    applayout[%d][3].set( int((float(args[0]))) )\n    volcontrol.setvol\
                (%s, args[0])' % (index, volcontrol.applist[index]))
                appfunc[index] = vol
                applayout.append([Label(sysvolframe, text=volcontrol.applist[index]), \
                                    Scale(sysvolframe, from_=100, to=0, orient='vertical', command=appfunc[index]), \
                                    Label(sysvolframe), \
                                    tk.StringVar()])
                applayout[index][2]['textvariable']= applayout[index][3]
                applayout[index][0].grid(column=(index + 1), row=0)
                applayout[index][1].grid(column=(index + 1), row=1)
                applayout[index][2].grid(column=(index + 1), row=2)
                volcontrol.getsysvol()
                applayout[index][1].set(volcontrol.systemvol)
        print 'went to if'
    else:
        print 'feeze>>>??'
        volcontrol.updateapps()
        print 'went to else'
        if volcontrol.applist:
            for index in xrange(len(volcontrol.applist)):
                exec ('def vol(*args):\n    applayout[%d][3].set( int((float(args[0]))) )\n    volcontrol.setvol\
                (args[0], "%s")' % (index, volcontrol.applist[index]))
                appfunc[index] = vol
                applayout.append([Label(sysvolframe, text=volcontrol.applist[index]), \
                                Scale(sysvolframe, from_=100, to=0, orient='vertical', command=appfunc[index]), \
                                Label(sysvolframe), tk.StringVar()])
                applayout[index][2]['textvariable']= applayout[index][3]
                applayout[index][0].grid(column=(index + 1), row=0)
                applayout[index][1].grid(column=(index + 1), row=1)
                applayout[index][2].grid(column=(index + 1), row=2)
                volcontrol.getsysvol()
                applayout[index][1].set(volcontrol.systemvol)
    root.after(10000,createlayout)

volcontrol = volume()
appfunc = {}
applayout = []
root = tk.Tk()
sysvol = tk.StringVar()
frame = Frame(root, padding=(4,8,4,4))
sysvolframe = Frame(frame, padding=(2,4), borderwidth=2, relief = 'groove')
sysvolscale = Scale(sysvolframe, from_=100, to=0, orient='vertical', command=syssetvol)
sysvollabel = Label(sysvolframe, textvariable=sysvol)

frame.grid(column=0, row=0, sticky="nswe")
sysvolframe.grid(column=0, row=0, sticky='nswe')
Label(sysvolframe, text='System').grid(column=0, row=0)
sysvolscale.grid(column=0, row=1)
sysvollabel.grid(column=0, row=2)

sysvol.set(sysvolscale.get())

getsysvolloop()
createlayout()

root.mainloop()

