from PyQt5 import QtCore, QtGui, QtWidgets

#self.tabWidget_2.setTabBar(HorizontalTabBar())
class HorizontalTabBar(QtWidgets.QTabBar):
    
    def __init__(self, *args, **kwargs):
        super(HorizontalTabBar, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()
        painter.begin(self)
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.save()

            s = option.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(option.rect.center())
            option.rect = r

            c = self.tabRect(index).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, option)
            painter.restore()
            '''
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter | QtCore.Qt.TextDontClip, self.tabText(index))
            '''
        painter.end()