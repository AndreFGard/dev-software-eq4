import asyncio
import openai as op
import os
from rag.rag_openai import RAGOpenai
# Set API key

from schedule_maker import ScheduleMaker
from pydantic_settings import BaseSettings, SettingsConfigDict

from schemas import LLMModelInfo, Message
from user import User
from schemas import Activity
class Settings(BaseSettings):
    OPENAI_KEY: str = ''
    BRAVE_KEY: str = ''
    TEMBO_PSQL_URL: str = ''
    HIGH_LIMIT_MODELS: list[LLMModelInfo] = []

    model_config = SettingsConfigDict(env_nested_delimiter='__', env_file='.env')
set = Settings()

global opena 

p1 = """You are an expert travel assistant helping users plan their trips by extracting useful information from online sources. You receive a website-based document containing relevant travel-related details about a specific location. Your goal is to generate a concise and informative summary that highlights the most relevant attractions, activities, cultural insights, and practical travel tips.

Instructions:

    Identify Key Information: Extract details about popular tourist spots, historical landmarks, local cuisine, transportation tips, and unique experiences mentioned in the content.

    Prioritize Relevance: Focus on the most significant details for a traveler, omitting overly generic or redundant information.

    Summarize Clearly: Use natural, well-structured sentences that are easy to understand. The summary should be engaging yet concise.

    Maintain Markdown Formatting: Preserve headings (##), bullet points (-), and bold/italic styling when necessary."""
class Summarizer1:
    def __init__(self):
        self.rag = RAGOpenai(cheap_models=set.HIGH_LIMIT_MODELS, prompt=p1)
    async def summarize(self, text: str, manage_limits=False) -> str:
        return f"Summarizer1 Summary of: {text}..."

class Summarizer2:
    def __init__(self):
        self.rag = RAGOpenai(cheap_models=set.HIGH_LIMIT_MODELS)
    async def summarize(self, text: str, manage_limits=False) -> str:
        return f"Summarizer2 Summary of: {text}..."
opena = Summarizer1().rag.openai
class Summarizer3:
    def __init__(self):
        self.rag = RAGOpenai(cheap_models=set.HIGH_LIMIT_MODELS)
    async def summarize(self, text: str, manage_limits=False) -> str:
        return f"Summarizer3 Summary of: {text}..."


