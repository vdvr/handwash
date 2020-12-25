import sys
import locale
import yaml
import glob
from PyQt5.QtWidgets import QApplication
from time import sleep

from . import (
    Step, 
    StepUI,
    IdleUI,
)
from PyQt5.QtGui import QFontDatabase


if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "nl_BE")

    with open('steps.yaml') as f:
        yamlSteps = yaml.safe_load(f)
    
    steps = [
        Step(
            name=name,
            **stepOpt
        )
            for step in yamlSteps["steps"] 
            for (name, stepOpt) in step.items()
    ]
    
    app = QApplication(sys.argv)
    
    for filepath in glob.iglob("fonts/*/*.ttf"):
        QFontDatabase.addApplicationFont(filepath)

    stepUI = StepUI(steps, 'ui/style.qss')
    stepUI.show()
    #idleUI = IdleUI('ui/style.qss')
    #idleUI.show()
    
    sys.exit(app.exec_())
