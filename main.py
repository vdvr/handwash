import sys
import yaml
import glob
from PyQt5.QtWidgets import QApplication
from ui import (
    Step,
    MainUI,
)
from PyQt5.QtGui import QFontDatabase

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

mainUI = MainUI(steps, startTxt=yConfig["startText"], styleFile="ui/style.qss", time_locale="nl_BE.utf8")
mainUI.show()

sys.exit(app.exec_())
