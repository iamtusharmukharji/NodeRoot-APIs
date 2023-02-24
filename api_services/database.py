from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

conn_engine = create_engine("sqlite:///noderoot.db", echo=True)

@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


Session = sessionmaker(bind=conn_engine, autoflush=True)
