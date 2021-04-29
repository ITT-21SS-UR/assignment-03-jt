#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random


class Experiment(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle('Color Test')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()
        self.counter = 0
        self.text = "Welcome to our little experiment.\n" \
                    "Put your left pointer finger on the F key. Put your right pointer finger on the J key.\n" \
                    "You will see a rectangle in the middle of the screen. This rectangle will change color.\n" \
                    "If it is BLUE press the F key, if it is YELLOW press the J key.\n" \
                    "Press the space-bar to continue"
        self.state = "intro"

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.state == "intro":
            self.draw_intro(event, qp)
        elif self.state == "first":
            self.draw_first(event, qp)
        elif self.state == "interlude":
            self.draw_interlude(event, qp)
        elif self.state == "second":
            self.draw_second(event, qp)
        elif self.state == "end":
            self.draw_end(event, qp)

    def draw_intro(self, event, qp):
        qp.setFont(QtGui.QFont('Decorative', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def draw_first(self, event, qp):
        cond = random.randint(0, 1)
        qp.setFont(QtGui.QFont('Decorative', 32))
        text_blue = "BLUE"
        text_yellow = "YELLOW"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, text_yellow)
        if cond == 0:
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond == 1:
            qp.setBrush(QtGui.QColor(255, 215, 0))
        rect = QtCore.QRect(830, 300, 200, 200)
        qp.drawRoundedRect(rect, 10.0, 10.0)

    def draw_interlude(self, event, qp):
        self.text = "Thank you for the first round. Now it gets a bit more difficult.\n" \
                    "Put your left pointer finger on the F key. Put your right pointer finger on the J key.\n" \
                    "You will see a rectangle in the middle of the screen. In the rectangle you will see a word.\n" \
                    "You have to look at the word and press the accordingly key.\n" \
                    "If it is BLUE press the F key, if it is YELLOW press the J key.\n" \
                    "Press the space-bar to continue"
        qp.setFont(QtGui.QFont('Decorative', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def draw_second(self, event, qp):
        cond_rec = random.randint(0, 1)
        cond_word = random.randint(0, 1)
        qp.setFont(QtGui.QFont('Decorative', 32))
        text_blue = "BLUE"
        text_yellow = "YELLOW"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, text_yellow)
        if cond_rec == 0:
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond_rec == 1:
            qp.setBrush(QtGui.QColor(255, 215, 0))
        rect = QtCore.QRect(860, 320, 200, 200)
        qp.drawRoundedRect(rect, 10.0, 10.0)
        if cond_word == 0:
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setFont(QtGui.QFont('Decorative', 32))
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text_blue)
        elif cond_word == 1:
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setFont(QtGui.QFont('Decorative', 32))
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text_yellow)

    def draw_end(self, event, qp):
        self.text = "Thanks for your participation"
        qp.setFont(QtGui.QFont('Decorative', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.state == "intro":
                self.state = "first"
                self.update()
            if self.state == "interlude":
                self.counter = 0
                self.state = "second"
                self.update()
        if event.key() == QtCore.Qt.Key_F:
            self.counter += 1
            print(self.counter)
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()
        if event.key() == QtCore.Qt.Key_J:
            self.counter += 1
            print(self.counter)
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
