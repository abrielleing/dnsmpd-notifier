import pytest
from sqlalchemy import create_engine
from repository.dnsmpd_sqlalchemy import DNSMPDSQLAlchemy

database_url = 'sqlite:///:memory:'
engine = create_engine(
        database_url,
        pool_recycle=590, # for MariaDB use maximum value of 590
        pool_size=10,
) if database_url.startswith('mysql') else create_engine(database_url)
dnsmpd = DNSMPDSQLAlchemy(engine=engine)

@pytest.fixture
def setup_db():
    dnsmpd.create(
            name='John Smith',
            email='john@test.com',
            request_date='1600873302')
    dnsmpd.create(
            name='Jane Doe',
            email='jane@test.com',
            request_date='1600874142')
    yield
    dnsmpd.delete_all()

def test_read_first(setup_db):
    dnsmpd_first = dnsmpd.read_first()

    assert 'John Smith' == dnsmpd_first.name

def test_read_last_id(setup_db):
    dnsmpd_last = dnsmpd.read_last_id()

    assert 'Jane Doe' == dnsmpd_last.name

def test_read_list(setup_db):
    dnsmpd_list = dnsmpd.read_list()

    assert 2 == len(dnsmpd_list)
    dnsmpd_first = dnsmpd_list[0]
    assert 'John Smith'  == dnsmpd_first.name
    dnsmpd_last = dnsmpd_list[-1]
    assert 'Jane Doe' == dnsmpd_last.name

def test_read_after(setup_db):
    dnsmpd_list = dnsmpd.read_after(1600873305)

    assert 1 == len(dnsmpd_list)
    dnsmpd_person = dnsmpd_list[0]
    assert 'Jane Doe' == dnsmpd_person.name

def test_read_after_id(setup_db):
    dnsmpd_list = dnsmpd.read_after_id(1)

    assert 1 == len(dnsmpd_list)
    dnsmpd_person = dnsmpd_list[0]
    assert 'Jane Doe'  == dnsmpd_person.name
