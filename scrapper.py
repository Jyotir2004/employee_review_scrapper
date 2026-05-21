# from playwright.async_api import async_playwright
# from bs4 import BeautifulSoup

# import asyncio
# import random
# import re
# import json

# from collections import Counter

# from save_reviews import save_reviews_to_json
# # from analysis import analyze_employee_review




# BASE_URL = (
#     "https://www.ambitionbox.com/"
#     "reviews/cloud-analogy-reviews?page={}"
# )

# MAX_SCROLLS = 8

# SCROLL_DELAY = 2




# def clean_text(text: str) -> str:

#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# def extract_rating(block: str) -> str:

#     match = re.search(
#         r"Star\s*([1-5]\.\d)",
#         block,
#         re.IGNORECASE | re.DOTALL
#     )

#     if match:
#         return match.group(1)

#     fallback = re.search(
#         r"\b([1-5]\.\d)\b",
#         block
#     )

#     if fallback:
#         return fallback.group(1)

#     return "0"


# def extract_likes(block: str) -> str:

#     if "Dislikes" in block:

#         likes = block.split(
#             "Dislikes"
#         )[0]

#     else:
#         likes = block

#     likes = re.sub(
#         r"Star\s*[1-5]\.\d",
#         "",
#         likes
#     )

#     categories = [
#         "Salary",
#         "Company culture",
#         "Job security",
#         "Promotions",
#         "Work-life balance",
#         "Skill development",
#         "Work satisfaction"
#     ]

#     for category in categories:

#         likes = likes.replace(
#             category,
#             ""
#         )

#     likes = clean_text(likes)

#     return likes[:500]


# def extract_dislikes(block: str) -> str:

#     if "Dislikes" not in block:
#         return ""

#     try:

#         dislikes = block.split(
#             "Dislikes"
#         )[1]

#         stop_words = [
#             "Work Details",
#             "Helpful Share",
#             "Company Response"
#         ]

#         for word in stop_words:

#             if word in dislikes:

#                 dislikes = dislikes.split(
#                     word
#                 )[0]

#         dislikes = clean_text(dislikes)

#         return dislikes[:500]

#     except:
#         return ""


# def extract_work_details(block: str) -> str:

#     match = re.search(
#         r"Work Details\s*(.*?)(?:Likes|Dislikes|$)",
#         block,
#         re.IGNORECASE | re.DOTALL
#     )

#     if not match:
#         return ""

#     work_details = clean_text(
#         match.group(1)
#     )

#     return work_details


# def extract_detailed_ratings(
#     block: str
# ) -> dict:

#     categories = [
#         "Salary",
#         "Company culture",
#         "Job security",
#         "Promotions",
#         "Work-life balance",
#         "Skill development",
#         "Work satisfaction"
#     ]

#     ratings = {}

#     for category in categories:

#         pattern = (
#             rf"{re.escape(category)}"
#             rf"\s*([1-5]\.\d)"
#         )

#         match = re.search(
#             pattern,
#             block,
#             re.IGNORECASE
#         )

#         if match:

#             ratings[category] = match.group(1)

#     return ratings




# async def parse_review(
#     block: str
# ):

#     overall_rating = extract_rating(
#         block
#     )

#     likes = extract_likes(
#         block
#     )

#     dislikes = extract_dislikes(
#         block
#     )

#     combined_text = (
#         f"{likes} {dislikes}"
#     ).strip()

#     # ai_analysis = await analyze_employee_review(
#     #     combined_text,
#     #     overall_rating
#     # )

#     return {

#         "overall_rating":
#             overall_rating,

#         "detailed_ratings":
#             extract_detailed_ratings(
#                 block
#             ),

#         "work_details":
#             extract_work_details(
#                 block
#             ),

#         "likes":
#             likes,

#         "dislikes":
#             dislikes,

#         # "ai_analysis":
#         #     ai_analysis
#     }




# async def get_reviews(
#     page_no: int
# ):

#     url = BASE_URL.format(
#         page_no
#     )

#     reviews = []

#     async with async_playwright() as p:

