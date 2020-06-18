from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor, qRgb


class TaskTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, gmp):
        self.names = []
        self.states = []
        self.reports = []
        self.last_reports = []
        self.severities = []

        response = gmp.get_tasks()

        for task in response.tasks:
            self.names.append(task.name)
            self.states.append(task.status)
            self.reports.append(task.report_count.current)
            if task.last_report.timestamp is not None:
                self.last_reports.append(task.last_report.timestamp.strftime("%a, %d. %B %Y %H:%M %Z"))
            else:
                self.last_reports.append("")
            self.severities.append(task.last_report.severity.full)

        self.column_count = 5
        self.row_count = len(self.names)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Name", "Status", "Berichte","Letzter Bericht", "Schweregrad")[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return self.names[row]
            elif column == 1:
                return self.states[row]
            elif column == 2:
                return self.reports[row]
            elif column == 3:
                return self.last_reports[row]
            elif column == 4:
                return self.severities[row]
        elif role == Qt.BackgroundRole:
            if row%2 == 1:
                return QColor(qRgb(70,70,70))
            else: 
                return QColor(qRgb(50,50,50))
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.TextColorRole:
            return QColor(Qt.white)

        return None