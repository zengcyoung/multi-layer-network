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

from PyQt5.QtCore import (QDir, QIODevice, QFile, QFileInfo, Qt, QTextStream,
        QUrl)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QComboBox,
        QDialog, QFileDialog, QGridLayout, QHBoxLayout, QHeaderView, QLabel,
        QProgressDialog, QPushButton, QSizePolicy, QTableWidget,
        QTableWidgetItem, QVBoxLayout)

import gettext

zh = gettext.translation('flatnet', localedir = 'locale',
        languages = ['zh'])
zh.install()

class Window(QDialog):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        browseNetwork1Button = self.createButton(_('Browse'),
                self.browseNetwork1File)
        browseNetwork2Button = self.createButton(_('Browse'),
                self.browseNetwork2File)
        browseNetworkMappingButton = self.createButton(_('Browse'),
                self.browseNetworkMappingFile)
        browseNetworkFlatButton = self.createButton(_('Browse'),
                self.browseNetworkFlatFile)

        self.network1PathComboBox = self.createComboBox(
                _('CSV file location of the 1st Network'))
        self.network2PathComboBox = self.createComboBox(
                _('CSV file location of the 2nd Network'))
        self.networkMappingPathComboBox = self.createComboBox(
                _('CSV file location of the network node mapping'))
        self.networkFlatPathComboBox = self.createComboBox(
                _('CSV file location of the flat network for saving'))

        network1Label = QLabel(_('Network 1:'))
        network2Label = QLabel(_('Network 2:'))
        networkMappingLabel = QLabel(_('Network mapping:'))
        networkFlatLabel = QLabel(_('Flat network:'))

        buttonsLayout = QVBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(browseNetwork1Button)
        buttonsLayout.addWidget(browseNetwork2Button)
        buttonsLayout.addWidget(browseNetworkMappingButton)
        buttonsLayout.addWidget(browseNetworkFlatButton)

        mainLayout = QGridLayout()
        mainLayout.addWidget(network1Label, 0, 0)
        mainLayout.addWidget(self.network1PathComboBox, 0, 1, 1, 2)
        mainLayout.addWidget(network2Label, 1, 0)
        mainLayout.addWidget(self.network2PathComboBox, 1, 1, 1, 2)
        mainLayout.addWidget(networkMappingLabel, 2, 0)
        mainLayout.addWidget(self.networkMappingPathComboBox, 2, 1, 1, 2)
        mainLayout.addWidget(networkFlatLabel, 3, 0)
        mainLayout.addWidget(self.networkFlatPathComboBox, 3, 1, 1, 2)
        mainLayout.addLayout(buttonsLayout, 0, 4, 4, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle(_('Flat network user relationship tool'))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def browseNetwork1File(self):
        None

    def browseNetwork2File(self):
        None

    def browseNetworkMappingFile(self):
        None

    def browseNetworkFlatFile(self):
        None

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

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

