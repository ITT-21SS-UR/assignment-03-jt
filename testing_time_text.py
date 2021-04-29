#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random
import time
import pandas as pd
from datetime import datetime


class Experiment(QtWidgets.QWidget):
    # init all necessary variables
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.text = "Welcome to our little experiment.\n" \
                    "Put your left pointer finger on the F key. Put your right pointer finger on the J key.\n" \
                    "You will see a rectangle in the middle of the screen. This rectangle will change color.\n" \
                    "If it is BLUE press the F key, if it is YELLOW press the J key.\n" \
                    "Press the space-bar to continue"
        self.state = "intro"
        self.text_blue = "BLUE"
        self.text_yellow = "YELLOW"
        self.timestamp_start = datetime.timestamp(datetime.now())
        self.start_time = []
        self.end_time = []
        self.stimuli = []
        self.sec_color_stimuli = []
        self.sec_word_stimuli = []
        self.key_pressed = []
        self.init_ui()

    # init UI
    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle('Color Test')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    # decides on state which display to paint
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setFont(QtGui.QFont('Decorative', 32))
        if self.state == "intro":
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        elif self.state == "first":
            self.draw_first(event, qp)
        elif self.state == "interlude":
            self.draw_interlude(event, qp)
        elif self.state == "second":
            self.draw_second(event, qp)
        elif self.state == "end":
            self.logging()
            self.text = "Thanks for your participation"
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    # draws first condition
    def draw_first(self, event, qp):
        self.start_time.append(time.time())
        cond = random.randint(0, 1)
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, self.text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, self.text_yellow)
        if cond == 0:
            self.stimuli.append('blue')
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond == 1:
            self.stimuli.append('yellow')
            qp.setBrush(QtGui.QColor(255, 215, 0))
        rect = QtCore.QRect(830, 300, 200, 200)
        qp.drawRoundedRect(rect, 10.0, 10.0)

    # draws interlude between first and second condition
    def draw_interlude(self, event, qp):
        self.text = "Thank you for the first round. Now it gets a bit more difficult.\n" \
                    "Put your left pointer finger on the F key. Put your right pointer finger on the J key.\n" \
                    "You will see a rectangle in the middle of the screen. In the rectangle you will see a word.\n" \
                    "You have to look at the word and press the accordingly key.\n" \
                    "If it is BLUE press the F key, if it is YELLOW press the J key.\n" \
                    "Press the space-bar to continue"
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    # draws second condition
    def draw_second(self, event, qp):
        self.start_time.append(time.time())
        cond_rec = random.randint(0, 1)
        cond_word = random.randint(0, 1)
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, self.text_blue)
        qp.drawText(event.rect(), QtCore.Qt.AlignRight, self.text_yellow)
        # randomized order for the color of the rectangle
        if cond_rec == 0:
            self.sec_color_stimuli.append('blue')
            qp.setBrush(QtGui.QColor(34, 34, 200))
        elif cond_rec == 1:
            self.sec_color_stimuli.append('yellow')
            qp.setBrush(QtGui.QColor(255, 215, 0))
        rect = QtCore.QRect(860, 320, 200, 200)
        qp.drawRoundedRect(rect, 10.0, 10.0)
        qp.setPen(QtGui.QColor(255, 255, 255))
        # randomized order for the word (important stimuli)
        if cond_word == 0:
            self.sec_word_stimuli.append('blue')
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text_blue)
        elif cond_word == 1:
            self.sec_word_stimuli.append('yellow')
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text_yellow)

    # handles key-presses
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
            if self.counter < 10:
                self.counter += 1
                self.end_time.append(time.time())
                self.key_pressed.append('F')
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()
        if event.key() == QtCore.Qt.Key_J:
            if self.counter < 10:
                self.counter += 1
                self.end_time.append(time.time())
                self.key_pressed.append('J')
            if self.counter == 10 and self.state == "first":
                self.state = "interlude"
            if self.counter == 10 and self.state == "second":
                self.state = "end"
            self.update()

    def logging(self):
        # get participant_id from input
        part_id = sys.argv[1]
        # get end timestamp
        timestamp_end = datetime.timestamp(datetime.now())
        time_calc = []
        correct_key = []
        condition = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        # calculate time for first and second condition
        for i in range(len(self.start_time)):
            time_calc.append(self.end_time[i] - self.start_time[i])
        # get correct key from stimulus for the first condition
        for i in self.stimuli:
            if i == 'blue':
                correct_key.append('F')
            elif i == 'yellow':
                correct_key.append('J')
        # get correct key from stimulus for the second condition
        for i in self.sec_word_stimuli:
            if i == 'blue':
                correct_key.append('F')
            elif i == 'yellow':
                correct_key.append('J')
        # concatenate both stimuli of the second conditions
        for i in range(len(self.sec_color_stimuli)):
            self.stimuli.append(self.sec_color_stimuli[i] + "-" + self.sec_word_stimuli[i])

        # construct csv data structure and add all data
        df = pd.DataFrame(columns=['participant_id', 'condition', 'stimulus', 'pressed_key', 'correct_key',
                                   'reaction_time_in_s', 'timestamp_start', 'timestamp_end'])
        for i in range(len(self.key_pressed)):
            df = df.append(pd.Series([part_id, condition[i], self.stimuli[i], self.key_pressed[i],
                                      correct_key[i], time_calc[i], self.timestamp_start, timestamp_end], index=df.columns),
                           ignore_index=True)
        df.to_csv('log_' + str(part_id) + '.csv', index=False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
