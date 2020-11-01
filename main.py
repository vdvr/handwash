import sys
import locale
import yaml
import glob
from PyQt5.QtWidgets import QApplication
from ui import (
    Step,
    MainUI,
)
from PyQt5.QtGui import QFontDatabase

locale.setlocale(locale.LC_TIME, "nl_be")

with open('steps.yaml') as f:
    yConfig = yaml.safe_load(f)
    
steps = [
    Step(
        name=name,
        **stepOpt
    )
        for step in yConfig["steps"] 
        for (name, stepOpt) in step.items()
]

app = QApplication(sys.argv)

for filepath in glob.iglob("fonts/*/*.ttf"):
    QFontDatabase.addApplicationFont(filepath)

mainUI = MainUI(steps, startTxt=yConfig["startText"], styleFile="ui/style.qss")
mainUI.show()

sys.exit(app.exec_())