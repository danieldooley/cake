import tkinter as tk
from tkinter import ttk
import requests


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.setup()
        self.lastquakecount = 0

    def setup(self):
        # Set app to be full screen
        self.master.wm_attributes('-fullscreen', 1)

        # Exit app on <Escape> press
        self.master.bind('<Escape>', self.exit)

        # Create a ttk style because styling the tk window doesn't work on macos?
        style = ttk.Style(root)
        style.theme_use('classic')
        style.configure('TFrame', background='black')
        style.configure('TLabel', background='black', foreground='red', font=('Helvetica', '60'))
        style.configure('info.TLabel', font=('Helvetica', '40'))
        style.configure('count.TLabel', font=('Seven Segment', '400'))

        # Create frames to have a black background with padding
        base = ttk.Frame(self.master)
        base.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        frame = ttk.Frame(base)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, padx=50, pady=50)

        # Create a small label to have static text
        lbl = ttk.Label(frame, text="Quakes Located by the NGMC:")
        lbl.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)

        # Create the large label to contain quake count
        self.countlbl = ttk.Label(frame, text="Loading...", anchor="center", style="count.TLabel")
        self.countlbl.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        # Create another small label to contain quake info
        self.infolbl = ttk.Label(frame, text="Latest Quake:\n", style="info.TLabel")
        self.infolbl.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.NO)

        # Start a loop of requesting quake info
        self.master.after(10, self.getquakes)

    def drawcounttext(self, todisplay):
        self.countlbl.config(text=todisplay)

    def drawinfotext(self, todisplay):
        self.infolbl.config(text=todisplay)

    def getquakes(self):
        # Blocking I/O request in a GUI thread - naughty :D
        r = requests.get("https://quakesearch.geonet.org.nz/count?startdate=2018-12-12T1:00:00")

        if r.status_code != 200:
            self.drawcounttext("ERROR")
            print("ERROR: Failed to retrieve quake count (status: %d):" % r.status_code)
            print(r.text)
            return

        data = r.json()
        c = data["count"]
        self.drawcounttext(c)
        self.master.after(5000, self.getquakes)

        if c <= self.lastquakecount:
            return

        self.lastquakecount = c

        # Get latest quake details:
        r = requests.get("https://api.geonet.org.nz/quake?MMI=-1")

        if r.status_code != 200:
            self.drawcounttext("ERROR")
            print("ERROR: Failed to retrieve quake info (status: %d):" % r.status_code)
            print(r.text)
            return

        data = r.json()
        self.drawinfotext("Latest Quake:\nMagnitude %.1f, %s" % (
            data["features"][0]["properties"]["magnitude"], data["features"][0]["properties"]["locality"]))

    def exit(self, event):
        self.master.destroy()


root = tk.Tk()
app = FullScreenApp(root)
root.mainloop()
