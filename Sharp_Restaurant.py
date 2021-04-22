import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import mysql.connector
import mysql.connector
from UiMain import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import threading

hackust_db = mysql.connector.connect(
    host="hackust-garyt.cteyronn0mjg.us-east-2.rds.amazonaws.com",
    user="developer",
    password="hackUST258",
    database='hackust_DB',
    auth_plugin='mysql_native_password'
)

role = "None"
cashier=[]
cash=[]
creditcard=[]


class MainWindow(QMainWindow):
    def __init__(self):
        global role
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.Login_Page)
        self.ui.Login_Page_btn_login.clicked.connect(self.Login)
        self.ui.Number_Of_People_Input_Page_btn_comfirm.clicked.connect(self.NoOfPeopleInput)

        self.ui.Table_Order_Page_btn_food_ordered.clicked.connect(self.Table_Order_Page_pop_up)
        self.ui.Food_Ordered_Widget_btn_back.clicked.connect(self.Table_Order_Page_go_down)
        self.ui.Table_Order_Page_btn_next_page.clicked.connect(self.Table_Order_Page_next_page)
        self.ui.Table_Order_Page_btn_previou_page.clicked.connect(self.Table_Order_Page_pre_page)
        self.ui.Food_Ordered_Widget_btn_order_now.clicked.connect(self.Table_Order_Page_order_now)
        self.ui.Food_Ordered_Widget_btn_check.clicked.connect(self.Table_Order_Page_check_now)

        self.ui.Waiter_Order_Page_btn_food_ordered.clicked.connect(self.Waiter_Order_Page_pop_up)
        self.ui.Waiter_Food_Ordered_Widget_btn_back.clicked.connect(self.Waiter_Order_Page_go_down)
        self.ui.Waiter_Order_Page_btn_next_page.clicked.connect(self.Waiter_Order_Page_next_page)
        self.ui.Waiter_Order_Page_btn_previou_page.clicked.connect(self.Waiter_Order_Page_pre_page)
        self.ui.Waiter_Food_Ordered_Widget_btn_order_cash.clicked.connect(self.Waiter_Order_Page_order_cash)
        self.ui.Waiter_Food_Ordered_Widget_btn_order_credit_card.clicked.connect(
            self.Waiter_Order_Page_order_credit_card)
        self.ui.Waiter_Order_Page_btn_back_2.clicked.connect(self.back_to_waiter_page)
        self.language = "e"

        self.ui.Waiter_Page_btn_check_table_1.clicked.connect(self.Table1)
        self.ui.Waiter_Page_btn_check_table_2.clicked.connect(self.Table2)
        self.ui.Waiter_Page_btn_check_table_3.clicked.connect(self.Table3)
        self.ui.Waiter_Page_btn_check_table_4.clicked.connect(self.Table4)
        self.ui.Waiter_Page_btn_check_table_5.clicked.connect(self.Table5)
        self.ui.Waiter_Page_btn_check_table_6.clicked.connect(self.Table6)
        self.ui.Waiter_Page_btn_takeaway_order.clicked.connect(self.TakeAway)
        self.ui.Cashier_Page_btn_cash.clicked.connect(self.Cash)
        self.ui.Cashier_Page_btn_credit_card.clicked.connect(self.CreditCard)
        self.ui.Cashier_Page_btn_back.clicked.connect(self.CashierBack)
        self.ui.Cash_Payment_Page_btn_back.clicked.connect(self.CashBack)
        self.ui.Cash_Payment_Page_btn_confirm.clicked.connect(self.CashConfirm)
        self.ui.Credit_Card_Payment_Page_btn_confirm.clicked.connect(self.CreditConfirm)
        self.ui.Credit_Card_Payment_Page_btn_back.clicked.connect(self.CreditBack)
        self.ui.Statistics_Page_btn_7_days.clicked.connect(self.colorchange_7days)
        self.ui.Statistics_Page_btn_30_days.clicked.connect(self.colorchange_30days)
        self.ui.Statistics_Page_btn_365_days.clicked.connect(self.colorchange_365days)
        self.ui.Cash_Payment_Page_input_paid.textChanged.connect(self.updataQ)

    def updataQ(self):
        try:
            self.q = float(self.ui.Cash_Payment_Page_input_paid.text())
            self.ui.Cash_Payment_Page_label_change_price.setText("$" + str(round(float(self.q) - float(self.z),2)))
        except:
            pass

    def SetUpKitchen_Bar(self):
        self.Bar_or_Kitchen=""
        self.dish_on_screen = 0
        self.on_screen_order_id = [[],[],[],[]]
        self.maxDish = 3
        if(self.ui.Kitchen_Bar_Page_label_name.text()=="Bar"):
            self.Bar_or_Kitchen = "2"
        else:
            self.Bar_or_Kitchen = "1"

        self.Kitchen_Bar_Page_label_array = [
            [self.ui.Kitchen_Bar_Page_btn_dish_1, self.ui.Kitchen_Bar_Page_image_dish_1,
             self.ui.Kitchen_Bar_Page_food_name_dish_1, self.ui.Kitchen_Bar_Page_food_quantity_dish_1,
             self.ui.Kitchen_Bar_Page_timer_dish_1,self.ui.Kitchen_Bar_Page_dish_1],
            [self.ui.Kitchen_Bar_Page_btn_dish_2, self.ui.Kitchen_Bar_Page_image_dish_2,
             self.ui.Kitchen_Bar_Page_food_name_dish_2, self.ui.Kitchen_Bar_Page_food_quantity_dish_2,
             self.ui.Kitchen_Bar_Page_timer_dish_2,self.ui.Kitchen_Bar_Page_dish_2],
            [self.ui.Kitchen_Bar_Page_btn_dish_3, self.ui.Kitchen_Bar_Page_image_dish_3,
             self.ui.Kitchen_Bar_Page_food_name_dish_3, self.ui.Kitchen_Bar_Page_food_quantity_dish_3,
             self.ui.Kitchen_Bar_Page_timer_dish_3,self.ui.Kitchen_Bar_Page_dish_3],
            [self.ui.Kitchen_Bar_Page_btn_dish_4, self.ui.Kitchen_Bar_Page_image_dish_4,
             self.ui.Kitchen_Bar_Page_food_name_dish_4, self.ui.Kitchen_Bar_Page_food_quantity_dish_4,
             self.ui.Kitchen_Bar_Page_timer_dish_4,self.ui.Kitchen_Bar_Page_dish_4]
        ]
        self.GetUpdatePendingDish()
        self.mainTimer = QTimer(self)
        self.mainTimer.timeout.connect(self.MainKitchenTimer)
        self.mainTimer.start(10000)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.TimerUpdate_1)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.TimerUpdate_2)
        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.TimerUpdate_3)
        self.timer4 = QTimer(self)
        self.timer4.timeout.connect(self.TimerUpdate_4)
        self.timerArray=[self.timer1,self.timer2,self.timer3,self.timer4]
        for i in range(4):
            self.Kitchen_Bar_Page_label_array[i][0].clicked.connect(self.KitchenBtnOnClick)
            if self.length>0:
                self.Kitchen_Bar_Page_label_array[i][5].show()

                self.Kitchen_Bar_Page_label_array[i][4].setText("00 min 00 sec")
                self.timerArray[i].start(1000)
                self.merged_dish = 0
                tempqu = self.Kitchen_Bar_Page_pending_dish_records[0][1]
                tempname = self.Kitchen_Bar_Page_pending_dish_records[0][0]
                index = 0
                self.order_id=self.Kitchen_Bar_Page_pending_dish_records[0][2]
                self.on_screen_order_id[i].append(self.order_id)
                self.item_id = self.Kitchen_Bar_Page_pending_dish_records[0][3]
                self.PendingToCooking()
                self.GetUpdatePendingDish()
                for check_row in self.Kitchen_Bar_Page_pending_dish_records:
                    if (str(check_row[0]) == str(tempname) and int(check_row[1]) + int(tempqu) <= 3):
                        tempqu = int(tempqu) +int(check_row[1])
                        self.on_screen_order_id[i].append(check_row[2])
                        self.order_id = check_row[2]
                        self.merged_dish = self.merged_dish+1
                        self.PendingToCooking()

                    if tempqu>=3:
                        break
                    index = index +1
                self.GetUpdatePendingDish()
                self.Kitchen_Bar_Page_label_array[i][2].setText(str(tempname))
                text = "x"+str(tempqu)
                self.Kitchen_Bar_Page_label_array[i][3].setText(str(text))
                iname = str(self.item_id)+".jpg"
                Ipic = QPixmap(iname)
                self.Kitchen_Bar_Page_label_array[i][1].setPixmap(Ipic)
                self.dish_on_screen =self.dish_on_screen+1
            else:
                self.Kitchen_Bar_Page_label_array[i][5].hide()
                self.timerArray[i].stop()
        text = str(self.length)+" Order Left"
        self.ui.Kitchen_Bar_Page_label_dish_left.setText(text)

    def MainKitchenTimer(self):
        if self.dish_on_screen <4:
            self.GetUpdatePendingDish()
            if(len(self.Kitchen_Bar_Page_pending_dish_records)!=0):
                for i in range(4):
                    if(self.Kitchen_Bar_Page_label_array[i][5].isVisible()==False):
                        self.Kitchen_Bar_Page_label_array[i][5].show()

                        self.Kitchen_Bar_Page_label_array[i][4].setText("00 min 00 sec")
                        self.timerArray[i].start(1000)
                        self.merged_dish = 0
                        tempqu = self.Kitchen_Bar_Page_pending_dish_records[0][1]
                        tempname = self.Kitchen_Bar_Page_pending_dish_records[0][0]
                        index = 0
                        self.order_id = self.Kitchen_Bar_Page_pending_dish_records[0][2]
                        self.on_screen_order_id[i].append(self.order_id)
                        self.item_id = self.Kitchen_Bar_Page_pending_dish_records[0][3]
                        self.PendingToCooking()
                        self.GetUpdatePendingDish()
                        for check_row in self.Kitchen_Bar_Page_pending_dish_records:
                            if (str(check_row[0]) == str(tempname) and int(check_row[1]) + int(tempqu) <= 3):
                                tempqu = int(tempqu) + int(check_row[1])
                                self.on_screen_order_id[i].append(check_row[2])
                                self.order_id = check_row[2]
                                self.merged_dish = self.merged_dish + 1
                                self.PendingToCooking()

                            if tempqu >= 3:
                                break
                            index = index + 1
                        self.GetUpdatePendingDish()
                        self.Kitchen_Bar_Page_label_array[i][2].setText(str(tempname))
                        text = "x" + str(tempqu)
                        self.Kitchen_Bar_Page_label_array[i][3].setText(str(text))
                        iname = str(self.item_id) + ".jpg"
                        Ipic = QPixmap(iname)
                        self.Kitchen_Bar_Page_label_array[i][1].setPixmap(Ipic)
                        self.dish_on_screen = self.dish_on_screen + 1

    def TimerUpdate_1(self):
        min = int(self.Kitchen_Bar_Page_label_array[0][4].text()[0:2])
        sec = int(self.Kitchen_Bar_Page_label_array[0][4].text()[7:9])
        sec = int(sec)+1
        if int(sec) < 10:
            sec = str(0)+str(sec)
        elif int(sec) == 60:
            min = int(min)+1
        if int(min) <10:
            min = str(0)+str(min)
        text  =str(min)+" min "+str(sec)+" sec"
        self.Kitchen_Bar_Page_label_array[0][4].setText(str(text))
    def TimerUpdate_2(self):
        min = int(self.Kitchen_Bar_Page_label_array[1][4].text()[0:2])
        sec = int(self.Kitchen_Bar_Page_label_array[1][4].text()[7:9])
        sec = int(sec)+1
        if int(sec) < 10:
            sec = str(0)+str(sec)
        elif int(sec) == 60:
            min = int(min)+1
        if int(min) <10:
            min = str(0)+str(min)
        text  =str(min)+" min "+str(sec)+" sec"
        self.Kitchen_Bar_Page_label_array[1][4].setText(str(text))
    def TimerUpdate_3(self):
        min = int(self.Kitchen_Bar_Page_label_array[2][4].text()[0:2])
        sec = int(self.Kitchen_Bar_Page_label_array[2][4].text()[7:9])
        sec = int(sec)+1
        if int(sec) < 10:
            sec = str(0)+str(sec)
        elif int(sec) == 60:
            min = int(min)+1
        if int(min) <10:
            min = str(0)+str(min)
        text  =str(min)+" min "+str(sec)+" sec"
        self.Kitchen_Bar_Page_label_array[2][4].setText(str(text))
    def TimerUpdate_4(self):
        min = int(self.Kitchen_Bar_Page_label_array[3][4].text()[0:2])
        sec = int(self.Kitchen_Bar_Page_label_array[3][4].text()[7:9])
        sec = int(sec)+1
        if int(sec) < 10:
            sec = str(0)+str(sec)
        elif int(sec) == 60:
            min = int(min)+1
        if int(min) <10:
            min = str(0)+str(min)
        text  =str(min)+" min "+str(sec)+" sec"
        self.Kitchen_Bar_Page_label_array[3][4].setText(str(text))
    def KitchenBtnOnClick(self):
        sender_index = -1
        for i in range(4):
            if (self.sender()==self.Kitchen_Bar_Page_label_array[i][0]):
                sender_index = i
                break
        self.CookingToReady(sender_index)
        self.dish_on_screen = self.dish_on_screen - 1
        if self.length >0:
            self.Kitchen_Bar_Page_label_array[sender_index][5].show()
            self.merged_dish = 0
            self.Kitchen_Bar_Page_label_array[i][4].setText("00 min 00 sec")
            self.timerArray[i].start(1000)
            tempqu = self.Kitchen_Bar_Page_pending_dish_records[0][1]
            tempname = self.Kitchen_Bar_Page_pending_dish_records[0][0]
            index = 0
            self.order_id = self.Kitchen_Bar_Page_pending_dish_records[0][2]
            self.on_screen_order_id[sender_index].append(self.order_id)
            self.item_id = self.Kitchen_Bar_Page_pending_dish_records[0][3]
            self.PendingToCooking()
            self.GetUpdatePendingDish()
            for check_row in self.Kitchen_Bar_Page_pending_dish_records:
                if (str(check_row[0]) == str(tempname) and int(check_row[1]) + int(tempqu) <= 3):
                    tempqu = int(tempqu) + int(check_row[1])
                    self.on_screen_order_id[sender_index].append(check_row[2])
                    self.order_id = check_row[2]
                    self.merged_dish = self.merged_dish + 1
                    self.PendingToCooking()

                if tempqu >= 3:
                    break
                index = index + 1
            self.GetUpdatePendingDish()
            self.Kitchen_Bar_Page_label_array[sender_index][2].setText(str(tempname))
            text = "x" + str(tempqu)
            self.Kitchen_Bar_Page_label_array[sender_index][3].setText(str(text))
            iname = str(self.item_id) + ".jpg"
            Ipic = QPixmap(iname)
            self.Kitchen_Bar_Page_label_array[sender_index][1].setPixmap(Ipic)
            self.dish_on_screen = self.dish_on_screen + 1
        else:
            self.Kitchen_Bar_Page_label_array[sender_index][5].hide()
            self.timerArray[i].stop()
        text = str(self.length) + " Order Left"
        self.ui.Kitchen_Bar_Page_label_dish_left.setText(text)




    def CookingToReady(self,block):
        for i in self.on_screen_order_id[block]:
            sql_select_Query = """UPDATE customer_order SET order_status = '2', ready_time = CURRENT_TIME  WHERE (order_id =  '"""+str(i)+"""');"""
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            hackust_db.commit()

    def PendingToCooking(self):
        sql_select_Query = """UPDATE customer_order SET order_status = '1' WHERE (order_id = '"""+str(self.order_id)+"""');"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        hackust_db.commit()

    def GetUpdatePendingDish(self):
        sql_select_Query = """SELECT a.item_ename, b.order_qty,b.order_id,a.item_id
               FROM item_name AS a INNER JOIN customer_order AS b ON a.item_id=b.item_id
               INNER JOIN menu AS c ON c.menu_id = a.item_id
               WHERE b.order_status = 0 AND c.responsible =  """ + str(self.Bar_or_Kitchen) + """ order by b.order_time;
               """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Kitchen_Bar_Page_pending_dish_records = cursor.fetchall()
        self.length = len(self.Kitchen_Bar_Page_pending_dish_records)


    # ==================================================================================
    def back_to_waiter_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)

    def Waiter_Order_Page_order_cash(self):
        self.ui.Cashier_Page_label_title.setText("Takeaway")
        self.waiter_payment = True
        for i in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                       len(self.Waiter_Order_Page_ordered_food_array)):
            rec_id = self.receipt_id
            item_id = self.Waiter_Order_Page_ordered_food_array[i][3]
            qu = self.Waiter_Order_Page_ordered_food_array[i][1]
            Current_time = datetime.datetime.now().strftime("%H:%M:%S")

            sql_select_Query = """INSERT INTO customer_order (receipt_id, item_id, order_qty, order_status, order_time)
    VALUES ('""" + str(rec_id) + """', '""" + str(item_id) + """', '""" + str(qu) + """', 1, '""" + str(Current_time) + """');    
               """
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            sql_select_Query = """ UPDATE menu SET realtime_quota = realtime_quota-""" + str(
                qu) + """ WHERE (menu_id = '""" + str(item_id) + """');"""
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            cursor.execute(sql_select_Query)
            sql_select_Query = """UPDATE receipt SET checking_time = CURRENT_TIME, checking_status = '1' WHERE (receipt_id = '""" + str(
                self.receipt_id) + """');"""
            cursor = hackust_db.cursor()
            hackust_db.commit()
        self.Waiter_Order_Page_Number_submited_food_ordered = len(self.Waiter_Order_Page_ordered_food_array)
        self.updatedish_Waiter()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cash_Payment_Page)
        self.Cash()

    def Waiter_Order_Page_order_credit_card(self):
        self.ui.Cashier_Page_label_title.setText("Takeaway")
        self.waiter_payment = True
        for i in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                       len(self.Waiter_Order_Page_ordered_food_array)):
            rec_id = self.receipt_id
            item_id = self.Waiter_Order_Page_ordered_food_array[i][3]
            qu = self.Waiter_Order_Page_ordered_food_array[i][1]
            Current_time = datetime.datetime.now().strftime("%H:%M:%S")

            sql_select_Query = """INSERT INTO customer_order (receipt_id, item_id, order_qty, order_status, order_time)
    VALUES ('""" + str(rec_id) + """', '""" + str(item_id) + """', '""" + str(qu) + """', 0, '""" + str(Current_time) + """');    
               """
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            sql_select_Query = """ UPDATE menu SET realtime_quota = realtime_quota-""" + str(
                qu) + """ WHERE (menu_id = '""" + str(item_id) + """');"""
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            sql_select_Query = """UPDATE receipt SET checking_time = CURRENT_TIME, checking_status = '1' WHERE (receipt_id = '"""+str(self.receipt_id)+"""');"""
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)

            hackust_db.commit()

        self.Waiter_Order_Page_Number_submited_food_ordered = len(self.Waiter_Order_Page_ordered_food_array)
        self.updatedish_Waiter()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Credit_Card_Payment_Page)
        self.CreditCard()

    def Waiter_Order_Page_de_q(self):
        for i in range(3):
            if (self.sender() == self.Waiter_Order_Page_food_quantity_array[i][2]):
                if (int(self.Waiter_Order_Page_food_quantity_array[i][0].text()) > 0):
                    q = int(self.Waiter_Order_Page_food_quantity_array[i][0].text()) - 1
                    self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(q))
                    if int(self.Waiter_Order_Page_food_quantity_array[i][0].text()) == 0:
                        for row in self.Waiter_Order_Page_ordered_food_array[
                                   self.Waiter_Order_Page_Number_submited_food_ordered:]:
                            if (row[0] == self.Waiter_Order_Page_food_name_array[i].text()):
                                self.Waiter_Order_Page_ordered_food_array.remove(row)
                                break
                        for row in self.Waiter_Order_Page_ordered_food_widget_array:
                            if (row[0].text() == self.Waiter_Order_Page_food_name_array[i].text()):
                                row[0].deleteLater()
                                row[1].deleteLater()
                                row[2].deleteLater()
                                row[3].deleteLater()
                                self.Waiter_Order_Page_ordered_food_widget_array.remove(row)

                                break
                    else:
                        for j in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                                       len(self.Waiter_Order_Page_ordered_food_array)):
                            if (self.Waiter_Order_Page_ordered_food_array[j][0] ==
                                    self.Waiter_Order_Page_food_name_array[
                                        i].text()):
                                self.Waiter_Order_Page_ordered_food_array[j][1] = \
                                    self.Waiter_Order_Page_food_quantity_array[i][0].text()
                                self.Waiter_Order_Page_ordered_food_array[j][2] = str(
                                    float(self.Waiter_Order_Page_food_price_array[i].text()[1:]) * float(
                                        self.Waiter_Order_Page_food_quantity_array[i][0].text()))
                                text = "x" + self.Waiter_Order_Page_ordered_food_array[j][1]
                                self.Waiter_Order_Page_ordered_food_widget_array[j][1].setText(text)
                                text = "$" + self.Waiter_Order_Page_ordered_food_array[j][2]
                                self.Waiter_Order_Page_ordered_food_widget_array[j][2].setText(text)
                break
        self.total = float(0)
        for row in self.Waiter_Order_Page_ordered_food_array:
            self.total = self.total + float(row[2])
        if self.language =="e":
            text = "Food Ordered          $" + str(self.total)
        else:
            text = "食品訂單          $" + str(self.total)
        self.ui.Waiter_Order_Page_btn_food_ordered.setText(text)
        text = "$" + str(self.total)
        self.ui.Waiter_Food_Ordered_Widget_label_total_price.setText(text)
    def Waiter_Order_Page_add_q(self):
        for i in range(3):
            if (self.sender() == self.Waiter_Order_Page_food_quantity_array[i][1]):
                q = int(self.Waiter_Order_Page_food_quantity_array[i][0].text()) + 1
                self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(q))
                if int(self.Waiter_Order_Page_food_quantity_array[i][0].text()) == 1:
                    self.Waiter_Order_Page_Number_food_ordered = int(self.Waiter_Order_Page_Number_food_ordered) + 1
                    food_order = [self.Waiter_Order_Page_food_name_array[i].text(),
                                  self.Waiter_Order_Page_food_quantity_array[i][0].text(), str(
                            float(self.Waiter_Order_Page_food_price_array[i].text()[1:]) * float(
                                self.Waiter_Order_Page_food_quantity_array[i][0].text())),
                                  self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][2]]
                    self.Food_Ordered_Widget_food_item = QHBoxLayout()
                    self.Food_Ordered_Widget_food_item.setSizeConstraint(QLayout.SetMinimumSize)
                    list_name = "Food_Ordered_Widget_food_item_" + str(self.Waiter_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_item.setObjectName(str(list_name))

                    self.Food_Ordered_Widget_food_name = QLabel(
                        self.ui.Waiter_Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_name.setMaximumSize(QSize(300, 200))
                    self.Food_Ordered_Widget_food_name.setWordWrap(True)
                    self.Food_Ordered_Widget_food_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_name_" + str(self.Waiter_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_name.setObjectName(str(list_name))
                    self.Food_Ordered_Widget_food_name.setText(str(food_order[0]))
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_name)

                    self.Food_Ordered_Widget_food_quantity = QLabel(
                        self.ui.Waiter_Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_quantity.setMaximumSize(QSize(16777215, 45))
                    self.Food_Ordered_Widget_food_quantity.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_quantity_" + str(self.Waiter_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_quantity.setObjectName(str(list_name))
                    text = "x" + str(food_order[1])
                    self.Food_Ordered_Widget_food_quantity.setText(text)
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_quantity)

                    self.Food_Ordered_Widget_food_price = QLabel(
                        self.ui.Waiter_Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_price.setMaximumSize(QSize(16777215, 45))
                    self.Food_Ordered_Widget_food_price.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_price_" + str(self.Waiter_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_price.setObjectName(str(list_name))

                    text = "$" + str(food_order[2])
                    self.Food_Ordered_Widget_food_price.setText(str(text))
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_price)
                    self.ui.Waiter_Food_Ordered_Widget_verticalLayout.addLayout(self.Food_Ordered_Widget_food_item)

                    self.Waiter_Order_Page_ordered_food_array.append(food_order)
                    food_widget_array = [self.Food_Ordered_Widget_food_name, self.Food_Ordered_Widget_food_quantity,
                                         self.Food_Ordered_Widget_food_price, self.Food_Ordered_Widget_food_item]

                    self.Waiter_Order_Page_ordered_food_widget_array.append(food_widget_array)

                else:
                    for j in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                                   len(self.Waiter_Order_Page_ordered_food_array)):
                        if (self.Waiter_Order_Page_ordered_food_array[j][0] == self.Waiter_Order_Page_food_name_array[
                            i].text()):
                            self.Waiter_Order_Page_ordered_food_array[j][1] = \
                                self.Waiter_Order_Page_food_quantity_array[i][
                                    0].text()
                            self.Waiter_Order_Page_ordered_food_array[j][2] = str(
                                float(self.Waiter_Order_Page_food_price_array[i].text()[1:]) * float(
                                    self.Waiter_Order_Page_food_quantity_array[i][0].text()))
                            text = "x" + self.Waiter_Order_Page_ordered_food_array[j][1]
                            self.Waiter_Order_Page_ordered_food_widget_array[j][1].setText(text)
                            text = "$" + self.Waiter_Order_Page_ordered_food_array[j][2]
                            self.Waiter_Order_Page_ordered_food_widget_array[j][2].setText(text)
                break
        self.total = float(0)
        for row in self.Waiter_Order_Page_ordered_food_array:
            self.total = self.total + float(row[2])
        if self.language == "e":
            text = "Food Ordered          $" + str(self.total)
        else:
            text = "食品訂單          $" + str(self.total)
        self.ui.Waiter_Order_Page_btn_food_ordered.setText(text)
        text = "$" + str(self.total)
        self.ui.Waiter_Food_Ordered_Widget_label_total_price.setText(text)
    def Waiter_Order_Page_pop_up(self):
        self.ui.Waiter_Food_Ordered_Widget.raise_()

    def Waiter_Order_Page_go_down(self):
        self.ui.Waiter_Food_Ordered_Widget.lower()

    def Waiter_ChangeToChi(self):
        global hackust_db
        self.ui.Waiter_Order_Page_btn_chi.setStyleSheet("""
        background-color: rgb(249, 234, 154);
        font-size: 18px;
        font-weight:500;
        color: rgb(41, 14, 4);
        """)
        self.ui.Waiter_Order_Page_btn_eng.setStyleSheet("""border-bottom-right-radius: 19px;
        border-bottom-left-radius: 19px; 
        background-color: rgb(232, 151, 0);
        border:none; 
        font-size: 18px; 
        font-weight:500;
        color: rgb(41, 14, 4);""")
        self.language = "c"
        self.updatedish_Waiter()
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")

        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
                        FROM item_name AS a INNER JOIN provide_time AS b 
                        ON a.item_id = b.menu_category
                        WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Waiter_Order_Page_records = cursor.fetchall()
        for i in range(len(self.Waiter_Order_Page_records)):
            self.Waiter_Order_Page_tab_btn_array[i].setText(self.Waiter_Order_Page_records[i][0])
        Waiter_Order_Page_total_price = self.total
        temp = "食品訂單          $" + str(Waiter_Order_Page_total_price)
        self.ui.Waiter_Order_Page_btn_food_ordered.setText(str(temp))
        self.ui.Table_Order_Page_btn_food_ordered.setText(str(temp))
        self.ui.Table_Order_Page_label_food_source_dish_1.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_dish_2.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_dish_3.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_1_dish_1.setText("美國")
        self.ui.Table_Order_Page_label_food_source_1_dish_2.setText("日本")
        self.ui.Table_Order_Page_label_food_source_1_dish_3.setText("歐洲")

    def Waiter_ChangeToEng(self):
        global hackust_db
        self.ui.Waiter_Order_Page_btn_eng.setStyleSheet("""border-bottom-right-radius: 19px;
        border-bottom-left-radius: 19px; 
        background-color: rgb(249, 234, 154);
        font-size: 18px;
        font-weight:500;
        color: rgb(41, 14, 4);
        """)
        self.ui.Waiter_Order_Page_btn_chi.setStyleSheet("""background-color: rgb(232, 151, 0);
        border:none; 
        font-size: 18px; 
        font-weight:500;
        color: rgb(41, 14, 4);""")
        self.language = "e"
        self.updatedish_Waiter()

        Current_time = datetime.datetime.now().strftime("%H:%M:%S")

        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
                FROM item_name AS a INNER JOIN provide_time AS b 
                ON a.item_id = b.menu_category
                WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Waiter_Order_Page_records = cursor.fetchall()
        for i in range(len(self.Waiter_Order_Page_records)):
            self.Waiter_Order_Page_tab_btn_array[i].setText(self.Waiter_Order_Page_records[i][0])

        Waiter_Order_Page_total_price = self.total

        text = "食品訂單          $" + str(Waiter_Order_Page_total_price)
        self.ui.Waiter_Order_Page_btn_food_ordered.setText(str(text))
        self.ui.Table_Order_Page_label_food_source_dish_1.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_dish_2.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_dish_3.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_1_dish_1.setText("USA")
        self.ui.Table_Order_Page_label_food_source_1_dish_2.setText("Japan")
        self.ui.Table_Order_Page_label_food_source_1_dish_3.setText("Europe")

    def SetUpWaiterOrderPage(self):
        global role, hackust_db
        self.total = float(0)
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        Current_Date = str(datetime.date.today())
        table_name = str(self.ui.Login_Page_text_username.text())

        sql_select_Query = """INSERT INTO receipt ( user_id, no_of_ppl, receipt_date, in_time, order_type,responsible)
                         VALUES ('""" + str(table_name) + """', '1', '""" + str(
            Current_Date) + """', '""" + str(Current_time) + """', '0','T001');
                        """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        hackust_db.commit()
        sql_select_Query = """Select receipt_id from receipt where receipt_date='""" + str(
            Current_Date) + """' and in_time='""" + str(Current_time) + """' and user_id='""" + str(
            table_name) + """' and no_of_ppl='1' and responsible='T001';
                                        """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.receipt_id = records[0][0]
        self.Waiter_Order_Page_Number_food_ordered = 0
        self.Waiter_Order_Page_Number_submited_food_ordered = 0
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.Waiter_Order_Page_dish_page = 0
        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
        FROM item_name AS a INNER JOIN provide_time AS b 
        ON a.item_id = b.menu_category
        WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Waiter_Order_Page_records = cursor.fetchall()
        self.Waiter_Order_Page_ordered_food_array = []
        text = "Food Ordered          $" + str(self.total)
        self.ui.Waiter_Order_Page_btn_food_ordered.setText(str(text))
        self.ui.Waiter_Food_Ordered_Widget.lower()
        try:
            for row in self.Waiter_Order_Page_ordered_food_widget_array:
                row[0].deleteLater()
                row[1].deleteLater()
                row[2].deleteLater()
                row[3].deleteLater()
            self.Waiter_Order_Page_ordered_food_widget_array = []
        except:
            self.Waiter_Order_Page_ordered_food_widget_array = []
        self.Waiter_Order_Page_tab_btn_array = [self.ui.Waiter_Order_Page_btn_tab_1,
                                                self.ui.Waiter_Order_Page_btn_tab_2,
                                                self.ui.Waiter_Order_Page_btn_tab_3,
                                                self.ui.Waiter_Order_Page_btn_tab_4,
                                                self.ui.Waiter_Order_Page_btn_tab_5,
                                                self.ui.Waiter_Order_Page_btn_tab_6,
                                                self.ui.Waiter_Order_Page_btn_tab_7,
                                                self.ui.Waiter_Order_Page_btn_tab_8,
                                                self.ui.Waiter_Order_Page_btn_tab_9,
                                                self.ui.Waiter_Order_Page_btn_tab_10,
                                                self.ui.Waiter_Order_Page_btn_tab_11,
                                                self.ui.Waiter_Order_Page_btn_tab_12,
                                                self.ui.Waiter_Order_Page_btn_tab_13]
        self.Waiter_Order_Page_food_name_array = [self.ui.Waiter_Order_Page_label_food_name_dish_1,
                                                  self.ui.Waiter_Order_Page_label_food_name_dish_2,
                                                  self.ui.Waiter_Order_Page_label_food_name_dish_3]
        self.Waiter_Order_Page_food_price_array = [self.ui.Waiter_Order_Page_label_food_price_dish_1,
                                                   self.ui.Waiter_Order_Page_label_food_price_dish_2,
                                                   self.ui.Waiter_Order_Page_label_food_price_dish_3]
        self.Waiter_Order_Page_food_image_array = [self.ui.Waiter_Order_Page_label_image_dish_1,
                                                   self.ui.Waiter_Order_Page_label_image_dish_2,
                                                   self.ui.Waiter_Order_Page_label_image_dish_3]
        self.Waiter_Order_Page_food_source_array = [[self.ui.Waiter_Order_Page_label_food_source_1_dish_1,
                                                     self.ui.Waiter_Order_Page_label_food_source_2_dish_1,
                                                     self.ui.Waiter_Order_Page_label_food_source_3_dish_1],
                                                    [self.ui.Waiter_Order_Page_label_food_source_1_dish_2,
                                                     self.ui.Waiter_Order_Page_label_food_source_2_dish_2,
                                                     self.ui.Waiter_Order_Page_label_food_source_3_dish_2],
                                                    [self.ui.Waiter_Order_Page_label_food_source_1_dish_3,
                                                     self.ui.Waiter_Order_Page_label_food_source_2_dish_3,
                                                     self.ui.Waiter_Order_Page_label_food_source_3_dish_3]
                                                    ]
        self.Waiter_Order_Page_food_quantity_array = [[self.ui.Waiter_Order_Page_label_food_quantity_dish_1,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_increase_dish_1,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_decrease_dish_1],
                                                      [self.ui.Waiter_Order_Page_label_food_quantity_dish_2,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_increase_dish_2,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_decrease_dish_2],
                                                      [self.ui.Waiter_Order_Page_label_food_quantity_dish_3,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_increase_dish_3,
                                                       self.ui.Waiter_Order_Page_btn_food_quantity_decrease_dish_3]]

        self.Waiter_Order_Page_selected_cat = self.Waiter_Order_Page_records[0][1]
        self.updatedish_Waiter()
        for i in range(len(self.Waiter_Order_Page_records)):
            self.Waiter_Order_Page_tab_btn_array[i].setText(self.Waiter_Order_Page_records[i][0])
            self.Waiter_Order_Page_tab_btn_array[i].setStyleSheet("")

        self.Waiter_Order_Page_tab_btn_array[0].setStyleSheet("background-color: rgb(249, 234, 154);")
        if (len(self.Waiter_Order_Page_records) < 13):
            for i in range(len(self.Waiter_Order_Page_records), 13):
                self.Waiter_Order_Page_tab_btn_array[i].deleteLater()

        if self.setup == True:
            self.setup = False
            for i in range(3):
                self.Waiter_Order_Page_food_quantity_array[i][1].clicked.connect(self.Waiter_Order_Page_add_q)
                self.Waiter_Order_Page_food_quantity_array[i][2].clicked.connect(self.Waiter_Order_Page_de_q)
            for i in range(len(self.Waiter_Order_Page_records)):
                self.Waiter_Order_Page_tab_btn_array[i].clicked.connect(self.TabOnClick_Waiter)
            self.ui.Waiter_Order_Page_btn_chi.clicked.connect(self.Waiter_ChangeToChi)
            self.ui.Waiter_Order_Page_btn_eng.clicked.connect(self.Waiter_ChangeToEng)


    def TabOnClick_Waiter(self):
        Waiter_Order_Page_selected_stylesheet = """background-color: rgb(249, 234, 154);"""
        for i in range(len(self.Waiter_Order_Page_records)):
            if (self.Waiter_Order_Page_tab_btn_array[i].text() == self.sender().text()):
                self.Waiter_Order_Page_tab_btn_array[i].setStyleSheet(Waiter_Order_Page_selected_stylesheet)
                self.Waiter_Order_Page_selected_cat = self.Waiter_Order_Page_records[i][1]
                self.Waiter_Order_Page_dish_page = 0
                self.updatedish_Waiter()
            else:
                self.Waiter_Order_Page_tab_btn_array[i].setStyleSheet("")

    def Waiter_Order_Page_pre_page(self):
        if self.Waiter_Order_Page_dish_page > 0:
            self.Waiter_Order_Page_dish_page = self.Waiter_Order_Page_dish_page - 1
            self.updatedish_Waiter()

    def Waiter_Order_Page_next_page(self):
        if (len(self.Waiter_Order_Page_menu_item_records) - (self.Waiter_Order_Page_dish_page + 1) * 3) > 0:
            self.Waiter_Order_Page_dish_page = self.Waiter_Order_Page_dish_page + 1
            self.updatedish_Waiter()

    def updatedish_Waiter(self):
        global hackust_db

        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name, b.menu_price,a.item_id
        FROM item_name AS a INNER JOIN menu AS b
        ON a.item_id = b.menu_id
        WHERE (b.realtime_quota > 0 OR b.realtime_quota <= -1) AND b.menu_category = '""" + str(
            self.Waiter_Order_Page_selected_cat) + """';"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Waiter_Order_Page_menu_item_records = cursor.fetchall()
        length = len(self.Waiter_Order_Page_menu_item_records) - self.Waiter_Order_Page_dish_page * 3
        if (self.Waiter_Order_Page_dish_page == 0):
            self.ui.Waiter_Order_Page_btn_previou_page.setIcon(QIcon())
        else:
            self.ui.Waiter_Order_Page_btn_previou_page.setIcon(QIcon(':/image/back.png'))
        if (length >= 3):
            self.ui.Waiter_Order_Page_dish_1.show()
            self.ui.Waiter_Order_Page_dish_2.show()
            self.ui.Waiter_Order_Page_dish_3.show()

            for i in range(3):
                self.Waiter_Order_Page_food_name_array[i].setText(
                    str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0]))

                text = "$" + str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][1])
                self.Waiter_Order_Page_food_price_array[i].setText(str(text))
                self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(0))
                Iname = str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][2])+".jpg"
                pic = QPixmap(Iname)
                self.Waiter_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                               len(self.Waiter_Order_Page_ordered_food_array)):
                    if (str(self.Waiter_Order_Page_ordered_food_array[j][0]) == str(
                            self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0])):
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Waiter_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(0))
                if (length > 3):
                    self.ui.Waiter_Order_Page_btn_next_page.setIcon(QIcon(':/image/forward.png'))
                else:
                    self.ui.Waiter_Order_Page_btn_next_page.setIcon(QIcon())
        elif (length == 1):
            for i in range(1):
                self.Waiter_Order_Page_food_name_array[i].setText(
                    str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0]))
                text = "$" + str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][1])
                self.Waiter_Order_Page_food_price_array[i].setText(str(text))
                Iname = str(
                    self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][2]) + ".jpg"
                pic = QPixmap(Iname)
                self.Waiter_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                               len(self.Waiter_Order_Page_ordered_food_array)):
                    if (str(self.Waiter_Order_Page_ordered_food_array[j][0]) == str(
                            self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0])):
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Waiter_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(0))

            self.ui.Waiter_Order_Page_dish_1.show()
            self.ui.Waiter_Order_Page_dish_2.hide()
            self.ui.Waiter_Order_Page_dish_3.hide()
            self.ui.Waiter_Order_Page_btn_next_page.setIcon(QIcon())
        elif (length == 2):
            for i in range(2):
                self.Waiter_Order_Page_food_name_array[i].setText(
                    str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0]))
                text = "$" + str(self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][1])
                self.Waiter_Order_Page_food_price_array[i].setText(text)
                Iname = str(
                    self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][2]) + ".jpg"
                pic = QPixmap(Iname)
                self.Waiter_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Waiter_Order_Page_Number_submited_food_ordered,
                               len(self.Waiter_Order_Page_ordered_food_array)):
                    if (str(self.Waiter_Order_Page_ordered_food_array[j][0]) == str(
                            self.Waiter_Order_Page_menu_item_records[self.Waiter_Order_Page_dish_page * 3 + i][0])):
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Waiter_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Waiter_Order_Page_food_quantity_array[i][0].setText(str(0))

            self.ui.Waiter_Order_Page_dish_1.show()
            self.ui.Waiter_Order_Page_dish_2.show()
            self.ui.Waiter_Order_Page_dish_3.hide()
            self.ui.Waiter_Order_Page_btn_next_page.setIcon(QIcon())
        else:
            self.ui.Waiter_Order_Page_dish_1.hide()
            self.ui.Waiter_Order_Page_dish_2.hide()
            self.ui.Waiter_Order_Page_dish_3.hide()
            self.ui.Waiter_Order_Page_btn_next_page.setIcon(QIcon())

    # ======================================================================================================================================
    def Table_Order_Page_check_now(self):
        rec_id = self.receipt_id
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        sql_select_Query = """UPDATE receipt SET checking_time = '""" + str(
            Current_time) + """', checking_status = '1' WHERE (receipt_id = '""" + str(rec_id) + """');"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        hackust_db.commit()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Number_Of_People_Input_Page)
        self.ui.Number_Of_People_Input_Page_text_number_of_people.setText("Number of People")

    def Table_Order_Page_order_now(self):
        for i in range(self.Table_Order_Page_Number_submited_food_ordered,
                       len(self.Table_Order_Page_ordered_food_array)):
            rec_id = self.receipt_id
            item_id = self.Table_Order_Page_ordered_food_array[i][3]
            qu = self.Table_Order_Page_ordered_food_array[i][1]
            Current_time = datetime.datetime.now().strftime("%H:%M:%S")

            sql_select_Query = """INSERT INTO customer_order (receipt_id, item_id, order_qty, order_status, order_time)
 VALUES ('""" + str(rec_id) + """', '""" + str(item_id) + """', '""" + str(qu) + """', 0, '""" + str(Current_time) + """');    
            """
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            sql_select_Query = """ UPDATE menu SET realtime_quota = realtime_quota-""" + str(
                qu) + """ WHERE (menu_id = '""" + str(item_id) + """');"""
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)
            hackust_db.commit()
        self.Table_Order_Page_Number_submited_food_ordered = len(self.Table_Order_Page_ordered_food_array)
        self.updatedish()

    def Table_Order_Page_de_q(self):
        for i in range(3):
            if (self.sender() == self.Table_Order_Page_food_quantity_array[i][2]):
                if (int(self.Table_Order_Page_food_quantity_array[i][0].text()) > 0):
                    q = int(self.Table_Order_Page_food_quantity_array[i][0].text()) - 1
                    self.Table_Order_Page_food_quantity_array[i][0].setText(str(q))
                    if int(self.Table_Order_Page_food_quantity_array[i][0].text()) == 0:
                        for row in self.Table_Order_Page_ordered_food_array[
                                   self.Table_Order_Page_Number_submited_food_ordered:]:
                            if (row[0] == self.Table_Order_Page_food_name_array[i].text()):
                                self.Table_Order_Page_ordered_food_array.remove(row)
                                break
                        for row in self.Table_Order_Page_ordered_food_widget_array:
                            if (row[0].text() == self.Table_Order_Page_food_name_array[i].text()):
                                row[0].deleteLater()
                                row[1].deleteLater()
                                row[2].deleteLater()
                                row[3].deleteLater()
                                self.Table_Order_Page_ordered_food_widget_array.remove(row)

                                break
                    else:
                        for j in range(self.Table_Order_Page_Number_submited_food_ordered,
                                       len(self.Table_Order_Page_ordered_food_array)):
                            if (self.Table_Order_Page_ordered_food_array[j][0] == self.Table_Order_Page_food_name_array[
                                i].text()):
                                self.Table_Order_Page_ordered_food_array[j][1] = \
                                    self.Table_Order_Page_food_quantity_array[i][0].text()
                                self.Table_Order_Page_ordered_food_array[j][2] = str(
                                    float(self.Table_Order_Page_food_price_array[i].text()[1:]) * float(
                                        self.Table_Order_Page_food_quantity_array[i][0].text()))
                                text = "x" + self.Table_Order_Page_ordered_food_array[j][1]
                                self.Table_Order_Page_ordered_food_widget_array[j][1].setText(text)
                                text = "$" + self.Table_Order_Page_ordered_food_array[j][2]
                                self.Table_Order_Page_ordered_food_widget_array[j][2].setText(text)
                break
        self.total = float(0)
        for row in self.Table_Order_Page_ordered_food_array:
            self.total = self.total + float(row[2])
        if self.language == "e":
            text = "Food Ordered          $" + str(self.total)
        else:
            text = "食品訂單          $" + str(self.total)
        self.ui.Table_Order_Page_btn_food_ordered.setText(text)
        text = "$" + str(self.total)
        self.ui.Food_Ordered_Widget_label_total_price.setText(text)
    def Table_Order_Page_add_q(self):
        for i in range(3):
            if (self.sender() == self.Table_Order_Page_food_quantity_array[i][1]):
                q = int(self.Table_Order_Page_food_quantity_array[i][0].text()) + 1
                self.Table_Order_Page_food_quantity_array[i][0].setText(str(q))
                if int(self.Table_Order_Page_food_quantity_array[i][0].text()) == 1:
                    self.Table_Order_Page_Number_food_ordered = int(self.Table_Order_Page_Number_food_ordered) + 1
                    food_order = [self.Table_Order_Page_food_name_array[i].text(),
                                  self.Table_Order_Page_food_quantity_array[i][0].text(), str(
                            float(self.Table_Order_Page_food_price_array[i].text()[1:]) * float(
                                self.Table_Order_Page_food_quantity_array[i][0].text())),
                                  self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][2]]
                    self.Food_Ordered_Widget_food_item = QHBoxLayout()
                    self.Food_Ordered_Widget_food_item.setSizeConstraint(QLayout.SetMinimumSize)
                    list_name = "Food_Ordered_Widget_food_item_" + str(self.Table_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_item.setObjectName(str(list_name))

                    self.Food_Ordered_Widget_food_name = QLabel(
                        self.ui.Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_name.setMaximumSize(QSize(300, 200))
                    self.Food_Ordered_Widget_food_name.setWordWrap(True)
                    self.Food_Ordered_Widget_food_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_name_" + str(self.Table_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_name.setObjectName(str(list_name))
                    self.Food_Ordered_Widget_food_name.setText(str(food_order[0]))
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_name)

                    self.Food_Ordered_Widget_food_quantity = QLabel(
                        self.ui.Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_quantity.setMaximumSize(QSize(16777215, 45))
                    self.Food_Ordered_Widget_food_quantity.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_quantity_" + str(self.Table_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_quantity.setObjectName(str(list_name))
                    text = "x" + str(food_order[1])
                    self.Food_Ordered_Widget_food_quantity.setText(text)
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_quantity)

                    self.Food_Ordered_Widget_food_price = QLabel(
                        self.ui.Food_Ordered_Widget_food_ordered_context)
                    self.Food_Ordered_Widget_food_price.setMaximumSize(QSize(16777215, 45))
                    self.Food_Ordered_Widget_food_price.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    list_name = "Food_Ordered_Widget_food_price_" + str(self.Table_Order_Page_Number_food_ordered)
                    self.Food_Ordered_Widget_food_price.setObjectName(str(list_name))

                    text = "$" + str(food_order[2])
                    self.Food_Ordered_Widget_food_price.setText(str(text))
                    self.Food_Ordered_Widget_food_item.addWidget(self.Food_Ordered_Widget_food_price)
                    self.ui.Food_Ordered_Widget_verticalLayout.addLayout(self.Food_Ordered_Widget_food_item)

                    self.Table_Order_Page_ordered_food_array.append(food_order)
                    food_widget_array = [self.Food_Ordered_Widget_food_name, self.Food_Ordered_Widget_food_quantity,
                                         self.Food_Ordered_Widget_food_price, self.Food_Ordered_Widget_food_item]

                    self.Table_Order_Page_ordered_food_widget_array.append(food_widget_array)

                else:
                    for j in range(self.Table_Order_Page_Number_submited_food_ordered,
                                   len(self.Table_Order_Page_ordered_food_array)):
                        if (self.Table_Order_Page_ordered_food_array[j][0] == self.Table_Order_Page_food_name_array[
                            i].text()):
                            self.Table_Order_Page_ordered_food_array[j][1] = \
                            self.Table_Order_Page_food_quantity_array[i][0].text()
                            self.Table_Order_Page_ordered_food_array[j][2] = str(
                                float(self.Table_Order_Page_food_price_array[i].text()[1:]) * float(
                                    self.Table_Order_Page_food_quantity_array[i][0].text()))
                            text = "x" + self.Table_Order_Page_ordered_food_array[j][1]
                            self.Table_Order_Page_ordered_food_widget_array[j][1].setText(text)
                            text = "$" + self.Table_Order_Page_ordered_food_array[j][2]
                            self.Table_Order_Page_ordered_food_widget_array[j][2].setText(text)
                break
        self.total = float(0)
        for row in self.Table_Order_Page_ordered_food_array:
            self.total = self.total + float(row[2])
        if self.language == "e":
            text = "Food Ordered          $" + str(self.total)
        else:
            text = "食品訂單          $" + str(self.total)
        self.ui.Table_Order_Page_btn_food_ordered.setText(text)
        text = "$"+str(self.total)
        self.ui.Food_Ordered_Widget_label_total_price.setText(text)
    def Table_Order_Page_pop_up(self):
        self.ui.Food_Ordered_Widget.raise_()

    def Table_Order_Page_go_down(self):
        self.ui.Food_Ordered_Widget.lower()

    def Table_ChangeToChi(self):
        global hackust_db
        self.ui.Table_Order_Page_btn_chi.setStyleSheet("""
        background-color: rgb(249, 234, 154);
        font-size: 18px;
        font-weight:500;
        color: rgb(41, 14, 4);
        """)
        self.ui.Table_Order_Page_btn_eng.setStyleSheet("""border-bottom-right-radius: 19px;
        border-bottom-left-radius: 19px; 
        background-color: rgb(232, 151, 0);
        border:none; 
        font-size: 18px; 
        font-weight:500;
        color: rgb(41, 14, 4);""")
        self.language = "c"
        self.updatedish()
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")

        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
                        FROM item_name AS a INNER JOIN provide_time AS b 
                        ON a.item_id = b.menu_category
                        WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Table_Order_Page_records = cursor.fetchall()
        for i in range(len(self.Table_Order_Page_records)):
            self.Table_Order_Page_tab_btn_array[i].setText(self.Table_Order_Page_records[i][0])
        temp = self.ui.Table_Order_Page_label_people_num.text()
        for i in range(len(temp)):
            if temp[i] == ":":
                temp = temp[i + 2:]
                break
        temp = "人數: " + str(temp)
        self.ui.Table_Order_Page_label_people_num.setText(str(temp))
        temp = "檯號: " + str(self.ui.Login_Page_text_username.text()[-1])
        self.ui.Table_Order_Page_label_table_num.setText(str(temp))

        temp = "食品訂單          $" + str(self.total)
        self.ui.Table_Order_Page_btn_food_ordered.setText(str(temp))
        self.ui.Table_Order_Page_label_food_source_dish_1.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_dish_2.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_dish_3.setText("食材來源：")
        self.ui.Table_Order_Page_label_food_source_1_dish_1.setText("美國")
        self.ui.Table_Order_Page_label_food_source_1_dish_2.setText("日本")
        self.ui.Table_Order_Page_label_food_source_1_dish_3.setText("歐洲")

    def Table_ChangeToEng(self):
        global hackust_db
        self.ui.Table_Order_Page_btn_eng.setStyleSheet("""border-bottom-right-radius: 19px;
        border-bottom-left-radius: 19px; 
        background-color: rgb(249, 234, 154);
        font-size: 18px;
        font-weight:500;
        color: rgb(41, 14, 4);
        """)
        self.ui.Table_Order_Page_btn_chi.setStyleSheet("""background-color: rgb(232, 151, 0);
        border:none; 
        font-size: 18px; 
        font-weight:500;
        color: rgb(41, 14, 4);""")
        self.language = "e"
        self.updatedish()

        Current_time = datetime.datetime.now().strftime("%H:%M:%S")

        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
                FROM item_name AS a INNER JOIN provide_time AS b 
                ON a.item_id = b.menu_category
                WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Table_Order_Page_records = cursor.fetchall()
        for i in range(len(self.Table_Order_Page_records)):
            self.Table_Order_Page_tab_btn_array[i].setText(self.Table_Order_Page_records[i][0])
        temp = self.ui.Table_Order_Page_label_people_num.text()
        for i in range(len(temp)):
            if temp[i] == ":":
                temp = temp[i + 2:]
                break
        temp = "Number of People: " + str(temp)
        self.ui.Table_Order_Page_label_people_num.setText(str(temp))
        temp = "Table Number: " + str(self.ui.Login_Page_text_username.text()[-1])
        self.ui.Table_Order_Page_label_table_num.setText(str(temp))
        Table_Order_Page_total_price = self.total
        temp = "Food Ordered          $" + str(Table_Order_Page_total_price)
        self.ui.Table_Order_Page_btn_food_ordered.setText(str(temp))
        self.ui.Table_Order_Page_label_food_source_dish_1.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_dish_2.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_dish_3.setText("Food Source:")
        self.ui.Table_Order_Page_label_food_source_1_dish_1.setText("USA")
        self.ui.Table_Order_Page_label_food_source_1_dish_2.setText("Japan")
        self.ui.Table_Order_Page_label_food_source_1_dish_3.setText("Europe")

    def SetUpTableOrderPage(self):
        global role, hackust_db
        self.total = float(0)
        self.Table_Order_Page_Number_food_ordered = 0
        self.Table_Order_Page_Number_submited_food_ordered = 0
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.Table_Order_Page_dish_page = 0
        Current_time = "16:00:00"  # =================For testing =================
        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name,a.item_id
        FROM item_name AS a INNER JOIN provide_time AS b 
        ON a.item_id = b.menu_category
        WHERE '""" + str(Current_time) + """' BETWEEN b.start_time AND b.end_time;"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Table_Order_Page_records = cursor.fetchall()
        self.Table_Order_Page_ordered_food_array = []
        text = "Food Ordered          $" + str(self.total)
        self.ui.Table_Order_Page_btn_food_ordered.setText(str(text))
        self.ui.Food_Ordered_Widget.lower()
        try:
            for row in self.Table_Order_Page_ordered_food_widget_array:
                row[0].deleteLater()
                row[1].deleteLater()
                row[2].deleteLater()
                row[3].deleteLater()
            self.Table_Order_Page_ordered_food_widget_array = []
        except:
            self.Table_Order_Page_ordered_food_widget_array = []

        self.Table_Order_Page_tab_btn_array = [self.ui.Table_Order_Page_btn_tab_1, self.ui.Table_Order_Page_btn_tab_2,
                                               self.ui.Table_Order_Page_btn_tab_3, self.ui.Table_Order_Page_btn_tab_4,
                                               self.ui.Table_Order_Page_btn_tab_5, self.ui.Table_Order_Page_btn_tab_6,
                                               self.ui.Table_Order_Page_btn_tab_7, self.ui.Table_Order_Page_btn_tab_8,
                                               self.ui.Table_Order_Page_btn_tab_9, self.ui.Table_Order_Page_btn_tab_10,
                                               self.ui.Table_Order_Page_btn_tab_11, self.ui.Table_Order_Page_btn_tab_12,
                                               self.ui.Table_Order_Page_btn_tab_13]
        self.Table_Order_Page_food_name_array = [self.ui.Table_Order_Page_label_food_name_dish_1,
                                                 self.ui.Table_Order_Page_label_food_name_dish_2,
                                                 self.ui.Table_Order_Page_label_food_name_dish_3]
        self.Table_Order_Page_food_price_array = [self.ui.Table_Order_Page_label_food_price_dish_1,
                                                  self.ui.Table_Order_Page_label_food_price_dish_2,
                                                  self.ui.Table_Order_Page_label_food_price_dish_3]

        self.Table_Order_Page_food_image_array = [self.ui.Table_Order_Page_label_image_dish_1,
                                                self.ui.Table_Order_Page_label_image_dish_2,
                                                self.ui.Table_Order_Page_label_image_dish_3]

        self.Table_Order_Page_food_source_array = [[self.ui.Table_Order_Page_label_food_source_1_dish_1,
                                                    self.ui.Table_Order_Page_label_food_source_2_dish_1,
                                                    self.ui.Table_Order_Page_label_food_source_3_dish_1],
                                                   [self.ui.Table_Order_Page_label_food_source_1_dish_2,
                                                    self.ui.Table_Order_Page_label_food_source_2_dish_2,
                                                    self.ui.Table_Order_Page_label_food_source_3_dish_2],
                                                   [self.ui.Table_Order_Page_label_food_source_1_dish_3,
                                                    self.ui.Table_Order_Page_label_food_source_2_dish_3,
                                                    self.ui.Table_Order_Page_label_food_source_3_dish_3]
                                                   ]
        self.Table_Order_Page_food_quantity_array = [[self.ui.Table_Order_Page_label_food_quantity_dish_1,
                                                      self.ui.Table_Order_Page_btn_food_quantity_increase_dish_1,
                                                      self.ui.Table_Order_Page_btn_food_quantity_decrease_dish_1],
                                                     [self.ui.Table_Order_Page_label_food_quantity_dish_2,
                                                      self.ui.Table_Order_Page_btn_food_quantity_increase_dish_2,
                                                      self.ui.Table_Order_Page_btn_food_quantity_decrease_dish_2],
                                                     [self.ui.Table_Order_Page_label_food_quantity_dish_3,
                                                      self.ui.Table_Order_Page_btn_food_quantity_increase_dish_3,
                                                      self.ui.Table_Order_Page_btn_food_quantity_decrease_dish_3]]

        self.Table_Order_Page_selected_cat = self.Table_Order_Page_records[0][1]
        self.updatedish()
        for i in range(len(self.Table_Order_Page_records)):
            self.Table_Order_Page_tab_btn_array[i].setStyleSheet("")
            self.Table_Order_Page_tab_btn_array[i].setText(self.Table_Order_Page_records[i][0])

        self.Table_Order_Page_tab_btn_array[0].setStyleSheet("background-color: rgb(249, 234, 154);")

        if (len(self.Table_Order_Page_records) < 13):
            for i in range(len(self.Table_Order_Page_records), 13):
                self.Table_Order_Page_tab_btn_array[i].deleteLater()
        if self.setup == True:
            self.setup = False
            for i in range(3):
                self.Table_Order_Page_food_quantity_array[i][1].clicked.connect(self.Table_Order_Page_add_q)
                self.Table_Order_Page_food_quantity_array[i][2].clicked.connect(self.Table_Order_Page_de_q)
            for i in range(len(self.Table_Order_Page_records)):
                self.Table_Order_Page_tab_btn_array[i].clicked.connect(self.TabOnClick)
            self.ui.Table_Order_Page_btn_chi.clicked.connect(self.Table_ChangeToChi)
            self.ui.Table_Order_Page_btn_eng.clicked.connect(self.Table_ChangeToEng)



    def TabOnClick(self):

        Table_Order_Page_selected_stylesheet = """background-color: rgb(249, 234, 154);"""
        for i in range(len(self.Table_Order_Page_records)):
            if (self.Table_Order_Page_tab_btn_array[i].text() == self.sender().text()):
                self.Table_Order_Page_tab_btn_array[i].setStyleSheet(Table_Order_Page_selected_stylesheet)
                self.Table_Order_Page_selected_cat = self.Table_Order_Page_records[i][1]
                self.Table_Order_Page_dish_page = 0
                self.updatedish()
            else:
                self.Table_Order_Page_tab_btn_array[i].setStyleSheet("")

    def Table_Order_Page_pre_page(self):
        if self.Table_Order_Page_dish_page > 0:
            self.Table_Order_Page_dish_page = self.Table_Order_Page_dish_page - 1
            self.updatedish()

    def Table_Order_Page_next_page(self):
        if (len(self.Table_Order_Page_menu_item_records) - (self.Table_Order_Page_dish_page + 1) * 3) > 0:
            self.Table_Order_Page_dish_page = self.Table_Order_Page_dish_page + 1
            self.updatedish()

    def updatedish(self):
        global hackust_db

        sql_select_Query = """SELECT a.item_""" + str(self.language) + """name, b.menu_price,a.item_id
        FROM item_name AS a INNER JOIN menu AS b
        ON a.item_id = b.menu_id
        WHERE (b.realtime_quota > 0 OR b.realtime_quota <= -1) AND b.menu_category = '""" + str(
            self.Table_Order_Page_selected_cat) + """';"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        self.Table_Order_Page_menu_item_records = cursor.fetchall()
        length = len(self.Table_Order_Page_menu_item_records) - self.Table_Order_Page_dish_page * 3
        if (self.Table_Order_Page_dish_page == 0):
            self.ui.Table_Order_Page_btn_previou_page.setIcon(QIcon())
        else:
            self.ui.Table_Order_Page_btn_previou_page.setIcon(QIcon(':/image/back.png'))
        if (length >= 3):
            self.ui.Table_Order_Page_dish_1.show()
            self.ui.Table_Order_Page_dish_2.show()
            self.ui.Table_Order_Page_dish_3.show()

            for i in range(3):
                self.Table_Order_Page_food_name_array[i].setText(
                    str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0]))

                text = "$" + str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][1])
                self.Table_Order_Page_food_price_array[i].setText(str(text))
                self.Table_Order_Page_food_quantity_array[i][0].setText(str(0))
                Iname = str(
                    self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][2]) + ".jpg"
                pic = QPixmap(Iname)
                self.Table_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Table_Order_Page_Number_submited_food_ordered,
                               len(self.Table_Order_Page_ordered_food_array)):
                    if (str(self.Table_Order_Page_ordered_food_array[j][0]) == str(
                            self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0])):
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Table_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(0))
                if (length > 3):
                    self.ui.Table_Order_Page_btn_next_page.setIcon(QIcon(':/image/forward.png'))
                else:
                    self.ui.Table_Order_Page_btn_next_page.setIcon(QIcon())
        elif (length == 1):
            for i in range(1):
                self.Table_Order_Page_food_name_array[i].setText(
                    str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0]))
                text = "$" + str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][1])
                self.Table_Order_Page_food_price_array[i].setText(str(text))
                Iname = str(
                    self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][2]) + ".jpg"
                pic = QPixmap(Iname)
                self.Table_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Table_Order_Page_Number_submited_food_ordered,
                               len(self.Table_Order_Page_ordered_food_array)):
                    if (str(self.Table_Order_Page_ordered_food_array[j][0]) == str(
                            self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0])):
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Table_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(0))

            self.ui.Table_Order_Page_dish_1.show()
            self.ui.Table_Order_Page_dish_2.hide()
            self.ui.Table_Order_Page_dish_3.hide()
            self.ui.Table_Order_Page_btn_next_page.setIcon(QIcon())
        elif (length == 2):
            for i in range(2):
                self.Table_Order_Page_food_name_array[i].setText(
                    str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0]))
                text = "$" + str(self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][1])
                self.Table_Order_Page_food_price_array[i].setText(text)
                Iname = str(
                    self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][2]) + ".jpg"
                pic = QPixmap(Iname)
                self.Table_Order_Page_food_image_array[i].setPixmap(pic)
                for j in range(self.Table_Order_Page_Number_submited_food_ordered,
                               len(self.Table_Order_Page_ordered_food_array)):
                    if (str(self.Table_Order_Page_ordered_food_array[j][0]) == str(
                            self.Table_Order_Page_menu_item_records[self.Table_Order_Page_dish_page * 3 + i][0])):
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(
                            self.Table_Order_Page_ordered_food_array[j][1]))
                        break
                    else:
                        self.Table_Order_Page_food_quantity_array[i][0].setText(str(0))

            self.ui.Table_Order_Page_dish_1.show()
            self.ui.Table_Order_Page_dish_2.show()
            self.ui.Table_Order_Page_dish_3.hide()
            self.ui.Table_Order_Page_btn_next_page.setIcon(QIcon())
        else:
            self.ui.Table_Order_Page_dish_1.hide()
            self.ui.Table_Order_Page_dish_2.hide()
            self.ui.Table_Order_Page_dish_3.hide()
            self.ui.Table_Order_Page_btn_next_page.setIcon(QIcon())

    def NoOfPeopleInput(self):
        global hackust_db
        s = self.ui.Number_Of_People_Input_Page_text_number_of_people.text()
        try:
            int(s)
            temp = int(s)
            if (temp <= 0 or temp > 12):
                self.ui.Number_Of_People_Input_Page_label_invaild_input.setStyleSheet(
                    "font:16px;color: rgb(255, 0, 0);")
            else:
                self.ui.stackedWidget.setCurrentWidget(self.ui.Table_Order_Page)
                self.SetUpTableOrderPage()
                temp = "Number of People: " + str(temp)
                self.ui.Table_Order_Page_label_people_num.setText(temp)
                text = "Table Number: " + str(self.ui.Login_Page_text_username.text()[-1])
                self.ui.Table_Order_Page_label_table_num.setText(text)
                Current_time = datetime.datetime.now().strftime("%H:%M:%S")
                Current_Date = str(datetime.date.today())
                table_name = str(self.ui.Login_Page_text_username.text())

                sql_select_Query = """INSERT INTO receipt ( user_id, no_of_ppl, receipt_date, in_time, order_type,responsible)
                 VALUES ('""" + str(table_name) + """', '""" + str(s) + """', '""" + str(
                    Current_Date) + """', '""" + str(Current_time) + """', '0','A');
                """
                cursor = hackust_db.cursor()
                cursor.execute(sql_select_Query)
                hackust_db.commit()
                sql_select_Query = """Select receipt_id from receipt where receipt_date='""" + str(
                    Current_Date) + """' and in_time='""" + str(Current_time) + """' and user_id='""" + str(
                    table_name) + """' and no_of_ppl='""" + str(s) + """' and responsible='A';
                                """
                cursor = hackust_db.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                self.receipt_id = records[0][0]
                self.ui.Number_Of_People_Input_Page_label_invaild_input.setStyleSheet(
                    "font:16px;color: rgb(255, 0, 0,0);")


        except ValueError:
            self.ui.Number_Of_People_Input_Page_label_invaild_input.setStyleSheet("font:16px;color: rgb(255, 0, 0);")

    def Login(self):
        global role, hackust_db
        rolearray = ["table", "kitchen", "bar", "staff", "admin"]
        self.setup = True
        name = self.ui.Login_Page_text_username.text()

        password = self.ui.Login_Page_text_password.text()
        sql_select_Query = """select user_role from user where user_id = '""" + str(
            name) + """' and user_pw = '""" + str(password) + """';"""
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

        if (len(records) != 0):
            role = rolearray[int(records[0][0])]
            if (role == "table"):
                self.ui.stackedWidget.setCurrentWidget(self.ui.Number_Of_People_Input_Page)
                text = "Table " + str(name[-1])
                self.ui.Number_Of_People_Input_Page_label_table_number.setText(text)

            elif (role == "kitchen"):
                self.ui.stackedWidget.setCurrentWidget(self.ui.Kitchen_Bar_Page)
                self.SetUpKitchen_Bar()
            elif (role == "bar"):
                self.ui.stackedWidget.setCurrentWidget(self.ui.Kitchen_Bar_Page)
                self.ui.Kitchen_Bar_Page_label_name.setText("Bar")
                self.SetUpKitchen_Bar()
            elif (role == "staff"):
                self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)
                self.Waiter()
                self.SetUpWaiterOrderPage()
            elif (role == "admin"):
                self.ui.stackedWidget.setCurrentWidget(self.ui.Statistics_Page)
                self.Statistics()
                self.Chart()
                self.create_bar()
        else:
            self.ui.Login_Page_label_login_fail.setStyleSheet("font:16px;color: rgb(255, 0, 0);")

    def Table1(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Waiter_Page_btn_check_table_1.text()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Table2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()

        x = 0
        name = self.ui.Waiter_Page_btn_check_table_2.text()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Table3(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Waiter_Page_btn_check_table_3.text()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Table4(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Waiter_Page_btn_check_table_4.text()
        a = "$" + str(0) + "." + str(0) + str(0)
        if (self.ui.Cashier_Page_label_total_price.text() == a):
            self.Cashiers()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Table5(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Waiter_Page_btn_check_table_5.text()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Table6(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Waiter_Page_btn_check_table_6.text()

        for row in tablecashier:
            if (tablecashier[x][0] == name):
                c = tablecashier[x][2]
                break
            x = x + 1
        name = name + " (" + str(c) + " People)"
        self.ui.Cashier_Page_label_title.setText(name)
        self.Cashiers()

    def Statistics(self):
        sql_select_Query = """
        SELECT b.item_ename, SUM(a.order_qty) AS total
        FROM hackust_DB.customer_order AS a
        INNER JOIN item_name AS b ON a.item_id = b.item_id
        GROUP BY b.item_id
        ORDER BY total DESC
        LIMIT 5; 



                      """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        statistics = cursor.fetchall()

        for row in statistics:
            self.ui.Statistics_Page_label_best_dish_1.setText(statistics[0][0])
            self.ui.Statistics_Page_label_best_dish_2.setText(statistics[1][0])
            self.ui.Statistics_Page_label_best_dish_3.setText(statistics[2][0])
            self.ui.Statistics_Page_label_best_dish_4.setText(statistics[3][0])
            self.ui.Statistics_Page_label_best_dish_5.setText(statistics[4][0])

        sql_select_Query = """
        SELECT AVG(TIMESTAMPDIFF(MINUTE, in_time, out_time))
        FROM hackust_DB.receipt
        WHERE order_type = 0 AND out_time IS NOT NULL;



                      """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        statistics = cursor.fetchall()
        self.ui.Statistics_Page_label_content_1.setText(str(statistics[0][0]))

    def Waiter(self):
        self.waiter_payment = False
        if (self.ui.stackedWidget.currentWidget() == self.ui.Waiter_Page):
            timer = QTimer()
            timer.timeout.connect(self.Waiter)
            timer.start(10000)


        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;

         """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tables = cursor.fetchall()
        x = 0
        for row in tables:
            x = x + 1
        if (x == 0):
            self.ui.Waiter_Page_btn_check_table_1.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_1.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_2.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_2.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_3.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_3.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_4.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_4.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_5.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_5.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)
        elif (x == 1):
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_2.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_2.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_3.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_3.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_4.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_4.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_5.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_5.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)


        elif (x == 2):
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[1][0]))
            self.ui.Waiter_Page_btn_check_table_3.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_3.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_4.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_4.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_5.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_5.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)

        elif (x == 3):
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_2.setText(str(tables[1][0]))
            self.ui.Waiter_Page_btn_check_table_3.setText(str(tables[2][0]))
            self.ui.Waiter_Page_btn_check_table_4.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_4.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_5.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_5.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)

        elif (x == 4):
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_2.setText(str(tables[1][0]))
            self.ui.Waiter_Page_btn_check_table_3.setText(str(tables[2][0]))
            self.ui.Waiter_Page_btn_check_table_4.setText(str(tables[3][0]))
            self.ui.Waiter_Page_btn_check_table_5.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_5.setEnabled(0)
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)

        elif (x == 5):
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_2.setText(str(tables[1][0]))
            self.ui.Waiter_Page_btn_check_table_3.setText(str(tables[2][0]))
            self.ui.Waiter_Page_btn_check_table_4.setText(str(tables[3][0]))
            self.ui.Waiter_Page_btn_check_table_5.setText(str(tables[4][0]))
            self.ui.Waiter_Page_btn_check_table_6.setStyleSheet(
                "background-color: rgb(232, 151, 0),0;color: rgb(41, 14, 4),0;")
            self.ui.Waiter_Page_btn_check_table_6.setEnabled(0)

        else:
            self.ui.Waiter_Page_btn_check_table_1.setText(str(tables[0][0]))
            self.ui.Waiter_Page_btn_check_table_2.setText(str(tables[1][0]))
            self.ui.Waiter_Page_btn_check_table_3.setText(str(tables[2][0]))
            self.ui.Waiter_Page_btn_check_table_4.setText(str(tables[3][0]))
            self.ui.Waiter_Page_btn_check_table_5.setText(str(tables[4][0]))
            self.ui.Waiter_Page_btn_check_table_6.setText(str(tables[5][0]))

    def CashConfirm(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)

        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                               """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()

        x = 0
        name = self.ui.Cashier_Page_label_title.text()

        if(self.waiter_payment==True):
            self.waiter_payment=False
            c= self.receipt_id
        else:
            for row in tablecashier:
                temp = str(tablecashier[x][0]) + " (" + str(tablecashier[x][2]) + " People)"
                if (temp == name):
                    c = tablecashier[x][1]
                    break
                x = x + 1

            sql_select_Query = """UPDATE customer_order SET order_status = '4' WHERE (order_id = """ + str(c) + """); """
            cursor = hackust_db.cursor()
            cursor.execute(sql_select_Query)

        hackust_db.commit()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        sql_select_Query = """UPDATE
               receipt
               SET
               out_time = '"""+str(Current_time)+"""', checking_status = '0'
               WHERE receipt_id='""" + str(c) + """'; """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)

        hackust_db.commit()

    def colorchange_7days(self):
        self.ui.Statistics_Page_btn_7_days.setStyleSheet("""

        QPushButton
        {


        background-color: rgb(249, 234, 154);
        	color: rgb(41, 14, 4);
        border-radius:0;
        border:none;
        font:24px;
        font-weight:500;
        }
        QPushButton:hover
        {
        	background-color: rgb(249, 246, 194);
        	color: rgb(41, 14, 4);
        border-radius:0;
        border:none;
        font:24px;
        font-weight:500;
        }""")

        self.ui.Statistics_Page_btn_30_days.setStyleSheet("""

QPushButton
{
background-color: rgb(232, 151, 0);
color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}
QPushButton:hover
{
	background-color: rgb(240, 186, 88);
	color: rgb(41, 14, 4);
border-radius:0;
font:24px;
font-weight:500;
}

""")

        self.ui.Statistics_Page_btn_365_days.setStyleSheet("""

QPushButton
{
background-color: rgb(232, 151, 0);
color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}
QPushButton:hover
{
	background-color: rgb(240, 186, 88);
	color: rgb(41, 14, 4);
border-radius:0;
font:24px;
font-weight:500;
}

""")

    def colorchange_30days(self):
        self.ui.Statistics_Page_btn_7_days.setStyleSheet("""

        QPushButton
        {
        background-color: rgb(232, 151, 0);
        color: rgb(41, 14, 4);
        border-radius:0;
        border:none;
        font:24px;
        font-weight:500;
        }
        QPushButton:hover
        {
        	background-color: rgb(240, 186, 88);
        	color: rgb(41, 14, 4);
        border-radius:0;
        font:24px;
        font-weight:500;
        }

        """)

        self.ui.Statistics_Page_btn_30_days.setStyleSheet("""

                QPushButton
                {


                background-color: rgb(249, 234, 154);
                	color: rgb(41, 14, 4);
                border-radius:0;
                border:none;
                font:24px;
                font-weight:500;
                }
                QPushButton:hover
                {
                	background-color: rgb(249, 246, 194);
                	color: rgb(41, 14, 4);
                border-radius:0;
                border:none;
                font:24px;
                font-weight:500;
                }""")

        self.ui.Statistics_Page_btn_365_days.setStyleSheet("""

        QPushButton
        {
        background-color: rgb(232, 151, 0);
        color: rgb(41, 14, 4);
        border-radius:0;
        border:none;
        font:24px;
        font-weight:500;
        }
        QPushButton:hover
        {
        	background-color: rgb(240, 186, 88);
        	color: rgb(41, 14, 4);
        border-radius:0;
        font:24px;
        font-weight:500;
        }

        """)

    def colorchange_365days(self):
        self.ui.Statistics_Page_btn_7_days.setStyleSheet("""

QPushButton
{
background-color: rgb(232, 151, 0);
color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}
QPushButton:hover
{
	background-color: rgb(240, 186, 88);
	color: rgb(41, 14, 4);
border-radius:0;
font:24px;
font-weight:500;
}

""")

        self.ui.Statistics_Page_btn_30_days.setStyleSheet("""

QPushButton
{
background-color: rgb(232, 151, 0);
color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}
QPushButton:hover
{
	background-color: rgb(240, 186, 88);
	color: rgb(41, 14, 4);
border-radius:0;
font:24px;
font-weight:500;
}

""")

        self.ui.Statistics_Page_btn_365_days.setStyleSheet("""

QPushButton
{


background-color: rgb(249, 234, 154);
	color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}
QPushButton:hover
{
	background-color: rgb(249, 246, 194);
	color: rgb(41, 14, 4);
border-radius:0;
border:none;
font:24px;
font-weight:500;
}""")

    def CreditConfirm(self):
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 ORDER BY checking_time;
                                       """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Cashier_Page_label_title.text()
        if (self.waiter_payment == True):
            self.waiter_payment = False
            c = self.receipt_id
        else:
            for row in tablecashier:
                temp = str(tablecashier[x][0]) + " (" + str(tablecashier[x][2]) + " People)"
                if (temp == name):
                    c = tablecashier[x][1]
                    break
                x = x + 1
        sql_select_Query = """UPDATE customer_order SET order_status = '4' WHERE (order_id = """ + str(c) + """); """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        hackust_db.commit()
        creditconfirms = cursor.fetchall()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)
        Current_time = datetime.datetime.now().strftime("%H:%M:%S")
        sql_select_Query = """UPDATE
        receipt
        SET
        out_time = '"""+str(Current_time)+"""', checking_status = '0'
        WHERE receipt_id='""" + str(c) + """'; """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        hackust_db.commit()
        creditconfirms = cursor.fetchall()

    def TakeAway(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Order_Page)
        self.SetUpWaiterOrderPage()


    def Chart(self):
        sql_select_Query = """
        SELECT order_type, COUNT(*)* 100.0 / SUM(COUNT(*)) OVER(), COUNT(*)
        FROM hackust_DB.receipt
        GROUP BY order_type;




                      """

        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        statistics = cursor.fetchall()
        series = QPieSeries()
        series.append("Dine-in", statistics[0][2])
        series.append("Takeaway", statistics[1][2])
        series.append("3rd Party App", statistics[2][2])
        slice = QPieSlice()
        slice = series.slices()[2]
        slice.setPen(QPen(Qt.black, 0))
        slice.setBrush(QColor(231, 180, 90))
        slice = series.slices()[1]
        slice.setPen(QPen(Qt.black, 0))
        slice.setBrush(QColor(231, 163, 45))
        slice = series.slices()[0]
        slice.setPen(QPen(Qt.black, 0))
        slice.setBrush(QColor(231, 130, 0))
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setMinimumSize(280, 280)
        chart.legend().setVisible(True)
        chart.legend().setMinimumSize(80, 80)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))
        chart.legend().setAlignment(Qt.AlignLeft)
        chartview = QChartView(chart)
        chartview.setStyleSheet("background-color: rgb(244, 244, 244,0);")
        chartview.setRenderHint(QPainter.Antialiasing)
        self.ui.Statistics_Page_graphicsView_title_4.setGeometry(20, 10, 351, 231)
        self.ui.Statistics_Page_graphicsView_title_4.setStyleSheet("background-color: rgb(244, 244, 244,0);border:0;")
        self.ui.Statistics_Page_graphicsView_title_4.setViewport(chartview)

    def CashierBack(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Page)
        self.CashierReset()

    def CashBack(self):
        if(self.waiter_payment== True):
            self.waiter_payment = False
            self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Order_Page)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        self.CashReset()

    def CreditBack(self):
        if (self.waiter_payment == True):
            self.waiter_payment = False
            self.ui.stackedWidget.setCurrentWidget(self.ui.Waiter_Order_Page)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Cashier_Page)
        self.CreditCardReset()

    def Cashiers(self):
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1  AND checking_time IS NOT NULL ORDER BY checking_time;
                                               """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Cashier_Page_label_title.text()

        for row in tablecashier:
            temp = str(tablecashier[x][0]) + " (" + str(tablecashier[x][2]) + " People)"
            if (temp == name):
                c = tablecashier[x][1]
                break
            x = x + 1
        sql_select_Query = """SELECT a.item_ename, b.order_qty, c.menu_price, b.order_status
                     FROM item_name AS a 
                     INNER JOIN customer_order AS b ON a.item_id = b.item_id
                     INNER JOIN menu AS c ON b.item_id = c.menu_id
                     WHERE b.receipt_id = """ + str(c) + """;


                      """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        cashierrecipit = cursor.fetchall()

        x = 1
        y = 0
        z = 0
        for row in cashierrecipit:
            self.Cashier_Page_food_item = QHBoxLayout()
            self.Cashier_Page_food_item.setSizeConstraint(QLayout.SetMinimumSize)
            list_name = "Cashier_Page_food_item_" + str(x)
            self.Cashier_Page_food_item.setObjectName(str(list_name))
            cashier.append(self.Cashier_Page_food_item)

            self.Cashier_Page_food_name = QLabel(self.ui.Cashier_food_ordered_content)
            self.Cashier_Page_food_name.setMaximumSize(QSize(16777215, 45))
            self.Cashier_Page_food_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cashier_Page_food_name_" + str(x)
            self.Cashier_Page_food_name.setObjectName(str(list_name))
            self.Cashier_Page_food_name.setText(str(cashierrecipit[y][0]))
            self.Cashier_Page_food_item.addWidget(self.Cashier_Page_food_name)
            cashier.append(self.Cashier_Page_food_name)

            self.Cashier_Page_food_quantity = QLabel(self.ui.Cashier_food_ordered_content)
            self.Cashier_Page_food_quantity.setMaximumSize(QSize(16777215, 45))
            self.Cashier_Page_food_quantity.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cashier_Page_food_quantity_" + str(x)
            self.Cashier_Page_food_quantity.setObjectName(str(list_name))
            self.Cashier_Page_food_quantity.setText("x" + str(cashierrecipit[y][1]))
            self.Cashier_Page_food_item.addWidget(self.Cashier_Page_food_quantity)
            cashier.append(self.Cashier_Page_food_quantity)

            self.Cashier_Page_food_price = QLabel(self.ui.Cashier_food_ordered_content)
            self.Cashier_Page_food_price.setMaximumSize(QSize(16777215, 45))
            self.Cashier_Page_food_price.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cashier_Page_food_food_price_" + str(x)
            self.Cashier_Page_food_price.setObjectName(str(list_name))
            self.Cashier_Page_food_price.setText("$" + str(cashierrecipit[y][2] * cashierrecipit[y][1]))
            self.Cashier_Page_food_item.addWidget(self.Cashier_Page_food_price)
            cashier.append(self.Cashier_Page_food_price)
            z = z + cashierrecipit[y][1] * cashierrecipit[y][2]
            x = x + 1
            y = y + 1
            self.ui.Cashier_Page_verticalLayout.addLayout(self.Cashier_Page_food_item)

        self.ui.Cashier_Page_label_total_price.setText("$" + str(z))

    def Cash(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Cash_Payment_Page)
        self.q = 100

        self.ui.stackedWidget.setCurrentWidget(self.ui.Cash_Payment_Page)
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 AND checking_time IS NOT NULL ORDER BY checking_time;
                                                          """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Cashier_Page_label_title.text()
        if (self.waiter_payment == True):
            c = self.receipt_id
        else:
            for row in tablecashier:
                temp = str(tablecashier[x][0]) + " (" + str(tablecashier[x][2]) + " People)"
                if (temp == name):
                    c = tablecashier[x][1]
                    break
                x = x + 1

        self.ui.Cash_Payment_Page_label_title.setText(self.ui.Cashier_Page_label_title.text())
        sql_select_Query = """SELECT a.item_ename, b.order_qty, c.menu_price, b.order_status
                   FROM item_name AS a 
                   INNER JOIN customer_order AS b ON a.item_id = b.item_id
                   INNER JOIN menu AS c ON b.item_id = c.menu_id
                   WHERE b.receipt_id = """ + str(c) + """;
                    """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        cashrecipit = cursor.fetchall()
        x = 1
        y = 0
        self.z = float(0)
        for row in cashrecipit:
            self.Cash_Payment_Page_food_item = QHBoxLayout()
            self.Cash_Payment_Page_food_item.setSizeConstraint(QLayout.SetMinimumSize)
            list_name = "Cash_Payment_Page_food_item_" + str(x)
            self.Cash_Payment_Page_food_item.setObjectName(str(list_name))
            cash.append(self.Cash_Payment_Page_food_item)

            self.Cash_Payment_Page_food_name = QLabel(self.ui.Cash_Payment_Page_food_ordered_content)
            self.Cash_Payment_Page_food_name.setMaximumSize(QSize(16777215, 45))
            self.Cash_Payment_Page_food_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cash_Payment_Page_food_name_" + str(x)
            self.Cash_Payment_Page_food_name.setObjectName(str(list_name))
            self.Cash_Payment_Page_food_name.setText(str(cashrecipit[y][0]))
            self.Cash_Payment_Page_food_item.addWidget(self.Cash_Payment_Page_food_name)
            cash.append(self.Cash_Payment_Page_food_name)

            self.Cash_Payment_Page_food_quantity = QLabel(self.ui.Cash_Payment_Page_food_ordered_content)
            self.Cash_Payment_Page_food_quantity.setMaximumSize(QSize(16777215, 45))
            self.Cash_Payment_Page_food_quantity.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cash_Payment_Page_food_quantity_" + str(x)
            self.Cash_Payment_Page_food_quantity.setObjectName(str(list_name))
            self.Cash_Payment_Page_food_quantity.setText("x" + str(cashrecipit[y][1]))
            self.Cash_Payment_Page_food_item.addWidget(self.Cash_Payment_Page_food_quantity)
            cash.append(self.Cash_Payment_Page_food_quantity)

            self.Cash_Payment_Page_food_price = QLabel(self.ui.Cash_Payment_Page_food_ordered_content)
            self.Cash_Payment_Page_food_price.setMaximumSize(QSize(16777215, 45))
            self.Cash_Payment_Page_food_price.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Cash_Payment_Page_food_price_" + str(x)
            self.Cash_Payment_Page_food_price.setObjectName(str(list_name))
            self.Cash_Payment_Page_food_price.setText("$" + str(cashrecipit[y][2] * cashrecipit[y][1]))
            self.Cash_Payment_Page_food_item.addWidget(self.Cash_Payment_Page_food_price)
            cash.append(self.Cash_Payment_Page_food_price)
            self.z = self.z + float(cashrecipit[y][1]) * float(cashrecipit[y][2])
            x = x + 1
            y = y + 1
            self.ui.Cash_Payment_Page_verticalLayout.addLayout(self.Cash_Payment_Page_food_item)
        self.ui.Cash_Payment_Page_label_total_price.setText("$" + str(self.z))
        self.ui.Cash_Payment_Page_input_paid.setText(str(self.q))
        self.ui.Cash_Payment_Page_label_change_price.setText("$" + str(self.q - self.z))

    def CreditCard(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Credit_Card_Payment_Page)

        self.ui.Credit_Card_Payment_Page_label_title.setText(self.ui.Cashier_Page_label_title.text())
        sql_select_Query = """SELECT user_id,receipt_id,no_of_ppl FROM receipt WHERE checking_status = 1 AND checking_time IS NOT NULL ORDER BY checking_time;
                                                                           """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        tablecashier = cursor.fetchall()
        x = 0
        name = self.ui.Cashier_Page_label_title.text()
        if (self.waiter_payment == True):
            c = self.receipt_id
        else:
            for row in tablecashier:
                temp = str(tablecashier[x][0]) + " (" + str(tablecashier[x][2]) + " People)"
                if (temp == name):
                    c = tablecashier[x][1]
                    break
                x = x + 1
        self.ui.Cash_Payment_Page_label_title.setText(self.ui.Cashier_Page_label_title.text())
        sql_select_Query = """SELECT a.item_ename, b.order_qty, c.menu_price, b.order_status
                                    FROM item_name AS a 
                                    INNER JOIN customer_order AS b ON a.item_id = b.item_id
                                    INNER JOIN menu AS c ON b.item_id = c.menu_id
                                    WHERE b.receipt_id = """ + str(c) + """;
                                     """
        cursor = hackust_db.cursor()
        cursor.execute(sql_select_Query)
        creditrecipit = cursor.fetchall()
        x = 1
        y = 0
        z = 0
        for row in creditrecipit:
            self.Credit_Card_Payment_Page_food_item = QHBoxLayout()
            self.Credit_Card_Payment_Page_food_item.setSizeConstraint(QLayout.SetMinimumSize)
            list_name = "Credit_Card_Payment_Page_food_item_" + str(x)
            self.Credit_Card_Payment_Page_food_item.setObjectName(str(list_name))
            creditcard.append(self.Credit_Card_Payment_Page_food_item)

            self.Credit_Card_Payment_Page_food_name = QLabel(self.ui.Credit_Card_Payment_Page_food_ordered_context)
            self.Credit_Card_Payment_Page_food_name.setMaximumSize(QSize(16777215, 45))
            self.Credit_Card_Payment_Page_food_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Credit_Card_Payment_Page_food_name_" + str(x)
            self.Credit_Card_Payment_Page_food_name.setObjectName(str(list_name))
            self.Credit_Card_Payment_Page_food_name.setText(str(creditrecipit[y][0]))
            self.Credit_Card_Payment_Page_food_item.addWidget(self.Credit_Card_Payment_Page_food_name)
            creditcard.append(self.Credit_Card_Payment_Page_food_name)

            self.Credit_Card_Payment_Page_food_quantity = QLabel(
                self.ui.Credit_Card_Payment_Page_food_ordered_context)
            self.Credit_Card_Payment_Page_food_quantity.setMaximumSize(QSize(16777215, 45))
            self.Credit_Card_Payment_Page_food_quantity.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Credit_Card_Payment_Page_food_quantity_" + str(x)
            self.Credit_Card_Payment_Page_food_quantity.setObjectName(str(list_name))
            self.Credit_Card_Payment_Page_food_quantity.setText("x" + str(creditrecipit[y][1]))
            self.Credit_Card_Payment_Page_food_item.addWidget(self.Credit_Card_Payment_Page_food_quantity)
            creditcard.append(self.Credit_Card_Payment_Page_food_quantity)

            self.Credit_Card_Payment_Page_food_price = QLabel(self.ui.Credit_Card_Payment_Page_food_ordered_context)
            self.Credit_Card_Payment_Page_food_price.setMaximumSize(QSize(16777215, 45))
            self.Credit_Card_Payment_Page_food_price.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            list_name = "Credit_Card_Payment_Page_food_price_" + str(x)
            self.Credit_Card_Payment_Page_food_price.setObjectName(str(list_name))
            self.Credit_Card_Payment_Page_food_price.setText("$" + str(creditrecipit[y][2] * creditrecipit[y][1]))
            self.Credit_Card_Payment_Page_food_item.addWidget(self.Credit_Card_Payment_Page_food_price)
            creditcard.append(self.Credit_Card_Payment_Page_food_price)
            z = z + creditrecipit[y][1] * creditrecipit[y][2]
            x = x + 1
            y = y + 1

            self.ui.Credit_Card_Payment_Page_verticalLayout.addLayout(self.Credit_Card_Payment_Page_food_item)

        self.ui.Credit_Card_Payment_Page_label_total_price.setText("$" + str(z))

    def create_bar(self):
        # The QBarSet class represents a set of bars in the bar chart.
        # It groups several bars into a bar set

        set0 = QBarSet("9")
        set1 = QBarSet("12")
        set2 = QBarSet("15")
        set3 = QBarSet("18")
        set4 = QBarSet("21")

        set0 << 1 << 2 << 3 << 1 << 3 << 6 << 8
        set1 << 8 << 10 << 12 << 9 << 13 << 15
        set2 << 3 << 5 << 8 << 7 << 8 << 10 << 12
        set3 << 10 << 12 << 11 << 10 << 9 << 14 << 16
        set4 << 7 << 6 << 5 << 7 << 8 << 10 << 11

        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.setMinimumSize(320, 280)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))

        chartView = QChartView(chart)
        chartView.setStyleSheet("background-color: rgb(244, 244, 244,0);")
        chartView.setRenderHint(QPainter.Antialiasing)
        self.ui.Statistics_Page_graphicsView_title_3.setGeometry(20, 10, 351, 231)
        self.ui.Statistics_Page_graphicsView_title_3.setStyleSheet("background-color: rgb(244, 244, 244,0);border:0;")
        self.ui.Statistics_Page_graphicsView_title_3.setViewport(chartView)

    def CashierReset(self):
        global cashier

        for row in cashier:
            row.deleteLater()

        cashier = []

    def CreditCardReset(self):
        global creditcard

        for row in creditcard:
            row.deleteLater()
        creditcard = []

    def CashReset(self):
        global cash
        for row in cash:
            row.deleteLater()
        cash = []
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
