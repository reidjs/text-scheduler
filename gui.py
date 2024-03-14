from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
)
from PyQt5.QtCore import QDate, QDateTime, QTime, QEvent
import sys
import os


class ScrollableComboBox(QComboBox):
    def __init__(self, items=[], wraparound=False, parent=None):
        super().__init__(parent)
        self.addItems(items)
        self.wraparound = wraparound
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel and source is self:
            currentIndex = self.currentIndex()
            if event.angleDelta().y() > 0:  # Scroll up
                newIndex = currentIndex - 1
                if self.wraparound and newIndex < 0:
                    newIndex = self.count() - 1
            else:  # Scroll down
                newIndex = currentIndex + 1
                if self.wraparound and newIndex >= self.count():
                    newIndex = 0

            # Update only if newIndex is within bounds or wraparound is enabled
            if 0 <= newIndex < self.count() or self.wraparound:
                self.setCurrentIndex(newIndex)
            return True
        return super().eventFilter(source, event)


class CustomDateTimePicker(QWidget):
    def __init__(self, overwrite=True):
        super().__init__()
        self.overwrite = overwrite
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        self.recipientEntry = QLineEdit(self)
        self.recipientEntry.setPlaceholderText("Recipient Name")
        mainLayout.addWidget(self.recipientEntry)

        # Message text input
        self.messageText = QTextEdit(self)
        self.messageText.setPlaceholderText("Your message...")
        mainLayout.addWidget(self.messageText)

        pickerLayout = QHBoxLayout()

        currentDate = QDate.currentDate()
        currentTime = QTime.currentTime()

        months = [QDate.longMonthName(month) for month in range(1, 13)]
        self.monthBox = ScrollableComboBox(months, self)
        self.monthBox.setCurrentIndex(currentDate.month() - 1)
        pickerLayout.addWidget(self.monthBox)

        days = [
            str(day) for day in range(1, 32)
        ]  # Placeholder range, adjust later based on the month
        self.dayBox = ScrollableComboBox(days, self)
        self.dayBox.setCurrentIndex(currentDate.day() - 1)
        pickerLayout.addWidget(self.dayBox)

        # Adjust hours to 12-hour format
        hours = [f"{hour:02d}" for hour in range(1, 13)]
        self.hourBox = ScrollableComboBox(hours, wraparound=True, parent=self)
        hourIn12HFormat = (currentTime.hour() % 12) or 12
        self.hourBox.setCurrentIndex(hourIn12HFormat - 1)
        pickerLayout.addWidget(self.hourBox)

        minutes = [f"{minute:02d}" for minute in range(60)]
        self.minuteBox = ScrollableComboBox(minutes, self)
        self.minuteBox.setCurrentIndex(currentTime.minute())
        pickerLayout.addWidget(self.minuteBox)

        # Add AM/PM selection
        ampm = ["AM", "PM"]
        self.ampmBox = ScrollableComboBox(ampm, wraparound=True, parent=self)
        self.ampmBox.setCurrentIndex(0 if currentTime.hour() < 12 else 1)
        pickerLayout.addWidget(self.ampmBox)

        mainLayout.addLayout(pickerLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle('Schedule Message')

        self.scheduleButton = QPushButton("Schedule", self)
        self.scheduleButton.clicked.connect(self.createScheduleFile)
        mainLayout.addWidget(self.scheduleButton)

    def createScheduleFile(self):
        recipientName = self.recipientEntry.text()
        message = self.messageText.toPlainText()
        month = self.monthBox.currentText()
        day = self.dayBox.currentText()
        hour = self.hourBox.currentText()
        minute = self.minuteBox.currentText()
        ampm = self.ampmBox.currentText()

        s = open('SETTINGS.txt', 'r').read()
        lines = s.split('\n')
        lines_filtered = [
            e.strip()
            for e in lines
            if e != '' and not e.strip().startswith('#')
        ]
        print(lines_filtered)
        d = {e.split('=')[0]: e.split('=')[1] for e in lines_filtered}
        root = os.path.abspath(d['SCHEDULED_TEXTS_DIRECTORY'])

        # Constructing filename
        if '=' in recipientName:
            true_recipient = recipientName.split('=')[0]
        else:
            true_recipient = recipientName
        fileName = (
            f"Text {true_recipient} {month} {day}, {hour}:{minute}{ampm}.txt"
        )
        fileName = os.path.join(root, fileName)

        settingsEdited = False
        if '=' in recipientName:
            name = recipientName.split('=')[0]
            number = recipientName.split('=')[1]
            if name in d.keys():
                if d[name] != number:
                    if self.overwrite:
                        d[name] = number
                        settingsEdited = True
                    else:
                        raise ValueError(
                            f"Recipient {name} already exists with different number"
                        )
            else:
                d[name] = number
                settingsEdited = True
            if settingsEdited:
                print(f'Adding {name}={number} to SETTINGS.txt')
                with open('SETTINGS.txt', 'w') as file:
                    file.write('\n'.join([f"{k}={v}" for k, v in d.items()]))

        # Writing the message to the file
        with open(fileName, 'w') as file:
            file.write(message)

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    picker = CustomDateTimePicker()
    picker.show()
    sys.exit(app.exec_())
