# -*-coding:utf-8 -*-
# !/usr/bin/python
import happybase


class HbaseClient:
    config = {
        'BATCH_SIZE': 10
    }

    def __init__(self, host='localhost', tablename='qiushi'):
        self.conn = happybase.Connection(host)
        if tablename not in self.conn.tables():
            self.create_table(tablename)
        else:
            self.table = self.conn.table(tablename)

    def create_table(self, table):
        self.conn.create_table("%s" % table, {"page": dict()})
        self.table = self.conn.table(table)

    def list_tables(self):
        print self.conn.tables()

    def put(self, id, data_dict):
        self.table.put(id, data_dict)

    def get(self):  # 批量提取
        return self.table.scan(batch_size=self.config['BATCH_SIZE'])

    def get_a_record(self, id):
        row = self.table.row('%d' % id)
        # source = row['page:source']
        # url = row['page:url']
        # result = dict([(url, source)]) # 根据主键(RowKey)取列族(ColumnFamily)中列(Column)
        result = row  # 根据主键(RowKey)取整个列族(ColumnFamily)
        return result

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    a = HbaseClient()
    dicts = a.get_a_record(1)
    print dicts
    for k, v in dicts.items():
        if k == 'page:title':
            title = v

        if k == 'page:source':
            source = v
