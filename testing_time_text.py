#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random
import time
import pandas as pd
from datetime import datetime


class Experiment(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.text = "Welcome to our little experiment.\n" \
                    "Put your left pointer finger on the F key. Put your right pointer finger on the J key.\n" \
                    "You will see a rectangle in the middle of the screen. This rectangle will change color.\n" \
                    "If it is BLUE press the F key, if it is YELLOW press the J key.\n" \
                    "Press the space-bar to continue"
        self.state = "intro"
        self.timestamp = datetime.now()
        print(self.timestamp)
        self.times_start_first = []
        self.times_end_first = []
        self.times_first = []
        self.times_start_sec = []
        self.times_end_sec = []
        self.times_sec = []
        self.condition_first = []
        self.condition = []
        self.stimu_first = []
        self.stimu_color_sec = []
        self.stimu_word_sec = []
        self.stimu_sec = []
        self.key_pressed_first = []
        self.key_pressed_sec =[]
        self.correct_key_first = []
        self.correct_key_sec = []
        self.init_ui()

    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle('Color Test')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.state == "intro":
            self.draw_intro(event, qp)
        elif self.state == "first":
            self.condition.append(1)
            self.draw_first(event, qp)
        elif self.state == "interlude":
            self.draw_interlude(event, qp)
        elif self.state == "second":
            self.condition.append(2)
            self.draw_second(event, qp)
        elif self.state == "end":
            self.calculate()
            self.logging()
            self.draw_end(event, qp)

    def draw_intro(self, event, qp):
        qp.setFont(QtGui.QFont('Decorative', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def draw_first(self, event, qp):
        self.times_start_first.append(time.time())
        cond = random.randint(0, 1)
        qp.setFont(QtGui.QFont('Decorative', 32))
        text_blue = "BLUE"
        text_yellow = "YELLOW"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, text_yellow)
        if cond == 0:
            self.stimu_first.append('blue')
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond == 1:
            self.stimu_first.append('yellow')
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
        self.times_start_sec.append(time.time())
        cond_rec = random.randint(0, 1)
        cond_word = random.randint(0, 1)
        qp.setFont(QtGui.QFont('Decorative', 32))
        text_blue = "BLUE"
        text_yellow = "YELLOW"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, text_yellow)
        if cond_rec == 0:
            self.stimu_color_sec.append('blue')
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond_rec == 1:
            self.stimu_color_sec.append('yellow')
            qp.setBrush(QtGui.QColor(255, 215, 0))
        rect = QtCore.QRect(860, 320, 200, 200)
        qp.drawRoundedRect(rect, 10.0, 10.0)
        if cond_word == 0:
            self.stimu_word_sec.append('blue')
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setFont(QtGui.QFont('Decorative', 32))
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text_blue)
        elif cond_word == 1:
            self.stimu_word_sec.append('yellow')
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
            if self.counter < 10 and self.state == "first":
                self.counter += 1
                self.times_end_first.append(time.time())
                self.key_pressed_first.append('F')
            if self.counter < 10 and self.state == "second":
                self.counter += 1
                self.times_end_sec.append(time.time())
                self.key_pressed_sec.append('F')
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()
        if event.key() == QtCore.Qt.Key_J:
            if self.counter < 10 and self.state == "first":
                self.counter += 1
                self.times_end_first.append(time.time())
                self.key_pressed_first.append('J')
            if self.counter < 10 and self.state == "second":
                self.counter += 1
                self.times_end_sec.append(time.time())
                self.key_pressed_sec.append('J')
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()

    def calculate(self):
        for i in range(len(self.times_start_first)):
            self.times_first.append(self.times_end_first[i] - self.times_start_first[i])
        for i in range(len(self.times_start_sec)):
            self.times_sec.append(self.times_end_sec[i] - self.times_start_sec[i])

    def logging(self):
        part_id = sys.argv[1]
        # print(part_id)
        correct_key_first = []
        correct_key_sec = []
        # print(self.stimu_first)
        print(self.key_pressed_first)
        for i in self.stimu_first:
            if i == 'blue':
                correct_key_first.append('F')
            elif i == 'yellow':
                correct_key_first.append('J')
        print(correct_key_first)
        for i in range(len(self.stimu_color_sec)):
            self.stimu_sec.append(self.stimu_color_sec[i] +  "-" + self.stimu_word_sec[i])
            # print(self.stimu_sec)
        # print(self.key_pressed_sec)
        for i in self.stimu_word_sec:
            if i == 'blue':
                correct_key_sec.append('F')
            elif i == 'yellow':
                correct_key_sec.append('J')
        # print(correct_key_sec)
        # print(self.times_first)
        # print(self.times_sec)
        # print(self.condition)
        df = pd.DataFrame(columns=['participant_id', 'condition', 'stimulus', 'pressed_key', 'correct_key',
                                   'reaction_time_in_s', 'timestamp'])
        for i in range(len(self.key_pressed_first)):
            df = df.append(pd.Series([part_id, 1, self.stimu_first[i], self.key_pressed_first[i],
                                      correct_key_first[i], self.times_first[i], self.timestamp], index=df.columns),
                           ignore_index=True)
        for i in range(len(self.key_pressed_sec)):
            df = df.append(pd.Series([part_id, self.condition[10+i], self.stimu_sec[i], self.key_pressed_sec[i],
                                      correct_key_sec[i], self.times_sec[i], self.timestamp], index=df.columns),
                           ignore_index=True)
        df.to_csv('log.csv', index=False)
        print(df)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