#         browser = await p.chromium.launch(
#             headless=False
#         )

#         page = await browser.new_page()

#         try:

#             print(
#                 f"\nSCRAPING PAGE {page_no}"
#             )

#             print(f"Opening: {url}")

#             await page.goto(
#                 url,
#                 wait_until="networkidle",
#                 timeout=60000
#             )

#             await asyncio.sleep(
#                 random.uniform(4, 6)
#             )

       

#             for _ in range(MAX_SCROLLS):

#                 await page.mouse.wheel(
#                     0,
#                     3000
#                 )

#                 await asyncio.sleep(
#                     SCROLL_DELAY
#                 )

        

#             html = await page.content()

#             soup = BeautifulSoup(
#                 html,
#                 "html.parser"
#             )

#             text = soup.get_text(
#                 "\n",
#                 strip=True
#             )

#             blocks = text.split(
#                 "Likes"
#             )

#             print(
#                 f"Blocks Found: {len(blocks)}"
#             )

        

#             for block in blocks[1:]:

#                 try:

#                     review = await parse_review(
#                         block
#                     )

#                     if (
#                         review["likes"]
#                         or review["dislikes"]
#                     ):

#                         reviews.append(
#                             review
#                         )

#                 except Exception as e:

#                     print(
#                         "Review Parsing Error:",
#                         e
#                     )

#             await browser.close()

#             return {

#                 "success": True,

#                 "page": page_no,

#                 "total_reviews":
#                     len(reviews),

#                 "data":
#                     reviews
#             }

#         except Exception as e:

#             await browser.close()

#             return {

#                 "success": False,

#                 "page": page_no,

#                 "error": str(e)
#             }




# def analyze_page_summary(
#     reviews
# ):

#     positive = 0
#     negative = 0
#     neutral = 0

#     positive_dimensions = []
#     negative_dimensions = []

#     summaries = []

#     for review in reviews:

#         analysis = review.get(
#             "ai_analysis",
#             {}
#         )

#         sentiment = analysis.get(
#             "sentiment",
#             "Neutral"
#         )

#         if sentiment == "Positive":
#             positive += 1

#         elif sentiment == "Negative":
#             negative += 1

#         else:
#             neutral += 1

#         positive_dimensions.extend(
#             analysis.get(
#                 "positive_dimensions",
#                 []
#             )
#         )

#         negative_dimensions.extend(
#             analysis.get(
#                 "negative_dimensions",
#                 []
#             )
#         )

#         summary = analysis.get(
#             "overall_positive_summary",
#             ""
#         )

#         if summary:
#             summaries.append(summary)

#     return {

#         "positive_reviews":
#             positive,

#         "negative_reviews":
#             negative,

#         "neutral_reviews":
#             neutral,

#         "top_positive_dimensions":
#             Counter(
#                 positive_dimensions
#             ).most_common(10),

#         "top_negative_dimensions":
#             Counter(
#                 negative_dimensions
#             ).most_common(10),

#         "summaries":
#             summaries
#     }




# async def scrape_multiple_pages():

#     page_no = 1

#     all_reviews = []

#     all_page_analysis = []

#     while True:

#         result = await get_reviews(
#             page_no
#         )

#         if (
#             not result["success"]
#             or not result["data"]
#         ):

#             print(
#                 f"\nNo data found on page "
#                 f"{page_no}"
#             )

#             break

#         reviews = result["data"]

#         page_analysis = analyze_page_summary(
#             reviews
#         )

#         all_page_analysis.append({

#             "page": page_no,

#             "analysis":
#                 page_analysis
#         })

#         all_reviews.extend(
#             reviews
#         )

#         print(
#             f"Page {page_no} scraped "
#             f"with {len(reviews)} reviews"
#         )

#         page_no += 1

#         await asyncio.sleep(
#             random.uniform(3, 5)
#         )

#     return {

#         "success": True,

#         "total_pages_scraped":
#             len(all_page_analysis),

#         "total_reviews":
#             len(all_reviews),

#         "page_analysis":
#             all_page_analysis,

