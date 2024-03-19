import sqlite3
import traceback

class SQLLiteToSchema:

    def __init__(self, db_path):
        # todo: allow users to pass their own conn anc cursor
        self.conn = None
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_schema(self, output_format='JSON'):
        database_schema = {}
        try:
            databases = self.list_databases()
            # sqlite single database
            database_schema['name'] = databases[0]['name']
            database_schema['file'] = databases[0]['file']
            database_schema['tables'] = []

            # List all tables
            tables = self.list_tables()

            for table in tables:

                table_info = {}
                table_coumns = self.table_schema(table[0])

                index_info_list = self.index_detail(table[0])

                foreign_keys = self.foreign_keys(table[0])

                table_info['name'] = table[0]
                table_info['columns'] = table_coumns
                table_info['foreign_keys'] = foreign_keys
                table_info['index'] = index_info_list


                database_schema['tables'].append(table_info)

        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            self.conn.close()

        return database_schema

    def list_databases(self):
        # This query shows all attached databases, including the main one
        self.cursor.execute("PRAGMA database_list;")
        databases = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        database_with_col_names = []
        for row in databases:
            row_with_col_names = {column_names[i]: value for i, value in enumerate(row)}
            database_with_col_names.append(row_with_col_names)
        return database_with_col_names

    def list_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return tables

    def index_detail(self, table_name):
        # This query lists all tables in the database
        self.cursor.execute(f"PRAGMA index_list({table_name});")
        indexes = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        indexes_with_col_names = []
        for index in indexes:
            index_with_col_names = {column_names[i]: value for i, value in enumerate(index)}
            indexes_with_col_names.append(index_with_col_names)

        index_info_list = []

        for index in indexes_with_col_names:
            # todo: might be error prone; might have to add explicit check for pk
            origin = 'CREATE INDEX' if index['origin'] == 'c' else 'UNIQUE' if index['origin'] == 'u' else 'PRIMARY KEY'
            index_detail = {
                "name": index['name'],
                "is_partial": True if index['partial'] == 1 else False,
                "is_unique": True if index['unique'] == 1 else False,
                "origin": origin
            }
            
            index_info = self.index_info(index['name'])
            index_columns = []
            for seq in index_info:
                index_column = {
                    'id': seq['cid'],
                    'name': seq['name']
                }
                index_columns.append(index_column)
            
            index_detail['columns'] = index_columns
            index_info_list.append(index_detail)

        return index_info_list

    def index_info(self, index_name):
        self.cursor.execute(f"PRAGMA index_info({index_name});")
        index_info = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        index_info_with_col_name = []
        for info in index_info:
            info_with_col_name = {column_names[i]: value for i, value in enumerate(info)}
            index_info_with_col_name.append(info_with_col_name)

        return index_info_with_col_name

    def foreign_keys(self, table_name):
        self.cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        foreign_keys_with_col_name = []
        for key in foreign_keys:
            fk_with_col_name =  {column_names[i]: value for i, value in enumerate(key)}
            foreign_keys_with_col_name.append(fk_with_col_name)

        return foreign_keys_with_col_name



    def table_schema(self, table_name):
        # This query retrieves the SQL CREATE statement for a given table
        query = f"PRAGMA table_info({table_name});"
        # print(query)
        self.cursor.execute(query)
        schema = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        column_info_list = []
        for column in schema:
            # print(column)
            column_with_name = {column_names[i]: value for i, value in enumerate(column)}

            is_primary_key = False if column_with_name['pk'] == 0 else True
            primary_key_sequence = column_with_name['pk'] if is_primary_key else None

            column_info = {
                "name": column_with_name['name'],
                "type": column_with_name['type'],
                "not_null": True if column_with_name['notnull'] == 1 else False,
                "is_primary_key": is_primary_key,
                "primary_key_sequence": primary_key_sequence,
                "default_value": column_with_name['dflt_value'] if column_with_name['dflt_value'] else None
            }

            column_info_list.append(column_info)

        return column_info_list


