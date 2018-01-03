# -*-coding:utf-8-*-
import sys
from PyQt5 import QtWidgets
from ui.tianyi import TianYi


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TianYi()
    window.show()
    sys.exit(app.exec_())


import pandas as pd

df = pd.read_csv('000001.csv')
df.Type[df.Type == 'B'] = 1
df.Type[df.Type == 'S'] = -1
print(df.head(10))

# if __name__ == '__main__':
#     #main()



