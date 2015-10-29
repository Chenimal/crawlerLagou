import sys
import sqlite3
import json
import lib.functions

class dbSqlite():

    def __init__(self):
        try:
            self.db = 'data/db_crawler'
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('[error]' + str(e))

    def createTable(self, t_name, file):
        try:
            self.cursor.execute('DROP TABLE IF EXISTS ' + t_name)
            with open(sys.path[0] + '/bin/' + file, 'r') as f:
                q = f.read()
                self.cursor.execute(q)
        except Exception as e:
            print('[Error]: ' + str(e))
            return

    # show table contents
    def findAll(self, query):
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    # get table fields by name
    def getTableFields(self, tableName):
        if tableName == 'lagou_basic':
            fields = [
                'order_by', 'leader_name', 'calc_score', 'company_size', 'count_adjusted', 'work_year', 'education',
                'finance_stage', 'city', 'create_time_sort', 'company_id', 'industry_field', 'create_time', 'score', 'ad_word',
                'salary', 'position_name', 'company_name', 'job_nature', 'position_types_map', 'total_count', 'position_first_type',
                'rel_score', 'position_id', 'random_score', 'company_short_name', 'search_score', 'have_deliver',
                'hr_score', 'position_type', 'position_advantage', 'adjust_score'
            ]
        return fields

    # generate insert query
    def insertQuery(self, tableName):
        f = self.getTableFields(tableName)
        s = ','.join(['?' for i in range(0, len(f))])
        f = ','.join(f)
        q = 'insert into %s(%s) values(%s)' % (tableName, f, s)
        return q

    def insertParam(self, tableName):
        f = self.getTableFields(tableName)
        f = list(map(lib.functions.underlineToCamel, f))
        return f

    # import data into table from file
    def importFromFileToTable(self, filePath, tableName, excludeFields=[]):
        # generate query
        fields = self.getTableFields(tableName)
        fields_str = ','.join(fields)
        s = ['?' for i in range(0, len(fields))]
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

'''m = dbSqlite()
print(m.getTableFields('lagou_basic'))
m.createTable('lagou_basic','database.sql')
m.importFromFileToTable(
    filePath='data/position_lagou.txt',
    tableName='lagou_basic',
    excludeFields=['id', 'company_label_list', 'log_time'])'''