#         "reviews":
#             all_reviews
#     }




# def final_overall_analysis(
#     page_analysis
# ):

#     total_positive = 0
#     total_negative = 0
#     total_neutral = 0

#     all_positive_dimensions = []
#     all_negative_dimensions = []

#     all_summaries = []

#     for page in page_analysis:

#         analysis = page["analysis"]

#         total_positive += analysis[
#             "positive_reviews"
#         ]

#         total_negative += analysis[
#             "negative_reviews"
#         ]

#         total_neutral += analysis[
#             "neutral_reviews"
#         ]

#         all_positive_dimensions.extend([
#             dim[0]
#             for dim in analysis[
#                 "top_positive_dimensions"
#             ]
#         ])

#         all_negative_dimensions.extend([
#             dim[0]
#             for dim in analysis[
#                 "top_negative_dimensions"
#             ]
#         ])

#         all_summaries.extend(
#             analysis.get(
#                 "summaries",
#                 []
#             )
#         )

#     return {

#         "total_positive_reviews":
#             total_positive,

#         "total_negative_reviews":
#             total_negative,

#         "total_neutral_reviews":
#             total_neutral,

#         "overall_positive_dimensions":
#             Counter(
#                 all_positive_dimensions
#             ).most_common(10),

#         "overall_negative_dimensions":
#             Counter(
#                 all_negative_dimensions
#             ).most_common(10),

#         "overall_summaries":
#             all_summaries
#     }



# async def main():

#     result = await scrape_multiple_pages()

#     if not result["success"]:

#         print(
#             "\nScraping Failed"
#         )

#         return

#     save_reviews_to_json(
#         result
#     )

#     final_analysis = final_overall_analysis(
#         result["page_analysis"]
#     )

#     print("\n" + "=" * 80)
#     print("FINAL ANALYSIS")
#     print("=" * 80)

#     print(
#         f"\nTotal Pages Scraped: "
#         f"{result['total_pages_scraped']}"
#     )

#     print(
#         f"Total Reviews Scraped: "
#         f"{result['total_reviews']}"
#     )

#     print(
#         f"\nTotal Positive Reviews: "
#         f"{final_analysis['total_positive_reviews']}"
#     )

#     print(
#         f"Total Negative Reviews: "
#         f"{final_analysis['total_negative_reviews']}"
#     )

#     print(
#         f"Total Neutral Reviews: "
#         f"{final_analysis['total_neutral_reviews']}"
#     )

#     print("\nTop Positive Dimensions:")

#     for dim, count in final_analysis[
#         "overall_positive_dimensions"
#     ]:

#         print(f"  • {dim}: {count}")

#     print("\nTop Negative Dimensions:")

#     for dim, count in final_analysis[
#         "overall_negative_dimensions"
#     ]:

#         print(f"  • {dim}: {count}")

#     print("\n" + "=" * 80)
#     print("SCRAPING COMPLETED")
#     print("=" * 80)


# if __name__ == "__main__":

#     asyncio.run(main())




from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

import asyncio
import random
import re
import json

from collections import Counter

from save_reviews import save_reviews_to_json
# from analysis import analyze_employee_review




BASE_URL = (
    "https://www.ambitionbox.com/"
    "reviews/cloud-analogy-reviews?page={}"
)

MAX_SCROLLS = 8

SCROLL_DELAY = 2




