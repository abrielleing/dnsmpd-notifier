import os
import logging
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, Text, MetaData, ForeignKey
from sqlalchemy.sql import select, and_, text
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

class DNSMPDSQLAlchemy():

    def __init__(self, engine=None, autoload=False, tablename='dnsmpd'):
        if engine is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
            engine = create_engine(
                    database_url,
                    pool_recycle=590, # for MariaDB use maximum value of 590
                    pool_size=10,
            ) if database_url.startswith('mysql') else create_engine(database_url)
        metadata = MetaData()
        if autoload:
            metadata.bind = engine
            table = Table(tablename, metadata, autoload=True, autoload_with=engine)
        else:
            table = Table(tablename, metadata,
                Column('ID', Integer, primary_key=True),
                Column('name', String(255), nullable=False),
                Column('email', String(255), nullable=False),
                Column('request_date', Integer, nullable=False)
            )
            metadata.create_all(engine)
        self._engine = engine
        self._table = table
        self._transaction = None

    def __enter__(self):
        self.transaction_begin()
        return self

    def __exit__(self, *args):
        self.transaction_rollback()

    def connect(self):
        self._conn = self._engine.connect()

    def close(self):
        self._transaction = None
        self._conn.close()

    def transaction_begin(self):
        self.connect()
        self._transaction = self._conn.begin()

    def transaction_commit(self):
        if self._transaction: self._transaction.commit()
        self._transaction = None

    def transaction_rollback(self):
        if self._transaction: self._transaction.rollback()
        self._transaction = None

    def create(self, **kw):                                        
        table = self._table                                        
        dnsmpd_id = None                                           
        if self._transaction is None: self.connect()               
        try:                                                       
            stmt = table.insert().values(**kw)                     
            r = self._conn.execute(stmt)                           
            dnsmpd_id = r.lastrowid                                
        except:                                                    
            logging.exception('Exception in create_dnsmpd')        
        finally:                                                   
            if self._transaction is None: self.close()             
        return dnsmpd_id

    def read_first(self, **kw):
        table = self._table
        dnsmpd = None
        if self._transaction is None: self.connect()
        try:
            stmt = table.select()
            stmt = stmt if kw.get('ID') is None else stmt.where(table.c.ID==kw.get('ID'))
            stmt = stmt if kw.get('name') is None else stmt.where(table.c.name==kw.get('name'))
            stmt = stmt if kw.get('email') is None else stmt.where(table.c.email==kw.get('email'))
            dnsmpd = self._conn.execute(stmt).fetchone()
        except:
            logging.exception('Exception in read_first')
        finally:
            if self._transaction is None: self.close()
        return dnsmpd

    def read_last_id(self):
        table = self._table
        dnsmpd_list = None
        if self._transaction is None: self.connect()
        try:
            stmt = table.select()
            stmt = stmt.order_by(table.c.ID.desc()).limit(1)
            dnsmpd_last = self._conn.execute(stmt).fetchone()
        except:
            logging.exception('Exception in read_last')
        finally:
            if self._transaction is None: self.close()
        return dnsmpd_last

    def read_list(self, **kw):
        table = self._table
        dnsmpd_list = None
        if self._transaction is None: self.connect()
        try:
            stmt = table.select()
            stmt = stmt if kw.get('ID') is None else stmt.where(table.c.ID==kw.get('ID'))
            stmt = stmt if kw.get('name') is None else stmt.where(table.c.name==kw.get('name'))
            stmt = stmt if kw.get('email') is None else stmt.where(table.c.email==kw.get('email'))
            dnsmpd_list = self._conn.execute(stmt).fetchall()
        except:
            logging.exception('Exception in read_list')
        finally:
            if self._transaction is None: self.close()
        return dnsmpd_list

    def read_after(self, timestamp_after):
        table = self._table
        dnsmpd_list = None
        if self._transaction is None: self.connect()
        try:
            stmt = table.select()
            stmt = stmt.where(table.c.request_date>timestamp_after)
            dnsmpd_list = self._conn.execute(stmt).fetchall()
        except:
            logging.exception('Exception in read_after')
        finally:
            if self._transaction is None: self.close()
        return dnsmpd_list

    def read_after_id(self, id_after):
        table = self._table
        dnsmpd_list = None
        if self._transaction is None: self.connect()
        try:
            stmt = table.select()
            stmt = stmt.where(table.c.ID>id_after)
            dnsmpd_list = self._conn.execute(stmt).fetchall()
        except:
            logging.exception('Exception in read_after')
        finally:
            if self._transaction is None: self.close()
        return dnsmpd_list

    def delete_all(self):
        ##-- Example of a transaction in context manager
        if str(self._engine.url) != 'sqlite:///:memory:':
            return
        is_deleted = False
        table = self._table
        try:
            with self._engine.begin() as conn:
                r = conn.execute(table.delete())
                is_deleted = r.rowcount > 0
        except:
            logging.exception('Exception in delete_all')
        return is_deleted
