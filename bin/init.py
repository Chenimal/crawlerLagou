import sys
# in order to import module from parent directory
sys.path.append('..')
import model

m = model.dbSqlite()
m.createTable('lagou_basic','lagou_basic.sql')
m.createTable('lagou_company_label','lagou_company_label.sql')


'''
this method shouldn't be used anymore as it doesn't store data in txt file.
m.importFromFileToTable('lagou_basic','data/position_lagou.txt')
'''
