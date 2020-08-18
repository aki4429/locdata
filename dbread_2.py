#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///locdata.sqlite')

Base = declarative_base()

class Locdata(Base):
    __tablename__ = 'locdata'

    id = Column(Integer, primary_key=True)
    banch = Column(String(10))
    code = Column(String(50))
    qty = Column(Integer)  # 数量

    def __repr__(self):
        return "[id:'%s' banch:'%s' code:'%s' qty:'%s']" % (self.id, self.banch, self.code, self.qty)

Base.metadata.create_all(engine)

# SQLAlchemy はセッションを介してクエリを実行する
Session = sessionmaker(bind=engine)
session = Session()

cd = input("検索コードを入力してください。:(q=終了)")
print(cd)
while(cd != 'q'):
    for res in session.query(Locdata).filter(Locdata.code.like('%{0}%'.format(cd))).all():
        print(res)

    cd = input("検索コードを入力してください。:(q=終了)")

session.close()
