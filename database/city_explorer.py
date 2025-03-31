import asyncio
import os
from rag import RAG
from dotenv import load_dotenv

# Load environment variables from .env file

async def explore_cities():
    # Initialize the RAG with Brave API key from environment
    brave_key = os.getenv("BRAVE_KEY")
    tembo_psql_url = os.getenv("TEMBO_PSQL_URL")
    openai_key = os.getenv('OPENAI_KEY')
    rag = RAG(brave_api_key=brave_key, TEMBO_PSQL_URL=tembo_psql_url, openai_key=openai_key, top_results=3)
    
    # Cities to explore
    cities = [
        "Must-visit places in Fernando de Noronha Pernambuco",
        "Best beaches in Rio de Janeiro",
        "Things to do in Balneario Camboriu Santa Catarina",
        "Historical sites in Prague"
    ]
    async def f(q):
        try:
            return await rag.search_store(q)
        except:
            return await asyncio.sleep(0)

    results = {}
    torun = await asyncio.gather(*[f(query) for query in cities])
    # for city_query in cities:
    #     print(f"\n\n{'='*50}")
    #     print(f"Searching for: {city_query}")
    #     print(f"{'='*50}")
        
    #     # Retrieve information with search
    #     city_results = await rag.retrieve_with_search(city_query)
    #     results[city_query] = city_results
        
    #     # Display the results
    #     print(f"\nFound {len(city_results)} relevant chunks:")
    #     for i, chunk in enumerate(city_results[:3], 1):
    #         print(f"\n--- Result {i} ---")
    #         print(chunk.content[:300] + "..." if len(chunk.content) > 300 else chunk.content)
    #         print(f"Source: {chunk.url}")
    
    return results

if __name__ == "__main__":
    # Run the async function
    results = asyncio.run(explore_cities())
    
    # Summary of findings
    print("\n\n" + "="*50)
    print("SUMMARY OF CITY EXPLORATION")
    print("="*50)
    
    for query, data in results.items():
        city_name = query.split(" in ")[1] if " in " in query else query.split(" ")[3]
        print(f"\n{city_name}: Found {len(data)} information chunks")