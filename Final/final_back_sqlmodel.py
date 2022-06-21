from sqlalchemy import Column, String, Integer, create_engine, Date, DateTime, exc, text, desc, func, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义User对象:
class UserLogin(Base):
    __tablename__ = 'user_login'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    statue = Column(String(20))


class UserLive(Base):
    __tablename__ = 'live_user'
    user_name = Column(String(50))
    user_tele = Column(BigInteger, primary_key=True)
    user_time = Column(Date)
    user_measure = Column(Integer)
    user_build = Column(String(20))
    user_pwd = Column(String(150))
    user_statue = Column(Integer)


class ElectricityFees(Base):
    __tablename__ = 'electricity_fees'
    ef_id = Column(Integer, primary_key=True)
    ef_user_id = Column(Integer)
    ef_date = Column(String(20))
    ef_num = Column(Integer)
    ef_pay = Column(Integer)
    ef_hadpay = Column(Integer)
    ef_payday = Column(Date)


class WaterFees(Base):
    __tablename__ = 'water_fees'
    wa_id = Column(Integer, primary_key=True)
    wa_user_id = Column(Integer)
    wa_date = Column(String(20))
    wa_num = Column(Integer)
    wa_pay = Column(Integer)
    wa_hadpay = Column(Integer)
    wa_payday = Column(Date)


class PropertyFees(Base):
    __tablename__ = 'property_fees'
    pr_id = Column(Integer, primary_key=True)
    pr_user_id = Column(Integer)
    pr_date = Column(String(20))
    pr_pay = Column(Integer)
    pr_hadpay = Column(Integer)
    pr_payday = Column(Date)


class Parking(Base):
    __tablename__ = 'parking'
    pa_id = Column(Integer, primary_key=True)
    pa_fooler = Column(String(50))
    is_used = Column(Integer)


class ParkingFees(Base):
    __tablename__ = 'parking_fees'
    pf_id = Column(Integer, primary_key=True)
    pa_id = Column(Integer)
    pf_user_tele = Column(BigInteger)
    pf_user_carnum = Column(String(50))
    pf_starttime = Column(DateTime)
    pf_stoptime = Column(DateTime)
    pf_hour = Column(String(20))
    pf_money = Column(String(20))


class ChargingStandard(Base):
    __tablename__ = 'charging_standard'
    cs_id = Column(Integer, primary_key=True)
    cs_kind = Column(String(20))
    cs_standard = Column(Integer)


class Code(Base):
    __tablename__ = 'code'
    tele = Column(Integer, primary_key=True)
    code = Column(String(20))


# 初始化数据库连接:
HOST = '47.241.35.150'
PORT = '3306'
DATABASE = 'finalbase'
USERNAME = 'root'
PASSWORD = 'Kadfgo53254G'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD,
                                                                                        host=HOST,
                                                                                        port=PORT,
                                                                                        db=DATABASE)

engine = create_engine(DB_URI, echo=True)
# engine = create_engine('mysql+pymysql://root:123456@47.241.35.150:3306/finalbase?charset=utf8', echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)
session.commit()
