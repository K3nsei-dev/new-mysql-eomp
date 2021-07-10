import unittest
import rsaidnumber
import mysql.connector as mysql


class CheckingId(unittest.TestCase):
    def test_rsa_id_number(self):
        id_num = rsaidnumber.parse("9804205251081")
        return id_num.valid


class DatabaseFunctions(unittest.TestCase):
    def test_insert_data(self):
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="@Lifechoices1234",
            database="lifechoicesonline"
        )
        name = "dummy"
        id_number = 9804205251081
        password = "dummypassword"
        cell_number = 631922598
        lc_unit = "academy"
        nok = "dummymom"
        nok_num = 604208810

        my_cursor = db.cursor()
        query = "INSERT INTO register (FullName, IDNumber, Password, CellNum, Unit) VALUES (%s, " \
                "%s, " \
                "%s, %s, %s) "
        values = (name, id_number, password, cell_number, lc_unit)
        my_cursor.execute(query, values)
        db.commit()

        reusable_id = my_cursor.lastrowid

        second_query = "INSERT INTO emergency (UserID, IDNum, NextOfKin, NextOfKinNum) VALUES (%s, " \
                       "%s, %s, %s) "
        second_values = (reusable_id, id_number, nok, nok_num)
        my_cursor.execute(second_query, second_values)
        db.commit()

    def test_update_data(self):
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="@Lifechoices1234",
            database="lifechoicesonline"
        )
        name = "dummy2"
        id_number = 1234567891234
        password = "dummypasswordnew"
        cell_number = 835851644
        lc_unit = "Business"
        nok = "dummymom"
        nok_num = 836967357

        my_cursor = db.cursor()
        query = "UPDATE register SET FullName = %s, IDNumber = %s, Password = %s, CellNum = %s, " \
                "Unit = %s WHERE IDNumber = %s "
        values = (
            name, id_number, password, cell_number, lc_unit, id_number)
        my_cursor.execute(query, values)
        db.commit()

        second_query = "UPDATE emergency SET IDNum = %s, NextOfKin = %s, NextOfKinNum = " \
                       "%s WHERE IDNum = %s "
        second_values = (id_number, nok, nok_num, id_number)
        my_cursor.execute(second_query, second_values)
        db.commit()

    def test_delete_data(self):
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="@Lifechoices1234",
            database="lifechoicesonline"
        )
        cursor = db.cursor()

        del_query = "DELETE FROM timesheet WHERE UserID = %s"
        del_query2 = "DELETE FROM emergency WHERE UserID = %s"
        del_query3 = "DELETE FROM register WHERE UserID = %s"
        sel_data = 35
        cursor.execute(del_query, (sel_data,))
        cursor.execute(del_query2, (sel_data,))
        cursor.execute(del_query3, (sel_data,))
        db.commit()
