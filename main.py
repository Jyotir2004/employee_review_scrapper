# from fastapi import FastAPI
# from scrapper import get_reviews
# from models import ScrapeRequest

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Review Scraper API!"}


# @app.post("/scrape")
# def scrape(data: ScrapeRequest):
#     reviews = scrape_reviews(data.url, data.max_pages)
#     return {"total_reviews": len(reviews), "reviews": reviews}

# @app.get("reviews/{asin}")
# def get_reviews(asin: str, page: int = 1):
#     base_url = f"https://www.ambitionbox.com/reviews/amazon-reviews{asin}"
#     reviews = scrape_reviews(base_url, page)
#     return {"total_reviews": len(reviews), "reviews": reviews}


# from fastapi import FastAPI
# from scrapper import get_reviews

# app = FastAPI()





# @app.get("/reviews")
# def reviews(page: int = 1):

#     data = get_reviews(page)

#     return {
#         "total_reviews": len(data),
#         "reviews": data
#     }

# main.py

# main.py

# main.py

# from fastapi import FastAPI
# from scrapper import get_reviews

# app = FastAPI()



# @app.get("/reviews/{page}")
# def reviews(page: int):

#     return get_reviews(page)

# from fastapi import FastAPI
# from scrapper import get_reviews
# import scrapper






# @app.get("/reviews/{page_no}")
# async def reviews(page_no: int):

#     data = await get_reviews(page_no)

#     return data
# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Review Scraper API!"}

# @app.get("/reviews")
# async def fetch_reviews(page: int = Query(1, ge=1)):

#     result = await get_reviews(page)

#     if not result["success"]:
#         return {
#             "success": False,
#             "error": result["error"]
#         }

#     return {
#         "success": True,
#         "page": page,
#         "total_reviews": len(result["data"]),
#         "data": result["data"]
#     }

from fastapi import FastAPI, Query
import asyncio
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrapper import get_reviews, scrape_multiple_pages

app = FastAPI(title="AmbitionBox Scraper API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": " Welcome AmbitionBox Review Scraper API Running"
    }



@app.get("/reviews")
async def get_page_reviews(page: int = Query(1, ge=1)):

    result = await get_reviews(page)

    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }

    return {
        "success": True,
        "page": page,
        "total_reviews": len(result["data"]),
        "data": result["data"]
    }



# @app.get("/reviews/all")
# async def get_all_reviews():

#     result = await scrape_multiple_pages(1, 12)

#     return {
#         "success": True,
#         "total_reviews": result["total_reviews"],
#         "total_pages": result["total_pages"],
#         "data": result["data"]
#     }

# @app.get("/reviews/all")
# async def get_all_reviews():

#     try:

#         result = await scrape_multiple_pages()

#         return {
#             "success": True,

#             "summary": {
#                 "total_reviews": result["total_reviews"],
#                 "total_pages_scraped": result["total_pages_scraped"]
#             },

#             "pages_with_data": result["pages_with_data"],

#             "empty_pages": result["empty_pages"],

#             "data": result["data"]
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

# @app.get("/reviews/all")
# async def get_all_reviews():

#     try:

#         result = await scrape_multiple_pages()

#         return {
#             "success": True,

#             "summary": {
#                 "total_reviews": result["total_reviews"],
#                 "total_pages_scraped": result["total_pages_scraped"]
#             },

#             "pages_with_data": result["pages_with_data"],

#             "empty_pages": result["empty_pages"],

#             "data": result["data"]
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )






@app.get("/reviews/all")
async def get_all_reviews():

    try:

   
        result = await scrape_multiple_pages()

        return {
            "success": True,

            "summary": {
                "total_pages_scraped": result["total_pages_scraped"],
                "total_reviews": result["total_reviews"]
            },

            "scraped_pages": result["scraped_pages"],

     
            "data": result["data"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )