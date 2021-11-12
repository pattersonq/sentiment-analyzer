import psycopg2
import coinmarketcapapi
from config import Config, Psql_cred

class Db_manager():

    def __init__(self) -> None:  
        conn = None
        curr = None
        db_name= Psql_cred.db_name
        user= Psql_cred.user
        password= Psql_cred.password
        host= Psql_cred.host
        port= Psql_cred.port
        #connect database
        try:
            self.conn = psycopg2.connect("dbname={db_name} user={user} password={password} host={host} port={port}".format(db_name=db_name, user=user, password=password, host=host, port=port))
            self.cur = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error_db:
                print(error_db)
    def is_empty(self):
        self.cur.execute(
            SQL("SELECT * FROM coins")
        )
        foo =  self.cur.fetchone()
        return not foo
        
    def disconnect_db(self):
        try:
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error_db:
                print(error_db)
        finally:
                if self.conn is not None:
                    self.conn.close()


    def populate_db(self):
        cmc = coinmarketcapapi.CoinMarketCapAPI(Config.cmc_token)
        info = cmc.info()
        names = info.slug
        symbols = info.symbols
        columns = ['coin_name', 'symbol']
        values = [names, symbols]
        #Populate database
        for column, value in [columns, values]:
            self.cur.execute(
                SQL("INSERT INTO coins ({coin_name}) VALUES {values};").format(coin_name = column, values = value)
                )
        self.is_populated = True
    
    def select_db(self):
        '''returns names and symbols as list'''
        self.cur.execute(
            SQL("SELECT name FROM coins")
        )
        names = self.cur.fetchall().split(",")
        self.cur.execute(
            SQL("SELECT symbol FROM coins")
        )
        symbols = self.cur.fetchall().split(",")

        return names, symbols
        
        