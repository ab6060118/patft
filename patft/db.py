import MySQLdb

class DB():
    db = None

    def __init__ (self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="user")
        cursor = self.db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS patft")
        cursor.execute("USE patft")

        cursor.execute("DROP TABLE IF EXISTS post")
        cursor.execute("CREATE TABLE IF NOT EXISTS post (United_States_Patent varchar(20), Date varchar(30), Current_US_Class varchar(255), Current_International_Class text)")

        cursor.execute("DROP TABLE IF EXISTS Related_US_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS Related_US_Patent_Documents (United_States_Patent varchar(20), Application_Number varchar(30), Filing_Date varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS US_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS US_Patent_Documents (United_States_Patent varchar(20), first varchar(30), second varchar(30), third varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS Foreign_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS Foreign_Patent_Documents (United_States_Patent varchar(20), first varchar(30), second varchar(30), third varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS Other_References")
        cursor.execute("CREATE TABLE IF NOT EXISTS Other_References (United_States_Patent varchar(20), data text)")

    def write (self, post):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO post (United_States_Patent, Date, Current_US_Class, Current_International_Class) VALUES ("' + post['United States Patent'] + '", "' + post['Date'] + '", "' + post['Current U.S. Class'] + '", "' + post['Current International Class'] + '")')
        self.db.commit()

        if post['Related U.S. Patent Documents']:
            data = ''
            for item in post['Related U.S. Patent Documents']:
                data = ''.join([data, '("' + post['United States Patent'] + '", "' + item['Application Number'] + '", "' + item['Filing Date'] + '")'])
            data = data.replace(')(', '), (')

            cursor.execute('INSERT INTO Related_US_Patent_Documents (United_States_Patent, Application_Number, Filing_Date) VALUES ' + data)
            self.db.commit()

        if post['References Cited'] != 'None':
            if post['References Cited']['U.S. Patent Documents']:
                data = ''
                for item in post['References Cited']['U.S. Patent Documents']:
                    data = ''.join([data, '("' + post['United States Patent'] + '", "' + item['first'] + '", "' + item['second'] + '", "' + item['third'] + '")'])
                data = data.replace(')(', '), (')

                cursor.execute('INSERT INTO US_Patent_Documents (United_States_Patent, first, second, third) VALUES ' + data)
                self.db.commit()

            if post['References Cited']['Foreign Patent Documents']:
                data = ''
                for item in post['References Cited']['Foreign Patent Documents']:
                    data = ''.join([data, '("' + post['United States Patent'] + '", "' + item['first'] + '", "' + item['second'] + '", "' + item['third'] + '")'])
                data = data.replace(')(', '), (')

                cursor.execute('INSERT INTO Foreign_Patent_Documents (United_States_Patent, first, second, third) VALUES ' + data)
                self.db.commit()

            if post['References Cited']['Other References']:
                data = ''
                for item in post['References Cited']['Other References']:
                    data = ''.join([data, '("' + post['United States Patent'] + '", "' + MySQLdb.escape_string(item) + '")'])
                data = data.replace(')(', '), (')

                cursor.execute('INSERT INTO Other_References (United_States_Patent, data) VALUES ' + data)
                self.db.commit()
