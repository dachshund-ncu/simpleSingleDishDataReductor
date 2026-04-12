style_sheet = R'''
    QMainWindow {
        background-color: #121212;
    }
    QMenuBar {
        background-color: transparent;
    }
    QMenuBar::item{
        background-color: transparent;
        padding: 8px; /* padding */
        border-radius: 2px; /* border radius */
        font-size: 12px; /* font size */
        text-align: left;
        font-family: silka;
        color: white; /* text color */
    }
    QMenuBar::item:selected {
        background-color: #212121;
        border: 1px solid rgba(255,255,255, 25%);
    }
    QMenu {
        background-color: #121212;
        color: white; /* text color */
        padding: 4px; /* padding */
        font-size: 12px; /* font size */
        border-radius: 2px; /* border radius */
        text-align: left;
        font-family: silka;
        border: 1px solid rgba(255,255,255, 25%);
    }
    QAction{
        color: white; /* text color */
        padding: 4px; /* padding */
        font-size: 15px; /* font size */
        border-radius: 2px; /* border radius */
        text-align: left;
        font-family: silka;
    }
    QMenu::item {
        background-color: transparent;
        padding: 8px 12px;
        border-radius: 2px; /* border radius */
    }
    QMenu::item:selected {
        background-color: rgba(255,255,255,9%);
        border: 1px solid rgba(255,255,255,25%);
    }
    QMenu::item:checked {
        background-color: #C2185B;
    }
    QMenu::separator{
        height: 1px;
        background-color: rgba(255, 255, 255, 25%); /* Matches your border color */
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 4px;
        margin-bottom: 4px;
    }
'''