from pydantic import BaseModel
from datetime import date, datetime
import asyncio as aio 
from itertools import chain
from schemas import *

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import TEXT, text
class VecDb:
    """This class provides a database interface for the vector database, which allows semantic search"""
    def __init__(self, TEMBO_PSQL_URL:str ):
        self.TEMBO_PSQL_URL = TEMBO_PSQL_URL
        self.url = self.TEMBO_PSQL_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = create_async_engine(self.url, echo=False)

    
    async def _create_tables(self):
        sitesq = """CREATE TABLE sites (timestamp date, url varchar(400), title varchar(255), id serial primary key);"""

        documentsq = """CREATE TABLE documents (
                id serial PRIMARY KEY,
                content text,
                site_id int,
                last_updated_at TIMESTAMP WITHOUT TIME ZONE,
                CONSTRAINT fk_sites FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE
            );
            SELECT vectorize.table(
            job_name    => 'docs_search',
            "table"    => 'documents',
            primary_key => 'id',
            columns     => ARRAY['id', 'content', 'site_id'],
            transformer => 'sentence-transformers/all-MiniLM-L6-v2',
            schedule    => 'realtime'
            );
        """
        async with self.engine.begin() as conn:
            try:
                await conn.execute(text(sitesq))
                await conn.execute(text(documentsq))
            except:
                ...
    
    
    async def insert_sites_n_chunks(self, sites: list[DB_Site]):
        """Inserts sites and their chunks into the vector database"""

        id = 0
        dumped = [site.model_dump() for site in sites]
        #todo use ORM to be able to batch insert
        import time
        start = time.time()

        

        async with self.engine.begin() as conn:
            ids = []
            for obj in dumped:
                obj.pop("content")
                result = await conn.execute(
                    text("""INSERT INTO sites (timestamp, url, title) 
                        VALUES(NOW(), :url, :title) 
                        RETURNING id"""), obj
                )
                ids.append(result.first().id) #type: ignore

            print(f"BENCH: site insertion: {time.time()-start:.3f}")
            start = time.time()

            docs = [[DB_Document(content=chunk + " ", site_id=id).model_dump() for chunk in site.chunks if len(chunk)] for id,site in zip(ids, sites)]
            flatdocs = []
            for l in docs: flatdocs += l

            doc_result = await conn.execute(text("""INSERT INTO documents (content, last_updated_at, site_id) VALUES(:content, NOW(), :site_id)
                        """), flatdocs)
            print(f"BENCH: doc insertion: {time.time()-start:.3f}")
            x = 4

        return id
    
    async def retrieve_no_search(self,query:str) -> list[str]:
        async with self.engine.begin() as conn:
            result = await conn.execute(text("""select * from vectorize.search(
                                       job_name=>'docs_search',
                                        query => :query, 
                                       return_columns => ARRAY['id','content'], num_results=>:num_results);
             """), {"query":query, "num_results": 5})
            
            chunks = [r[0]['content'] for r in result.fetchall()]
            return chunks
    