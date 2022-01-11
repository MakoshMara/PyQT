from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime

from common.variables import SERVER_DATABASE


class DataBase:
    class AllUsers:
        def __init__(self, name):
            self.name = name
            self.last_login = datetime.datetime.now()
            self.id = None

    class ActiveUsers:
        def __init__(self,user_id,ip_adr, port, login_time):
            self.user = user_id
            self.ip_adr = ip_adr
            self.port = port
            self.login_time = login_time
            self.id = None

    class History:
        def __init__(self,user_id,date,ip,port):
            self.user = user_id
            self.date_time = date
            self.ip = ip
            self.port = port
            self.id = None

    def __init__(self):
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        self.metadata = MetaData()
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime)
                            )
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_adr', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        self.metadata.create_all(self.database_engine)

        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.History, login_history)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

    def user_login(self, name, ip_adr, port):
        rezult = self.session.query(self.AllUsers).filter_by(name=name)
        if rezult.count():
            user = rezult.first()
            print(user.last_login)
            user.last_login = datetime.datetime.now()
        else:
            user = self.AllUsers(name)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_adr, port, datetime.datetime.now())
        self.session.add(new_active_user)
        history = self.History(user.id, datetime.datetime.now(), ip_adr, port)
        self.session.add(history)
        self.session.commit()

    def user_logout(self, name):

        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
        return query.all()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
        return query.all()

    def active_users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_adr,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(self.AllUsers.name,
                                   self.History.date_time,
                                   self.History.ip,
                                   self.History.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по этому имени
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

if __name__ == '__main__':
    test_db = DataBase()
    # Выполняем "подключение" пользователя
    test_db.user_login('client_1', '192.168.1.1', 5555)
    test_db.user_login('client_2', '192.168.1.2', 6666)

    # Выводим список кортежей - активных пользователей
    print(' ---- test_db.active_users_list() ----')
    print(test_db.active_users_list())

    # Выполняем "отключение" пользователя
    test_db.user_logout('client_1')
    # И выводим список активных пользователей
    print(' ---- test_db.active_users_list() after logout client_1 ----')
    print(test_db.active_users_list())

    # Запрашиваем историю входов по пользователю
    print(' ---- test_db.login_history(client_1) ----')
    print(test_db.login_history('client_1'))

    # и выводим список известных пользователей
    print(' ---- test_db.users_list() ----')
    print(test_db.users_list())