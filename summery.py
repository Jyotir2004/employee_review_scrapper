# # import google.genai as genai



# # genai.configure(api_key="AIzaSyDcgGP4JSNYscMxiN1QYwD_705BULDUX0o")


# # model = genai.GenerativeModel("gemini-2.0-flash")


# # async def analyze_sentiment(text: str):

# #     if not text.strip():
# #         return "Neutral"

# #     prompt = f"""
# #     Analyze the sentiment of this employee review.

# #     Return ONLY one word:
# #     Positive
# #     Negative
# #     Neutral

# #     Review:
# #     {text}
# #     """

# #     try:

# #         response = model.generate_content(prompt)

# #         sentiment = response.text.strip()

# #         return sentiment

# #     except Exception as e:

# #         print("Sentiment Error:", e)

# #         return "Unknown"
# # import aiohttp

# # OLLAMA_URL = "http://localhost:11434/api/generate"


# # async def analyze_sentiment(text: str, rating: int):

# #     if not text or not text.strip():

# #        if rating >= 4:
# #         return "Positive"
# #        elif rating <= 2:
# #         return "Negative"
# #        elif rating == 3:
# #         return "Neutral"

# #     prompt = f"""
# #     Classify sentiment of this employee review.

# #     Return ONLY one word:
# #     Positive / Negative / Neutral

# #     Review:
# #     {text} (Rating: {rating})
# #     """

# #     payload = {
# #         "model": "gemma3:4b",
# #         "prompt": prompt,
# #         "stream": False
# #     }

# #     try:
# #         async with aiohttp.ClientSession() as session:
# #             async with session.post(OLLAMA_URL, json=payload) as resp:
# #                 data = await resp.json()
# #                 return data.get("response", "Neutral").strip()

# #     except Exception as e:
# #         print("Ollama Error:", e)
# #         return "Unknown"

# import aiohttp

# OLLAMA_URL = "http://localhost:11434/api/generate"


# async def analyze_sentiment(text: str, rating):

#     try:
#         rating = int(rating)
#     except:
#         rating = 0

#     if not text or not text.strip():

#         if rating >= 4:
#             return "Positive"

#         elif rating <= 2:
#             return "Negative"

#         elif rating == 3:
#             return "Neutral"

#         return "Unknown"

#     prompt = f"""
#     Classify sentiment of this employee review.

#     Return ONLY one word:
#     Positive / Negative / Neutral

#     Review:
#     {text} (Rating: {rating})
#     """

#     payload = {
#         "model": "gemma3:4b",
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         async with aiohttp.ClientSession() as session:

#             async with session.post(
#                 OLLAMA_URL,
#                 json=payload
#             ) as resp:

#                 data = await resp.json()

#                 return data.get(
#                     "response",
#                     "Neutral"
#                 ).strip()

#     except Exception as e:

#         print("Ollama Error:", e)

#         return "Unknown" - sentiment.py



# async def analyze_page_summary(session, page_reviews, page_number):

#     texts = []
#     ratings = []

#     for r in page_reviews:

#         text = (r.get("review") or "").strip()
#         rating = r.get("rating", 0)

#         if text:
#             texts.append(text)

#         try:
#             ratings.append(int(rating))
#         except:
#             pass

#     if not texts:

#         return {
#             "page": page_number,
#             "positive_count": 0,
#             "negative_count": 0,
#             "neutral_count": 0,
#             "page_summary": "",
#             "positive_dimensions": [],
#             "negative_dimensions": [],
#             "dimension_summary": {}
#         }

#     avg_rating = sum(ratings) / len(ratings) if ratings else 0

#     review_text = "\n".join(texts)

#     prompt = f"""
# You are an expert HR analytics AI.

# Analyze ALL reviews from one page.

# Return ONLY valid JSON.

# Tasks:
# 1. Count positive, negative, neutral reviews
# 2. Summarize the page
# 3. Extract positive & negative dimensions
# 4. Provide dimension-wise summary
# 5.provide sentiment wise summary

# Dimensions:
# Salary, Management, Work Culture, Work Life Balance,
# Career Growth, Learning Opportunities, Team, Job Security

# Format:
# {{
#   "positive_count": 0,
#   "negative_count": 0,
#   "neutral_count": 0,

#   "page_summary": "",

#   "positive_dimensions": [],
#   "negative_dimensions": [],

#   "dimension_summary": {{
#     "Salary": {{
#       "sentiment": "Negative",
#       "summary": ""
#     }}
#   }}
# }}

# Rules:
# - ONLY JSON
# - No markdown
# - No explanation
# - Keep it concise

# Average Rating: {avg_rating}/5

# Reviews:
# {review_text}
# """

#     payload = {
#         "model": "gemma3:4b",
#         "prompt": prompt,
#         "stream": False,
#         "format": "json"
#     }

#     try:

#         async with session.post(OLLAMA_URL, json=payload) as resp:

#             data = await resp.json()
#             raw = data.get("response", "{}").strip()

#             print(f"\nPAGE {page_number} RAW RESPONSE:\n{raw}")

#             match = re.search(r"\{.*\}", raw, re.DOTALL)
#             if not match:
#                 return {}

#             parsed = json.loads(match.group(0))
#             parsed["page"] = page_number

#             return parsed

#     except Exception as e:
#         print(f"Page {page_number} Error:", e)
#         return {}



# def aggregate_results(page_results):

#     totals = {
#         "positive": 0,
#         "negative": 0,
#         "neutral": 0
#     }

#     all_page_summaries = []

#     positive_dims = []
#     negative_dims = []

#     dimension_summary = defaultdict(lambda: {
#         "positive": 0,
#         "negative": 0,
#         "neutral": 0,
#         "summaries": []
#     })

  
#     for r in page_results:

#         if not r:
#             continue

#         totals["positive"] += r.get("positive_count", 0)
#         totals["negative"] += r.get("negative_count", 0)
#         totals["neutral"] += r.get("neutral_count", 0)

#         all_page_summaries.append(r.get("page_summary", ""))

#         positive_dims.extend(r.get("positive_dimensions", []))
#         negative_dims.extend(r.get("negative_dimensions", []))


#         for dim, data in r.get("dimension_summary", {}).items():

#             dimension_summary[dim]["summaries"].append(
#                 data.get("summary", "")
#             )

#             sentiment = data.get("sentiment", "Neutral")

#             if sentiment == "Positive":
#                 dimension_summary[dim]["positive"] += 1

#             elif sentiment == "Negative":
#                 dimension_summary[dim]["negative"] += 1

#             else:
#                 dimension_summary[dim]["neutral"] += 1

 
#     return {
#         "total_positive_reviews": totals["positive"],
#         "total_negative_reviews": totals["negative"],
#         "total_neutral_reviews": totals["neutral"],

#         "top_positive_dimensions":
#             Counter(positive_dims).most_common(10),

#         "top_negative_dimensions":
#             Counter(negative_dims).most_common(10),

#         "page_summaries":
#             all_page_summaries,

#         "dimension_summary":
#             dict(dimension_summary)
#     }




# async def analyze_all_pages(all_pages_reviews):

#     async with aiohttp.ClientSession() as session:

#         tasks = [
#             analyze_page_summary(session, page, i + 1)
#             for i, page in enumerate(all_pages_reviews)
#         ]

#         page_results = await asyncio.gather(*tasks)

#     return aggregate_results(page_results) 
