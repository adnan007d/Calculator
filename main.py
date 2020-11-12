#!/usr/bin/python3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import sys

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator,self).__init__()
        loadUi('Calculator.ui',self)    # Loading UI
        self.Calc_List = list() # List for calculation
        self.Display_List = list()   # List for Display
        self.Operator_list = ['+','*','/','-','.','%','^']  #Operator lists
        self.initUI()
        
    def initUI(self):
        # Connecting the buttons to a specific function
        self.Button_1.clicked.connect(lambda : self.Operator_And_Operand(self.Button_1.text()))
        self.Button_2.clicked.connect(lambda : self.Operator_And_Operand(self.Button_2.text()))
        self.Button_3.clicked.connect(lambda : self.Operator_And_Operand(self.Button_3.text()))
        self.Button_4.clicked.connect(lambda : self.Operator_And_Operand(self.Button_4.text()))
        self.Button_5.clicked.connect(lambda : self.Operator_And_Operand(self.Button_5.text()))
        self.Button_6.clicked.connect(lambda : self.Operator_And_Operand(self.Button_6.text()))
        self.Button_7.clicked.connect(lambda : self.Operator_And_Operand(self.Button_7.text()))
        self.Button_8.clicked.connect(lambda : self.Operator_And_Operand(self.Button_8.text()))
        self.Button_9.clicked.connect(lambda : self.Operator_And_Operand(self.Button_9.text()))
        self.Button_0.clicked.connect(lambda : self.Operator_And_Operand(self.Button_0.text()))
        self.Dot.clicked.connect(lambda : self.Operator_And_Operand(self.Dot.text()))
        self.Plus.clicked.connect(lambda : self.Operator_And_Operand(self.Plus.text()))
        self.Minus.clicked.connect(lambda : self.Operator_And_Operand(self.Minus.text()))
        self.Multiply.clicked.connect(lambda : self.Operator_And_Operand(self.Multiply.text()))
        self.Divide.clicked.connect(lambda : self.Operator_And_Operand(self.Divide.text()))
        self.Mod.clicked.connect(lambda : self.Operator_And_Operand(self.Mod.text()))
        self.Right_Brac.clicked.connect(lambda : self.Operator_And_Operand(self.Right_Brac.text()))
        self.Left_Brac.clicked.connect(lambda : self.Operator_And_Operand(self.Left_Brac.text()))
        self.Raise.clicked.connect(lambda : self.Operator_And_Operand(self.Raise.text()))
        self.Back.clicked.connect(self.Cancel)
        self.Clear.clicked.connect(self.clear)
        self.Equal.clicked.connect(self.Calc)

    def Operator_And_Operand(self,value):   # Displaying and storing the operator and Operand
        if len(self.Display_List) and self.Display_List[-1] in self.Operator_list and value in self.Operator_list: # Checking for consecutive operators
            if self.Display_List[0] == '-' and value in ['+','-','/','*','%','^'] and len(self.Display_List) == 1: # So that if you type - and then some operator then a number then negative sign still stays
                return
            if value != '.' or self.Display_List[-1] != '-': # This allows . after - for example -.5 for -0.5 (D'Morgan's rule)
                self.Display_List.pop()
        if not len(self.Display_List) and value in ['+','*','/','^','%',')']: # Only allowing - as the starting operator
            return
        if len(self.Display_List) and self.Display_List[-1] == '(' and value in ['+','*','/',')','.','%','^']: # Allowing only - after ( example in 5^(-2) and not 5^(*2)
            return
        self.Display_List.append(value)
        display = "".join(self.Display_List) # Joining the list to form a string
        self.Input.setText(display)
    
    def Cancel(self):
        if len(self.Display_List):   # Popping only when list is not empty
            self.Display_List.pop()  #Poping the last element of the list when Back button is pressed
        display = "".join(self.Display_List) # Joining the list into string
        self.Input.setText(display)

    def clear(self):
        # Clearing Display list, Calculation list, Input and Answer 
        del(self.Display_List[:])
        del(self.Calc_List[:])
        self.Input.setText("") 
        self.Answer.setText("")

    def Calc(self):
        if not len(self.Display_List) or self.Display_List[-1] in self.Operator_list: # When list is Empty or last element is a operator do nothing
            return
        try:
            self.Calc_List = list()  # Clear the Calulation list Before adding elements
            # Appending the elements of Display list to Calculation list with some changes as follows
            for i in range(len(self.Display_List)):
                if self.Display_List[i] == '^': # If the operator is ^ then append ** 
                    self.Calc_List.append('**')
                elif self.Display_List[i] == '(' and i > 0 and self.Display_List[i-1] not in ['+','*','/','-','.','%','^']:   
                    self.Calc_List.append("*")  # If there is a Left Bracket and there is no operator before it then add * 
                    self.Calc_List.append("(")  # For example 1(1+3) will be 1*(1+3) and if the Right Bracket is the first element then do nothing and append it
                elif self.Display_List[i] == ')' and i+1 != len(self.Display_List)  and self.Display_List[i+1] not in ['+','*','/','-','.','%',')']:
                    self.Calc_List.append(")")  # If there is a Right Bracket and there is no operator after it then add *
                    self.Calc_List.append("*")  # For example (1+5)6 will be (1+5)*6 and if Left Bracket is the last element then do nothing and append it
                else:
                    self.Calc_List.append(self.Display_List[i])
            answer = eval("".join(self.Calc_List)) # Evaluating after joining the list to string
            self.Answer.setText(str(answer))
            
        except ZeroDivisionError:
            self.Answer.setText("Infinite!!!")
        except SyntaxError:
            self.Answer.setText("Syntax Error!!!")
        except Exception as e:
            print(self.Calc_List)
            print(str(e))
            pass


# Initializing the app
app = QApplication(sys.argv)
Calc = Calculator()
Calc.setFixedWidth(346)
Calc.setFixedHeight(506)
Calc.show()
sys.exit(app.exec_())