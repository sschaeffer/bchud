import curses

class BCAdvancementWindow():

    def __init__(self, window:curses.window):
        self.window = window

    def Render(self,height,width):
        self.window.resize(height-1,width)
        self.window.clear()
        self.window.box()