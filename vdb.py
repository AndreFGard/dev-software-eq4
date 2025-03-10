from pydantic import BaseModel
from datetime import date, datetime

class DB_Site(BaseModel):
    timestamp: date
    url: str
    content: str
    title: str
    id: int = 0


from sqlalchemy import create_engine, text
class VecDb:
    def __init__(self, TEMBO_PSQL_URL:str ):
        self.TEMBO_PSQL_URL = TEMBO_PSQL_URL
        self.url = self.TEMBO_PSQL_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
        self.engine = create_engine(self.url, echo=True)
    
    def _create_sites_table(self):
        q = """CREATE TABLE sites (timestamp date, url varchar(400), content text, title varchar(100), id serial primary key);"""
        print("create table not implemented")
    
    def _create_documents_table(self):
        q = """CREATE TABLE documents (content text, site_id int, id serial primary key,
                    CONSTRAINT fk_sites FOREIGN KEY (site_id) REFERENCES sites(id));"""
        print("create table not implemented")

    def insert_site(self, site: DB_Site):
        id = 0
        with self.engine.begin() as conn:
            result = conn.execute(
                text("""INSERT INTO sites (timestamp, url, content, title) 
                    VALUES(:timestamp, :url, :content, :title) 
                    RETURNING id"""),
                {
                    "timestamp": site.timestamp or datetime.now().date(),
                    "url": site.url,
                    "content": site.content,
                    "title": site.title
                }
            )
            id = result.first().id
        return id
    
