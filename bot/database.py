from sqlalchemy import create_engine, Column, BigInteger, Integer, String
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('HOST')
database = os.getenv('DB_NAME')

ENGINE = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:\
5432/{database}')

Base = declarative_base()

class TeleusersAlanica(Base):
    __tablename__ = 'teleusers_alanica'
    id = Column(Integer, primary_key=True)
    teleid = Column(BigInteger, nullable=True, default=0)
    username = Column(String, nullable=True, default=0)
    f_name = Column(String, nullable=True, default=0)
    l_name = Column(String, nullable=True, default=0)
    status = Column(String, nullable=True, default=0)
    chat = Column(String, nullable=True, default=0)
    language = Column(String, nullable=True, default=0)
    topic = Column(String, nullable=True, default=0)
    question = Column(String, nullable=True, default=0)


    def __repr__(self) -> str:
        return self.teleid


if __name__ == '__main__':
    Base.metadata.create_all(ENGINE)