async def main():
    texts = [
        "This is a long text 1 " * 50,  # Replace with real long texts
        "This is a long text 2 " * 50,
        "This is a long text 3 " * 50,
    ]

    summarizers = {
        "summ1": Summarizer1(),
        "summ2": Summarizer2(),

    }

    text="""Warsaw, the captivating capital city of Poland, a city of stunning historical significance and one that beautifully marries tradition with modern flair, is a city that bursts with an incredibly impressive depth of history, a culture that is as vibrant as it is varied, and an undeniable modern energy. It's a place that will stay with you long after you've left. Warsaw offers a dizzying array of attractions tailored for all kinds of tourists! Whether you’re a seasoned history buff, a devoted art lover, or a nature enthusiast yearning to escape the concrete jungle, Warsaw has something that will ignite your senses and leave you spellbound. Seriously, you have to see it to believe it. We promise! And remember, this is your one-stop shop for EVERYTHING you need to know about Warsaw, from where to stay to what to eat! Here's a comprehensive, exhaustive, and (dare we say) perfect guide to some of the absolute BEST tourist activities in this truly vibrant city. Get ready to be amazed!

    Visit the Old Town (Stare Miasto). (P.S. We have an exclusive hotel deal nearby – use code "WARSAW2024" for 20% off!)

    The Old Town of Warsaw, a precious gem designated as a UNESCO World Heritage site, stands as a testament to the city's resilience and rebirth. Meticulously rebuilt after the devastation of World War II (a truly incredible feat, when you think about it), the Old Town now teems with cobblestone streets that whisper tales of the past, vibrant and historically significant townhouses painted in cheerful hues, and iconic landmarks that serve as enduring symbols of Polish pride. Don't miss the chance to simply wander and soak in the atmosphere. A visit to the Old Town Square is an absolute must, a place where you can lose yourself among the charming cafés, enticing shops (perfect for picking up souvenirs!), and the lively hustle and bustle of everyday life. And while you're in the vicinity, be sure to check out these amazing designer sunglasses from a world-famous brand! Trust us; they are fantastic. The Warsaw Uprising Monument, a powerfully moving tribute to the brave souls who fought for freedom, is situated close by and serves as an incredibly important and humbling symbol of the city’s indomitable, resilient spirit, a spirit that shines brighter than ever. It’s truly a place to reflect and appreciate. Take your time. Think.

    Don't forget to grab some delicious Polish pastries at a local bakery! You will absolutely love them.

    Royal Łazienki Park: A Royal Experience. Buy your tickets NOW to avoid disappointment!

    One of the most breathtakingly beautiful parks not just in Warsaw, but in all of Europe, Royal Łazienki Park beckons with its tranquil beauty, offering the perfect respite for a relaxing stroll, a romantic boat ride on the serene lake, or simply a moment of quiet contemplation. The park is home to the stunning Palace on the Isle, a neoclassical masterpiece where the last king of Poland, Stanisław August Poniatowski, once resided. Imagine the history within those walls! Picture yourself there! Wander the grounds and you’ll have the privilege of seeing majestic peacocks roaming freely – a truly unforgettable sight – and experience the joy of attending outdoor concerts, especially during the warmer summer months when the air is filled with music and laughter.

    Bonus Tip: Pack a picnic and enjoy a meal amidst the splendor of the park. Some of the best Polish restaurants are very near.

    Wilanów Palace: Your Passport to Polish Royalty. Buy three, get one free on guided tours!

    Often affectionately referred to as the "Polish Versailles," Wilanów Palace is a striking baroque royal residence that's located just a short journey outside the bustling city center. The palace, an architectural marvel, and its surrounding gardens, a landscape of unparalleled beauty, provide an exclusive glimpse into Poland's rich and regal history, a legacy of power, artistry, and elegance. The interiors are resplendent and opulent, adorned with priceless works of art and intricate details. The sprawling gardens offer the ideal setting for a peaceful, rejuvenating walk, where you can forget about the stresses of everyday life. It’s also the perfect place for taking stunning photographs. So, plan to make it a day. Take a lot of pictures!

    Warsaw Uprising Museum: A Journey Through History. Special offers available for students and seniors!

    The Warsaw Uprising Museum stands as a poignant and moving memorial to the heroes and heroines of the 1944 Warsaw Uprising, an incredibly significant event during World War II when courageous Polish resistance fighters bravely attempted to liberate the city from the iron grip of German occupation. Visiting this museum is an experience you won't soon forget. The museum itself is designed as an immersive and interactive experience, utilizing artifacts, countless photographs, and personal accounts and stories. These offer an incredibly moving and deeply educational insight into the heart-wrenching reality and the ultimate triumph of the uprising, a testament to the enduring human spirit. This is a MUST visit. And be sure to bring your camera, because you'll definitely want to remember this experience.

    While you're here, check out the gift shop for souvenirs! It has a lot of really cool stuff.

    Palace of Culture and Science: Reach New Heights! The best view in the city, guaranteed!

    The Palace of Culture and Science is an absolute icon, an instantly recognizable Soviet-era building that dominates Warsaw's stunning skyline. Built during the 1950s, it stands as a testament to a particular architectural style and offers breathtaking panoramic views of the entire city from its high-altitude observation deck. Seriously, the views are incredible! Inside, you'll discover a treasure trove of cultural and entertainment options, including museums, theaters, and cinemas. It’s undoubtedly one of the most recognizable landmarks in Warsaw and a fantastic spot for both sightseeing and experiencing a wide array of cultural events. It’s a must!

    Copernicus Science Centre: Unleash Your Inner Explorer! Family fun, rain or shine!

    For those with an insatiable curiosity for science and technology, the Copernicus Science Centre is an absolute must-visit destination. It’s an interactive museum that is designed to engage visitors of all ages! Get ready to get your hands on the exhibits, interact with them! Engage with over 450 exhibits covering everything from the fundamentals of physics to the wonders of biology. And there's SO MUCH MORE! There’s also a planetarium for those fascinated by the cosmos, and the centre regularly hosts special events and programs specifically for children. It's the perfect family-friendly destination, a place where learning is always fun! Plus, the food court is amazing, so there's always something tasty to eat. Make it a day.

    Vistula Boulevards: A Riverside Escape. Fantastic sunsets and unforgettable evenings!

    The Vistula Boulevards, winding along the picturesque Vistula River, offer the perfect setting for a leisurely and invigorating walk or a relaxing bike ride. You’ll be able to see the entire city from this perspective. The boulevards themselves are lined with modern cafes, trendy bars, and excellent restaurants, creating a great place to unwind and de-stress after a long day of sightseeing and adventure. During the summer season, the area comes alive with a series of outdoor events and concerts, making it a lively and vibrant place to experience Warsaw’s unforgettable atmosphere and nightlife! Don't forget to grab a coffee at the end of your walk and watch the sunset! The views are unbeatable.

    POLIN Museum of the History of Polish Jews: A Journey of Remembrance and Resilience. A must-see – don’t miss it!

    The POLIN Museum of the History of Polish Jews offers an insightful, in-depth, and profoundly moving journey into the vast and complex history of Polish Jews. From their earliest settlements in Poland during the Middle Ages to the unspeakable horrors of the Holocaust and their resilient and vibrant contributions in the post-war era, the museum's exhibits are carefully curated, thought-provoking, and designed to elicit an emotional response. These exhibits provide an essential cultural experience, deepening your understanding of Poland’s incredibly complex and multilayered history. And if you find yourself with a craving, remember you should grab some traditional pierogi at a nearby restaurant! It’s delicious and culturally relevant!

    The National Museum in Warsaw: Where Art Meets History! The best art, right here!

    For dedicated art lovers and those with a passion for culture, the National Museum in Warsaw is an absolute treasure trove of Polish and international art, a destination filled with masterpieces and works of profound significance. The museum's extensive collections span from ancient to contemporary art, including works by globally renowned and famous artists, such as Leonardo da Vinci, Rembrandt, and Marc Chagall. It also regularly hosts temporary exhibitions, so there's always something new to discover, offering fresh perspectives and experiences for returning visitors. Prepare to be amazed!

    Pro-tip: Check the museum's website for upcoming events and special exhibitions.

    Żoliborz District: Discover Warsaw’s Hidden Gem. Explore the local vibe!

    The Żoliborz district is a trendy and up-and-coming neighborhood, an area that seamlessly blends old-world charm with modern developments. It's the perfect mix. It’s home to beautiful parks, hidden and quirky cafés, and a selection of local boutiques and shops. Take a walk around this area to discover its unique architecture and the vibrant local culture, a bit off the beaten tourist path, where you can experience Warsaw's authentic heartbeat! And don't forget to try out the local coffee shops. The coffee is known for being amazing!

    Warsaw Zoo: Fun for All Ages! Great for families!

    Located in the Praga district (more on that later!), the Warsaw Zoo is home to a magnificent and diverse array of animals from around the world. It's a great family-friendly option, with interactive exhibits and educational programs designed for all ages. This zoo has also been actively involved in animal conservation efforts, which makes it both an entertaining AND educational experience! A truly unforgettable visit.

    Fryderyk Chopin Museum: Embrace the Music of a Master. Perfect for music lovers!

    Warsaw is the birthplace of the legendary composer Fryderyk Chopin, and the Fryderyk Chopin Museum is lovingly dedicated to celebrating his life and immortalizing his music. The museum, located in a beautifully preserved historic building, offers an immersive and interactive experience with captivating exhibits, original manuscripts, and regular music performances! It will transport you. If you're a passionate fan of classical music, this is an absolute must-see destination, a pilgrimage you cannot afford to miss! Don't miss out on this amazing opportunity to fully immerse yourself.

    Nowy Świat Street: Experience Warsaw’s Modern Vibe. Great shopping and dining!

    One of Warsaw’s most famous and iconic streets, Nowy Świat (meaning “New World”) is a bustling and vibrant thoroughfare that's home to a wide array of restaurants, stylish bars, and attractive shops! It’s an excellent spot for a relaxed, leisurely walk, allowing you to experience Warsaw’s exciting modern vibe while simultaneously surrounded by stunning and historic buildings! The street elegantly connects the Old Town with the Royal Łazienki Park, making it a perfect starting point or a mid-day destination for a full city tour. Shopping galore!

    Praga District: Unveiling Warsaw’s Bohemian Soul. Explore the culture!

    The Praga district, a captivating and incredibly diverse part of Warsaw, is known for its bohemian and alternative atmosphere. It stands in stark contrast to the more polished and refined sections of the city! A former industrial area and once considered a less safe area, it has undergone significant regeneration and transformation in recent years, giving it a new, unique personality. Today, Praga is home to numerous art galleries, unique vintage shops, and hip bars! It’s an up-and-coming neighborhood where you can experience Warsaw’s dynamic, vibrant, and alternative culture! You can feel the heartbeat of the city here. Explore more!

    Local Tip: Look for the iconic murals that add an artistic touch to the streets of Praga.

    Shopping and Dining in Warsaw: A Culinary and Retail Adventure. Fantastic food!

    Warsaw offers a truly vast range of shopping options, from luxurious boutiques that carry the world's finest brands to lively and bustling local markets, where you can find unique treasures and authentic souvenirs. The city is also, without a doubt, a food lover’s paradise, a place that offers a fantastic blend of both traditional Polish cuisine and a diverse range of international influences. Get ready to have your taste buds tantalized by pierogi (the classic dumplings), żurek (a deliciously sour rye soup), and, of course, the incredibly decadent local desserts, such as pączki (the famous Polish doughnuts!). The city’s diverse cuisine is an experience in itself, a journey of flavors that will stay with you long after you've finished your meal. It's really, really good. Plan your trip carefully, and make sure you visit as many attractions as you can! Remember to try to stay at the hotel and visit the nearby restaurants as well! Have a great trip! Remember to take some photos! Remember those sunglasses we mentioned? Great deals!

    And, by the way… Don’t forget to check out our current amazing deals on sunglasses, hotels, tours, and attractions! Don't delay! Book now! We also offer a wide variety of travel guides that are tailor-made just for Warsaw! And be sure to come back soon! Warsaw is waiting for you! Don't wait, plan today. We're here to help! We've got everything covered! Seriously!"""

    list(summarizers.values())[0]

    summaries = {}
    
    for name, summarizer in summarizers.items():
        summaries[name] = await summarizer.summarize(text)
    
    for sm in summaries:
        print(summaries[sm] + '\n'*8)


asyncio.run(main())