def clean_text(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_rating(block: str) -> str:

    match = re.search(
        r"Star\s*([1-5]\.\d)",
        block,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1)

    fallback = re.search(
        r"\b([1-5]\.\d)\b",
        block
    )

    if fallback:
        return fallback.group(1)

    return "0"


def extract_likes(block: str) -> str:

    if "Dislikes" in block:

        likes = block.split(
            "Dislikes"
        )[0]

    else:
        likes = block

    likes = re.sub(
        r"Star\s*[1-5]\.\d",
        "",
        likes
    )

    categories = [
        "Salary",
        "Company culture",
        "Job security",
        "Promotions",
        "Work-life balance",
        "Skill development",
        "Work satisfaction"
    ]

    for category in categories:

        likes = likes.replace(
            category,
            ""
        )

    likes = clean_text(likes)

    return likes[:500]


def extract_dislikes(block: str) -> str:

    if "Dislikes" not in block:
        return ""

    try:

        dislikes = block.split(
            "Dislikes"
        )[1]

        stop_words = [
            "Work Details",
            "Helpful Share",
            "Company Response"
        ]

        for word in stop_words:

            if word in dislikes:

                dislikes = dislikes.split(
                    word
                )[0]

        dislikes = clean_text(dislikes)

        return dislikes[:500]

    except:
        return ""


def extract_work_details(block: str) -> str:

    match = re.search(
        r"Work Details\s*(.*?)(?:Likes|Dislikes|$)",
        block,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return ""

    work_details = clean_text(
        match.group(1)
    )

    return work_details


def extract_detailed_ratings(
    block: str
) -> dict:

    categories = [
        "Salary",
        "Company culture",
        "Job security",
        "Promotions",
        "Work-life balance",
        "Skill development",
        "Work satisfaction"
    ]

    ratings = {}

    for category in categories:

        pattern = (
            rf"{re.escape(category)}"
            rf"\s*([1-5]\.\d)"
        )

        match = re.search(
            pattern,
            block,
            re.IGNORECASE
        )

        if match:

            ratings[category] = match.group(1)

    return ratings




async def parse_review(
    block: str
):

    overall_rating = extract_rating(
        block
    )

    likes = extract_likes(
        block
    )

    dislikes = extract_dislikes(
        block
    )

    combined_text = (
        f"{likes} {dislikes}"
    ).strip()

    # ai_analysis = await analyze_employee_review(
    #     combined_text,
    #     overall_rating
    # )

    return {

        "overall_rating":
            overall_rating,

        "detailed_ratings":
            extract_detailed_ratings(
                block
            ),

        "work_details":
            extract_work_details(
                block
            ),

        "likes":
            likes,

        "dislikes":
            dislikes,

        # "ai_analysis":
        #     ai_analysis
    }




async def get_reviews(
    page_no: int
):

    url = BASE_URL.format(
        page_no
    )

    reviews = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        try:

            print(
                f"\nSCRAPING PAGE {page_no}"
            )

            print(f"Opening: {url}")

            await page.goto(
                url,
                wait_until="networkidle",
                timeout=60000
            )

            await asyncio.sleep(
                random.uniform(4, 6)
            )

       

            for _ in range(MAX_SCROLLS):

                await page.mouse.wheel(
                    0,
                    3000
                )

                await asyncio.sleep(
                    SCROLL_DELAY
                )

        

            html = await page.content()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            text = soup.get_text(
                "\n",
                strip=True
            )

            blocks = text.split(
                "Likes"
            )

            print(
                f"Blocks Found: {len(blocks)}"
            )

        

            for block in blocks[1:]:

                try:

                    review = await parse_review(
                        block
                    )

                    if (
                        review["likes"]
                        or review["dislikes"]
                    ):

                        reviews.append(
                            review
                        )

                except Exception as e:

                    print(
                        "Review Parsing Error:",
                        e
                    )

            await browser.close()

            return {

                "success": True,

                "page": page_no,

                "total_reviews":
                    len(reviews),

                "data":
                    reviews
            }

        except Exception as e:

            await browser.close()

            return {

                "success": False,

                "page": page_no,

                "error": str(e)
            }




def analyze_page_summary(
    reviews
):

    positive = 0
    negative = 0
    neutral = 0

    positive_dimensions = []
    negative_dimensions = []

    summaries = []

    for review in reviews:

        analysis = review.get(
            "ai_analysis",
            {}
        )

        sentiment = analysis.get(
            "sentiment",
            "Neutral"
        )

        if sentiment == "Positive":
            positive += 1

        elif sentiment == "Negative":
            negative += 1

        else:
            neutral += 1

        positive_dimensions.extend(
            analysis.get(
                "positive_dimensions",
                []
            )
        )

        negative_dimensions.extend(
            analysis.get(
                "negative_dimensions",
                []
            )
        )

        summary = analysis.get(
            "overall_positive_summary",
            ""
        )

        if summary:
            summaries.append(summary)

    return {

        "positive_reviews":
            positive,

        "negative_reviews":
            negative,

        "neutral_reviews":
            neutral,

        "top_positive_dimensions":
            Counter(
                positive_dimensions
            ).most_common(10),

        "top_negative_dimensions":
            Counter(
                negative_dimensions
            ).most_common(10),

        "summaries":
            summaries
    }




async def scrape_multiple_pages():

    page_no = 1

    all_reviews = []

    all_page_analysis = []

    while True:

        result = await get_reviews(
            page_no
        )

        if (
            not result["success"]
            or not result["data"]
        ):

            print(
                f"\nNo data found on page "
                f"{page_no}"
            )

            break

        reviews = result["data"]

        page_analysis = analyze_page_summary(
            reviews
        )

        all_page_analysis.append({

            "page": page_no,

            "analysis":
                page_analysis
        })

        all_reviews.extend(
            reviews
        )

        print(
            f"Page {page_no} scraped "
            f"with {len(reviews)} reviews"
        )

        page_no += 1

        await asyncio.sleep(
            random.uniform(3, 5)
        )

    return {

        "success": True,

        "total_pages_scraped":
            len(all_page_analysis),

        "total_reviews":
            len(all_reviews),

        "page_analysis":
            all_page_analysis,

        "reviews":
            all_reviews
    }




def final_overall_analysis(
    page_analysis
):

    total_positive = 0
    total_negative = 0
    total_neutral = 0

    all_positive_dimensions = []
    all_negative_dimensions = []

    all_summaries = []

    for page in page_analysis:

        analysis = page["analysis"]

        total_positive += analysis[
            "positive_reviews"
        ]

        total_negative += analysis[
            "negative_reviews"
        ]

        total_neutral += analysis[
            "neutral_reviews"
        ]

        all_positive_dimensions.extend([
            dim[0]
            for dim in analysis[
                "top_positive_dimensions"
            ]
        ])

        all_negative_dimensions.extend([
            dim[0]
            for dim in analysis[
                "top_negative_dimensions"
            ]
        ])

        all_summaries.extend(
            analysis.get(
                "summaries",
                []
            )
        )

    return {

        "total_positive_reviews":
            total_positive,

        "total_negative_reviews":
            total_negative,

        "total_neutral_reviews":
            total_neutral,

        "overall_positive_dimensions":
            Counter(
                all_positive_dimensions
            ).most_common(10),

        "overall_negative_dimensions":
            Counter(
                all_negative_dimensions
            ).most_common(10),

        "overall_summaries":
            all_summaries
    }



async def main():

    result = await scrape_multiple_pages()

    if not result["success"]:

        print(
            "\nScraping Failed"
        )

        return

    save_reviews_to_json(
        result
    )

    final_analysis = final_overall_analysis(
        result["page_analysis"]
    )

    print("\n" + "=" * 80)
    print("FINAL ANALYSIS")
    print("=" * 80)

    print(
        f"\nTotal Pages Scraped: "
        f"{result['total_pages_scraped']}"
    )

    print(
        f"Total Reviews Scraped: "
        f"{result['total_reviews']}"
    )

    print(
        f"\nTotal Positive Reviews: "
        f"{final_analysis['total_positive_reviews']}"
    )

    print(
        f"Total Negative Reviews: "
        f"{final_analysis['total_negative_reviews']}"
    )

    print(
        f"Total Neutral Reviews: "
        f"{final_analysis['total_neutral_reviews']}"
    )

    print("\nTop Positive Dimensions:")

    for dim, count in final_analysis[
        "overall_positive_dimensions"
    ]:

        print(f"  • {dim}: {count}")

    print("\nTop Negative Dimensions:")

    for dim, count in final_analysis[
        "overall_negative_dimensions"
    ]:

        print(f"  • {dim}: {count}")

    print("\n" + "=" * 80)
    print("SCRAPING COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    asyncio.run(main()) 
