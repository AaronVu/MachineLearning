# import surface.loginForm
# import sys
#
# from PyQt5 import QtWidgets

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = surface.loginForm.Ui_Form()
#     window.show()
#     sys.exit(app.exec_())

from nltk.corpus import comtrans
words = comtrans.words('alignment-en-fr.txt')
for word in words:
    print(word)
