from theme import * 

class AFFTheme(Theme):
    
    TEXTURE = "data/ui/gui.png"
    
    CHECKON = Stretch(360,40,20,20)
    CHECKOFF = Stretch(400,40,20,20)
    RADIOON = Stretch(280,40,20,20)
    RADIOOFF = Stretch(320,40,20,20)
    PANDA = Tiled(280,80,20,20)
    
    INPUT = TileBorder(20,300,180,180,20)
    
    X = Stretch(280,80,20,20)
    DRAG = Stretch(440,80,20,20)
    
    FRAME = TileBorder(20,300,180,180,20)
    FORM = TileBorder(20,20,202-20,182-20,20)
    FRAMEBAR = TileBarX(280,480,140,20,20)
    BUTTON = Tiled(320,420,20,20)
    BUTTON = TileBarX(280,480,140,20,20)
    BUTTON = TileBorder(288,170,490-288,190-170,5)
    BUTTON = TileBorder(290,270,210,20,10)
    BUTTON = Tiled(290,270,210,20)
    INPUT = BUTTON
    MENU  = BUTTON
    PROGRESS_BAR = INPUT
    
    BUTTON = TileBarX(300,300,140,20,20)
    DOWN = Tiled(300,260,200,40)
    TEXTCOLOR = (1,1,1,1)
    LABLECOLOR = TEXTCOLOR
    INPUTCOLOR = TEXTCOLOR
    
    SELECT_OPTION_COLOR = (1,0,0,1)

    VSCROLL = Stretch(470,330,10,450-330)
    VSCROLL_UP = Stretch(490,330,10,10)
    VSCROLL_CENTER = Stretch(490,370,10,40)
    VSCROLL_DOWN = Stretch(490,440,10,10)
    
    HSCROLL = Stretch(280,460,460-280,470-460)
    HSCROLL_UP = Stretch(480,440,10,10)
    HSCROLL_CENTER = Stretch(350,440,40,10)
    HSCROLL_DOWN = Stretch(450,440,10,10)
            
    SELECT_BG = StretchBorder(300,330,460-300,10,5)
    SELECT_HIGHLIGHT = StretchBorder(300,350,460-300,10,5)