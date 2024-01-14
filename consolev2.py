import wx
from threading import *

# define status for autonomous
auto_stat = "NO"
autonomous = False

# define status for manual
man_stat = "NO"
manual = False

# define status for mission
mission_stat = ""
status = ""
mission = "None"

# define status for kill
kill_stat = "YES"
kill = False

# define status for heartbeat
hb_stat = "OK"
hb = ""

# functions for missions
ID_MISSION_1 = wx.NewId()
ID_MISSION_2 = wx.NewId()
ID_MISSION_3 = wx.NewId()
ID_MISSION_4 = wx.NewId()
ID_MISSION_5 = wx.NewId()


class statuses(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        global autonomous
        global auto_stat
        global manual
        global man_stat
        global mission
        global status
        global mission_stat
        global kill
        global kill_stat
        global hb
        global hb_stat
        while frame.IsShown():
            # autonomous status
            if autonomous:
                auto_stat = "YES"
            else:
                auto_stat = "NO"

            # manual status
            if manual:
                man_stat = "YES"
            else:
                man_stat = "NO"

            # mission status
            if mission == "None":
                status = ""
            elif mission == "":
                status = "Failed"
            else:
                status = "Deployed"
            mission_stat = mission + status

            # kill status
            if kill:
                kill_stat = "YES"
            else:
                kill_stat = "NO"

            # heartbeat status
            if hb == "None":
                hb_stat = "MISSED"
            else:
                hb_stat = "OK"


class conFrame(wx.Frame):
    def __init__(self, parent, title):

        super(conFrame, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()
        self.Bind(wx.EVT_BUTTON, self.DisplayMessage, id=ID_MISSION_1)
        self.Bind(wx.EVT_BUTTON, self.DisplayMessage, id=ID_MISSION_2)
        self.Bind(wx.EVT_BUTTON, self.DisplayMessage, id=ID_MISSION_3)
        self.Bind(wx.EVT_BUTTON, self.DisplayMessage, id=ID_MISSION_4)
        self.Bind(wx.EVT_BUTTON, self.DisplayMessage, id=ID_MISSION_5)

    def InitUI(self):
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(17)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # self.display = wx.TextCtrl(self, style=wx.TE_RIGHT)
        # vbox.Add(self.display, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        gs = wx.GridSizer(6, 3, 5, 5)
        m1btn = wx.Button(self, label='Mission 1', id=ID_MISSION_1)
        m2btn = wx.Button(self, label='Mission 2', id=ID_MISSION_2)
        m3btn = wx.Button(self, label='Mission 3', id=ID_MISSION_3)
        m4btn = wx.Button(self, label='Mission 4', id=ID_MISSION_4)
        m5btn = wx.Button(self, label='Mission 5', id=ID_MISSION_5)
        missbtns = [m1btn, m2btn, m3btn, m4btn, m5btn]
        for i in missbtns:
            i.SetFont(font)
        gs.AddMany([
            (wx.StaticText(self, label='Control'), 0, wx.EXPAND),
            (wx.StaticText(self, label='Status'), 0, wx.EXPAND),
            (wx.StaticText(self), wx.EXPAND),
            (m1btn, 0, wx.EXPAND),
            (wx.StaticText(self, label='Autonomous'), 0, wx.EXPAND),
            (wx.StaticText(self, label=auto_stat), 0, wx.EXPAND),
            (m2btn, 0, wx.EXPAND),
            (wx.StaticText(self, label='Manual'), 0, wx.EXPAND),
            (wx.StaticText(self, label=man_stat), 0, wx.EXPAND),
            (m3btn, 0, wx.EXPAND),
            (wx.StaticText(self, label='Current Mission'), 0, wx.EXPAND),
            (wx.StaticText(self, label=mission_stat), 0, wx.EXPAND),
            (m4btn, 0, wx.EXPAND),
            (wx.StaticText(self, label='Killed'), 0, wx.EXPAND),
            (wx.StaticText(self, label=kill_stat), 0, wx.EXPAND),
            (m5btn, 0, wx.EXPAND),
            (wx.StaticText(self, label='Heartbeat'), 0, wx.EXPAND),
            (wx.StaticText(self, label=hb_stat), 0, wx.EXPAND)
        ])

        vbox.Add(gs, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.ln = wx.StaticLine(self, pos=(130, -50), size=(1, 500), style=wx.LI_VERTICAL)
        self.ln2 = wx.StaticLine(self, pos=(260, -50), size=(1, 500), style=wx.LI_VERTICAL)

    def DisplayMessage(self, e):

        eid = e.GetId()

        if eid == ID_MISSION_1:
            print('Running mission 1')
        elif eid == ID_MISSION_2:
            print('Running mission 2')
        elif eid == ID_MISSION_3:
            print('Running mission 3')
        elif eid == ID_MISSION_4:
            print('Running mission 4')
        elif eid == ID_MISSION_5:
            print('Running mission 5')

    def OnExit(self):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    print("Opened window")
    frame = conFrame(None, title='Console')
    frame.Show()
    print(frame.IsShown())
    app.MainLoop()
