# -*-coding:utf-8-*-
import sys
import pandas as pd
from PyQt5 import QtWidgets
from ui.tianyi import TianYi


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TianYi()
    window.show()
    sys.exit(app.exec_())


def test():
    df = pd.read_csv('000001.csv')
    df.loc[df.loc[:, 'Type'] == 'B', 'Type'] = 1
    # df.loc[df.loc[:, 'Type'] == 'S', 'Type'] = -1
    df.Type[df.Type == 'S'] = -1
    print(df.head(10))


if __name__ == '__main__':
    test()
#     #main()




