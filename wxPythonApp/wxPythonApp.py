import wx
from mainFrame import MainFrame

def main():
    """
    Creates App class instance, then initiates the main 
    frame where all other modules are loaded.
    Runs the main loop
    """
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()