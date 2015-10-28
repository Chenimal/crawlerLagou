import sys
import sqlite3
import json


class model():

    def __init__(self):
        try:
            self.db = 'db_crawler'
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('[error]' + str(e))

    def create_table(self, t_name, file):
        try:
            self.cursor.execute('DROP TABLE IF EXISTS ' + t_name)
            with open(sys.path[0] + '/' + file, 'r') as f:
                q = f.read()
                self.cursor.execute(q)
        except Exception as e:
            print('[Error]: ' + str(e))
            return

    # show table contents
    def find(self, query):
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    # in case that we want to fetch many columns but don't want to type all,
    # so only exclude few
    def excludeFields(self, tableName, excludeFields=[]):
        # get fields names
        query = 'select COLUMN_NAME from information_schema.columns where table_name=\'%s\' ' % (
            tableName)
        if excludeFields:
            excludeFields = map(lambda s: '\'%s\'' % s, excludeFields)
            query = query + \
                ' and COLUMN_NAME not in (%s)' % (','.join(excludeFields))
        self.cursor.execute(query)
        fields = map(lambda s: s[0], self.cursor.fetchall())
        return fields

    # testA => test_a
    def camelToUnderline(self, string):
        result = ''
        for char in string:
            result += char if char.islower() else '_' + char.lower()
        return result

    # test_a => testA
    def underlineToCamel(self, string):
        result = ''
        for substr in string.split('_'):
            result += substr if result == '' else substr.capitalize()
        return result

    # import data into table from file
    def importFromFileToTable(self, filePath, tableName, excludeFields=[]):
        # generate query
        fields = self.excludeFields(tableName, excludeFields)
        fields_str = ','.join(fields)
        s = ['%s' for i in range(0, len(fields))]
        query = "insert into " + tableName + \
                "(" + fields_str + ") values(" + ','.join(s) + ")"
        # corresponding fields
        fields = map(self.underlineToCamel, fields)
        # read file and start inserting
        f = open(filePath, 'r')
        i = 0
        val = []
        for line in f:
            if i % 1000 == 0:
                print('%d item added' % i)
            line = json.loads(line)
            for item in fields:
                val.append(line[item])
            self.cursor.execute(query, val)
            val = []
            i = i + 1
        print("Import %d records" % (i))
        f.close()

m = model()
m.importFromFileToTable(
    filePath='data/position_lagou.txt',
    tableName='lagou_basic',
    excludeFields=['id', 'company_label_list', 'log_time'])
