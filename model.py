import sys
import sqlite3
import json
import lib.functions as func

class dbSqlite():

    def __init__(self):
        try:
            self.db = sys.path[0]+'/data/db_crawler'
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('[error]' + str(e))
            func.logger(self.__class__.__name__, str(e))

    def createTable(self, t_name, file):
        try:
            with open(sys.path[0] + '/bin/' + file, 'r') as f:
                q = f.read()
                self.cursor.execute(q)
        except Exception as e:
            print('[Error]: ' + str(e))
            func.logger(self.__class__.__name__, str(e))

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

    # return list of keys which will be inserted into db
    def insertParam(self, tableName):
        f = self.getTableFields(tableName)
        f = list(map(func.underlineToCamel, f))
        return f

    # import data into table from file
    def importFromFileToTable(self, tableName,filePath):
        insert_query = self.insertQuery(tableName)
        insert_param = self.insertParam(tableName)
        f = open(filePath, 'r')
        i = 0
        for line in f:
            if i % 1000 == 0:
                print('%d item added' % i)
            p = json.loads(line)
            r = self.findAll("select * from %s where position_id = '%s'" % (tableName, p['positionId']))
            if not r:
                p = list(map(lambda x: p.get(x),insert_param))
                self.cursor.execute(insert_query, p)
                self.conn.commit()
                i = i + 1
        print("Import %d records" % (i))
        f.close()

'''m = dbSqlite()
m.importFromFileToTable('data/position_lagou.txt','lagou_basic')'''
