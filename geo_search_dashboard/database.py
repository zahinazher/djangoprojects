import sqlite3
from sqlite3 import Error
from datetime import datetime
from time import strftime

class database:
    db_file = r"C:\Users\cunni\click_ads_dashboard\click_ad_dashboard\db.sqlite3"
    db_name = 'clickbot'

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def create_database(self):
        query = """
                CREATE TABLE IF NOT EXISTS clickbot (
                id integer PRIMARY KEY,
                geo_location text NOT NULL,
                niche text NOT NULL,
                instance_id text,
                date_time text,
                keyword text NOT NULL,
                volume float,
                domain text,
                proxy_ip text,
                estimated_cost text,
                kw_difficulty text,
                cpc float,
                comp_density text,
                number_of_results float,
                intent float,
                serp_features float,
                trend float
            );
        """
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def add_column(self, domain, type):
        query = "ALTER TABLE %s ADD COLUMN %s %s;" %(self.db_name, domain, type)
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def delete_column(self, domain):
        query = "ALTER TABLE %s DROP COLUMN %s;" %(self.db_name, domain)
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def select_data(self):
        query = "SELECT * FROM %s;" % self.db_name
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            print([description[0] for description in cursor.description])
            for row in cursor.fetchall():
                print ("Output Row:",row)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_row(self, geo, niche, inst_id, kw, volume, kw_difficulty, cpc, comp_density, no_of_results, intent, serp, trend, domain):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "insert into %s (geo_location, niche, keyword, cpc, volume, instance_id, date_time, proxy_ip," \
                " estimated_cost, kw_difficulty, comp_density, number_of_results, intent, serp_features, trend, domain)" \
                " values ('Denmark', 'Auto', 'Volvo', '3.11', '21000', '1555515', '%s', '1.1.1.1', '$3100'," \
                "'4.2', '8.4', '96', '1.4', '3.2', '1.7', 'amazon.se' );" % (self.db_name, date)

        query = "insert into %s (geo_location, niche, instance_id, date_time, keyword, volume, kw_difficulty, cpc, comp_density," \
                "number_of_results, intent, serp_features, trend, domain) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                " '%s', '%s', '%s', '%s', '%s', '%s')" \
                % (self.db_name, geo, niche, inst_id, date, kw, volume, kw_difficulty, cpc, comp_density, no_of_results, intent, serp, trend, domain)
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.executescript(query)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    db = database()
    db.create_connection()
    # db. create_database(database)
    # db.insert_row()
    # db.delete_column('number')
    # db.add_column('number_of_results', 'text')
    db.select_data()