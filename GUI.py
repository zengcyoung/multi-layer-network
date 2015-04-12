#!/usr/bin/python3

#############################################################################
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

from PyQt5.QtCore import (Qt, QDir, QFile)
from PyQt5.QtGui import (QKeySequence, QDesktopServices)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget, QDialog, QFileDialog, QGridLayout, QVBoxLayout,
        QProgressDialog, QPushButton, QSizePolicy, QComboBox)

import json
import gettext
import Network

gConfigure = {}

def ReadConfigure():
    global gConfigure
    with open('conf.json') as configureFile:
        try:
            gConfigure = json.load(configureFile)
        except:
            gConfigure = {}
    if 'lang' in gConfigure:
        userLang = [gConfigure['lang']]
        langtext = gettext.translation('flatnet',
                localedir = 'locale', languages = userLang)
        langtext.install()
    else:
        gettext.install('flatnet')

def SaveConfigure():
    global gConfigure
    with open('conf.json', mode = 'w') as configureFile:
        try:
            json.dump(gConfigure, configureFile)
        except:
            None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        browseNetwork1Button = self.createButton(_('Browse'),
                self.browseNetwork1File)
        browseNetwork2Button = self.createButton(_('Browse'),
                self.browseNetwork2File)
        browseNetworkMappingButton = self.createButton(_('Browse'),
                self.browseNetworkMappingFile)
        browseNetworkFlatButton = self.createButton(_('Browse'),
                self.browseNetworkFlatFile)

        self.network1PathComboBox = self.createComboBox()
        self.network2PathComboBox = self.createComboBox()
        self.networkMappingPathComboBox = self.createComboBox()
        self.networkFlatPathComboBox = self.createComboBox()

        network1Label = QLabel(_('Network 1:'))
        network2Label = QLabel(_('Network 2:'))
        networkMappingLabel = QLabel(_('Network mapping:'))
        networkFlatLabel = QLabel(_('Flat network:'))

        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.addWidget(network1Label, 0, 0)
        mainLayout.addWidget(self.network1PathComboBox, 0, 1, 1, 4)
        mainLayout.addWidget(browseNetwork1Button, 0, 5, 1, 2)
        mainLayout.addWidget(network2Label, 1, 0)
        mainLayout.addWidget(self.network2PathComboBox, 1, 1, 1, 4)
        mainLayout.addWidget(browseNetwork2Button, 1, 5, 1, 2)
        mainLayout.addWidget(networkMappingLabel, 2, 0)
        mainLayout.addWidget(self.networkMappingPathComboBox, 2, 1, 1, 4)
        mainLayout.addWidget(browseNetworkMappingButton, 2, 5, 1, 2)
        mainLayout.addWidget(networkFlatLabel, 3, 0)
        mainLayout.addWidget(self.networkFlatPathComboBox, 3, 1, 1, 4)
        mainLayout.addWidget(browseNetworkFlatButton, 3, 5, 1, 2)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(mainLayout)
        widget.resize(500, 500)

        self.createActions()
        self.createMenus()

        self.setWindowTitle(_('Flat network user relationship tool'))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def createActions(self):
        self.englishAct = QAction("&English", self, triggered =
                self.switchToEnglish)

        self.chineseAct = QAction("简体中文", self, triggered =
                self.switchToChinese)

    def createMenus(self):
        self.langMenu = self.menuBar().addMenu(_("&Language"))
        self.langMenu.addAction(self.englishAct)
        self.langMenu.addAction(self.chineseAct)

    def switchToEnglish(self):
        gConfigure['lang'] = 'en'
        SaveConfigure()

    def switchToChinese(self):
        gConfigure['lang'] = 'zh'
        SaveConfigure()

    def browseNetwork1File(self):
        fileNetwork1Path = QFileDialog.getOpenFileName(self, _('Network 1 CSV File'),
                QDir.currentPath())

        if fileNetwork1Path:
            if self.network1PathComboBox.findText(fileNetwork1Path[0]) == -1:
                self.network1PathComboBox.addItem(fileNetwork1Path[0])

            self.network1PathComboBox.setCurrentIndex(
                    self.network1PathComboBox.findText(fileNetwork1Path[0]))

    def browseNetwork2File(self):
        fileNetwork2Path = QFileDialog.getOpenFileName(self, _('Network 2 CSV File'),
                QDir.currentPath())

        if fileNetwork2Path:
            if self.network2PathComboBox.findText(fileNetwork2Path[0]) == -1:
                self.network2PathComboBox.addItem(fileNetwork2Path[0])

            self.network2PathComboBox.setCurrentIndex(
                    self.network2PathComboBox.findText(fileNetwork2Path[0]))

    def browseNetworkMappingFile(self):
        fileNetworkMappingPath = QFileDialog.getOpenFileName(
                self, _('Network Mapping CSV File'),
                QDir.currentPath())

        if fileNetworkMappingPath:
            if self.networkMappingPathComboBox.findText(fileNetworkMappingPath[0]) == -1:
                self.networkMappingPathComboBox.addItem(fileNetworkMappingPath[0])

            self.networkMappingPathComboBox.setCurrentIndex(
                    self.networkMappingPathComboBox.findText(fileNetworkMappingPath[0]))

    def browseNetworkFlatFile(self):
        fileNetworkFlatPath = QFileDialog.getOpenFileName(
                self, _('Flat Network CSV File'),
                QDir.currentPath())

        if fileNetworkFlatPath:
            if self.networkFlatPathComboBox.findText(fileNetworkFlatPath[0]) == -1:
                self.networkFlatPathComboBox.addItem(fileNetworkFlatPath[0])

            self.networkFlatPathComboBox.setCurrentIndex(
                    self.networkFlatPathComboBox.findText(fileNetworkFlatPath[0]))

    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return comboBox

if __name__ == '__main__':

    import sys

    ReadConfigure()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

