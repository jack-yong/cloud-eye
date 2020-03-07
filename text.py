import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.panel = wx.Panel(self, -1)
        self.button = wx.Button(self.panel, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button)

    def onClick(self, evt):
        dialog = wx.Dialog(self.panel)
        rec = dialog.ShowModal()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()