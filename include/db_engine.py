from include.config import db_user, db_password, db_host, db_port, db_name
from sqlalchemy import create_engine

postgresql_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"  # noqa: E501


def connect_to_database():
    engine = create_engine(postgresql_url)
    return engine


engine = connect_to_database()
