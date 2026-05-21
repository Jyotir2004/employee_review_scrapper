# import aiohttp
# import json
# import re

# OLLAMA_URL = "http://localhost:11434/api/generate"

# DEFAULT_RESPONSE = {
#     "sentiment": "Unknown",
#     "overall_positive_summary": "",
#     "overall_negative_summary": "",
#     "positive_dimensions": [],
#     "negative_dimensions": [],
#     "dimension_sentiment": {}
# }


# async def analyze_employee_review(
#     text: str,
#     rating=0
# ):



#     try:
#         rating = int(rating)
#     except:
#         rating = 0

#     text = (text or "").strip()


#     if not text:

#         if rating >= 4:
#             sentiment = "Positive"

#         elif rating <= 2:
#             sentiment = "Negative"

#         elif rating == 3:
#             sentiment = "Neutral"

#         else:
#             sentiment = "Unknown"

#         return {
#             "sentiment": sentiment,
#             "overall_positive_summary": "No review text available",
#             "overall_negative_summary": "No review text available",
#             "positive_dimensions": [],
#             "negative_dimensions": [],
#             "dimension_sentiment": {}
#         }


#     prompt = f"""
# You are an expert HR analytics AI.

# Analyze the employee review and return ONLY valid JSON.

# Tasks:
# 1. Detect overall sentiment
# 2. Create concise positive summary
# 3. Create concise negative summary
# 4. Extract recurring positive dimensions
# 5. Extract recurring negative dimensions
# 6. Analyze sentiment for each dimension
# 7. Extract likes
# 8. Extract dislikes


# Possible sentiments:
# - Positive
# - Negative
# - Neutral

# Dimensions:
# - Salary
# - Management
# - Work Culture
# - Work Life Balance
# - Career Growth
# - Learning Opportunities
# - Team
# - Job Security

# Rules:
# - No markdown
# - No explanation
# - No extra text
# - Output ONLY JSON
# - Keep summaries concise
# - If a dimension is not mentioned use "Neutral"
# - If no likes/dislikes mentioned return empty list
# - likes/dislikes should not be short phrases, it should be in full sentence form as mentioned in the 

# JSON Format:
# {{
#   "sentiment": "Positive",
#   "overall_positive_summary": "...",
#   "overall_negative_summary": "...",
#   "positive_dimensions": [
#     "..."
#   ],
#   "negative_dimensions": [
#     "..."
#   ],
#   "dimension_sentiment": {{
#     "Salary": "Neutral",
#     "Management": "Positive",
#     "Work Culture": "Negative",
#     "Work Life Balance": "Neutral",
#     "Career Growth": "Neutral",
#     "Learning Opportunities": "Neutral",
#     "Team": "Positive",
#     "Job Security": "Neutral"
#   }}
#   "likes": [
#     "..."
#     ],
#     "dislikes": [
#     "..."
#     ]

# }}

# Employee Review:
# {text}

# Rating:
# {rating}/5
# """

#     payload = {
#         "model": "gemma3:4b",
#         "prompt": prompt,
#         "stream": False,
#         "format": "json"
#     }



#     try:

#         async with aiohttp.ClientSession() as session:

#             async with session.post(
#                 OLLAMA_URL,
#                 json=payload
#             ) as resp:

#                 if resp.status != 200:

#                     print(
#                         f"Ollama API Error: {resp.status}"
#                     )

#                     return DEFAULT_RESPONSE

#                 data = await resp.json()

#                 response = data.get(
#                     "response",
#                     "{}"
#                 ).strip()

#                 print("\nRAW LLM RESPONSE:")
#                 print(response)

              

#                 match = re.search(
#                     r"\{.*\}",
#                     response,
#                     re.DOTALL
#                 )

#                 if not match:

#                     print("JSON Parsing Failed")

#                     return DEFAULT_RESPONSE

#                 json_text = match.group(0)

#                 parsed = json.loads(json_text)

       

#                 return {
#                     "sentiment":
#                         parsed.get(
#                             "sentiment",
#                             "Unknown"
#                         ),

#                     "overall_positive_summary":
#                         parsed.get(
#                             "overall_positive_summary",
#                             ""
#                         ),

#                     "overall_negative_summary":
#                         parsed.get(
#                             "overall_negative_summary",
#                             ""
#                         ),

#                     "positive_dimensions":
#                         parsed.get(
#                             "positive_dimensions",
#                             []
#                         ),

#                     "negative_dimensions":
#                         parsed.get(
#                             "negative_dimensions",
#                             []
#                         ),

#                     "dimension_sentiment":
#                         parsed.get(
#                             "dimension_sentiment",
#                             {}
#                         )
#                 }

#     except Exception as e:

#         print(
#             "Review Analysis Error:",
#             e
#         )

#         return DEFAULT_RESPONSE 

