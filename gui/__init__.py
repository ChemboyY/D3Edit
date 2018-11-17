import wx
import save_manager
from gui import account_frame

def start():
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = Welcome(None, title='D3Edit')
    frm.Show()
    app.MainLoop()


class Welcome(wx.Frame):
    def __init__(self, *args, **kwargs):
        # ensure the parent's __init__ is called
        super(Welcome, self).__init__(*args, **kwargs)
        # create a panel in the frame
        pnl = wx.Panel(self)
        window_size = wx.Size(800, 600)
        self.SetInitialSize(size=window_size)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Import an account.dat file to get started!", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Import an account.dat file to get started!")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        openitem = fileMenu.Append(-1, "&Open\tCtrl-O",
                                    "Select account.dat file to import")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exititem = fileMenu.Append(wx.ID_EXIT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.onopen, openitem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exititem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def doondatfile(self, file):
        self.account = save_manager.SaveData(file)
        account_frame.Account()


    def onopen(self, event):
        with wx.FileDialog(self, "Open .dat file", wildcard=".dat files (*.dat)|*.dat",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                self.doondatfile(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)