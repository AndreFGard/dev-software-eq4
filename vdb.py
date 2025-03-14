from pydantic import BaseModel
from datetime import date, datetime
import asyncio as aio 
from itertools import chain
from schemas import *

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
class VecDb:
    def __init__(self, TEMBO_PSQL_URL:str ):
        self.TEMBO_PSQL_URL = TEMBO_PSQL_URL
        self.url = self.TEMBO_PSQL_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = create_async_engine(self.url, echo=True)
    
    def _create_sites_table(self):
        q = """CREATE TABLE sites (timestamp date, url varchar(400), content text, title varchar(255), id serial primary key);"""
        print("create table not implemented")
    
    def _create_documents_table(self):
        q = """CREATE TABLE documents (content text, site_id int, id serial primary key,
                    last_updated_at TIMESTAMP WITHOUT TIME ZONE,
                    CONSTRAINT fk_sites FOREIGN KEY (site_id) REFERENCES sites(id));"""
        print("create table not implemented")

    async def insert_sites_n_chunks(self, sites: list[DB_Site]):
        """returns site id"""
        id = 0
        dumped = [site.model_dump() for site in sites]
        #todo use ORM to be able to batch insert

        async with self.engine.begin() as conn:
            ids = []
            for obj in dumped:
                result = await conn.execute(
                    text("""INSERT INTO sites (timestamp, url, content, title) 
                        VALUES(NOW(), :url, :content, :title) 
                        RETURNING id"""), obj
                )
                ids.append(result.first().id)

            docs = [[DB_Document(content=chunk, site_id=id).model_dump() for chunk in site.chunks] for id,site in zip(ids, sites)]
            flatdocs = []
            for l in docs: flatdocs += l

            doc_result = await conn.execute(text("""INSERT INTO documents (content, last_updated_at, site_id) VALUES(:content, NOW(), :site_id)
                        """), flatdocs)
            

        return id
    
    async def retrieve_no_search(self,query:str):
        async with self.engine.begin() as conn:
            result = await conn.execute(text("""select * from vectorize.search(
                                       job_name=>'docs_search',
                                        query => :query, 
                                       return_columns => ARRAY['id','content'], num_results=>:num_results);
             """), {"query":query, "num_results": 5})
            
            chunks = [r[0]['content'] for r in result.fetchall()]
            return chunks
    