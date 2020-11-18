from datetime import datetime
import magic
import platform
import vlc
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem, 
    QGraphicsPixmapItem,
)



class MediaView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()

        self.instance = vlc.Instance("--input-repeat=999999")
        self.mediaplayer = self.instance.media_player_new()


    def setSource(self, filePath):
        self.scene.clear()
        self.mediaplayer.stop()
        self.viewport().update()

        fileMime = magic.from_file(filePath, mime=True)

        if fileMime == "image/svg+xml":
            mediaItem = QGraphicsSvgItem(filePath)
            mediaItem.setScale(4)

        elif fileMime in self._allowedImageMime:
            mediaItem = QGraphicsPixmapItem(QPixmap(filePath))

        elif fileMime in self._allowedVideoMime:
            
            self.media = self.instance.media_new(filePath)
            self.mediaplayer.set_media(self.media)

            if platform.system() == "Linux":
                self.mediaplayer.set_xwindow(int(self.winId()))
            elif platform.system() == "Windows":
                self.mediaplayer.set_hwnd(int(self.winId()))
            
            self.mediaplayer.play()
            return

        else:
            mediaItem = QGraphicsItem()
        
        self.scene.addItem(mediaItem)
        self.setScene(self.scene)



    @property
    def _allowedImageMime(self):
        return [
            "image/png",
            "image/jpeg",
            "image/bmp",
            "image/gif",
        ]
        
    
    @property
    def _allowedVideoMime(self):
        return [
            "video/mp4",
            "video/quicktime",
            "video/x-msvideo",
            "video/mpeg"
        ]

    
    @pyqtSlot()
    def _startVideo(self):
        self.videoPlayer.play()



class DateTimeWidget(QWidget):
    def __init__(self, main=False):
        super().__init__()

        # Initialize current time and date label and add to layout
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")

        self.dateTimeLayout = QVBoxLayout()
        self.dateLbl = QLabel(dateNow)
        self.dateLbl.setObjectName("datebig" if main else "datesmall")
        self.dateLbl.setAlignment(Qt.AlignHCenter if main else Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.dateLbl)

        self.timeLbl = QLabel(timeNow)
        self.timeLbl.setObjectName("timebig" if main else "timesmall")
        self.timeLbl.setAlignment(Qt.AlignHCenter if main else Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.timeLbl)

        self.dateTimeLayout.addStretch()
        self.dateTimeLayout.setSpacing(0)

        self.setLayout(self.dateTimeLayout)

        # Start timer for current time
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self._updateClock)
        self.clockTimer.start(1000)
        

    @pyqtSlot()
    def _updateClock(self):
        
        # Set current time
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")
        self.dateLbl.setText(dateNow)
        self.timeLbl.setText(timeNow)