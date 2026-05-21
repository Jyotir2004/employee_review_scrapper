# # import aiohttp
# # import json

# # OLLAMA_URL = "http://localhost:11434/api/generate"


# # async def analyze_dimensions(text: str):

# #     prompt = f"""
# #     Analyze this employee review.

# #     Extract sentiment for these dimensions:

# #     - Salary
# #     - Management
# #     - Work Culture
# #     - Work Life Balance
# #     - Career Growth
# #     - Learning Opportunities
# #     - Team
# #     - Job Security

# #     Return ONLY valid JSON.

# #     Example format:

# #     {{
# #       "Salary": "Positive",
# #       "Management": "Negative"
# #     }}

# #     Review:
# #     {text}
# #     """

# #     payload = {
# #         "model": "gemma3:4b",
# #         "prompt": prompt,
# #         "stream": False
# #     }

# #     try:

# #         async with aiohttp.ClientSession() as session:

# #             async with session.post(
# #                 OLLAMA_URL,
# #                 json=payload
# #             ) as resp:

# #                 data = await resp.json()

# #                 response = data.get("response", "{}")

# #                 return json.loads(response)

# #     except Exception as e:

# #         print("Dimension Analysis Error:", e)

# #         return {}

# # import aiohttp
# # import json
# # import re

# # OLLAMA_URL = "http://localhost:11434/api/generate"


# # async def analyze_dimensions(text: str, rating: int):

# #     prompt = f"""
# #     Analyze this employee review.

# #     Extract sentiment for these dimensions:

# #     - Salary
# #     - Management
# #     - Work Culture
# #     - Work Life Balance
# #     - Career Growth
# #     - Learning Opportunities
# #     - Team
# #     - Job Security

# #     Return ONLY valid JSON.

# #     Example:

# #     {{
# #       "Salary": "Positive",
# #       "Management": "Negative"
# #     }}

# #     Review:
# #     {text}
# #     """

# #     payload = {
# #         "model": "gemma3:4b",
# #         "prompt": prompt,
# #         "stream": False,
# #         "format": "json"
# #     }

# #     try:

# #         async with aiohttp.ClientSession() as session:

# #             async with session.post(
# #                 OLLAMA_URL,
# #                 json=payload
# #             ) as resp:

# #                 data = await resp.json()

# #                 response = data.get(
# #                     "response",
# #                     "{}"
# #                 ).strip()

# #                 print("RAW LLM RESPONSE:")
# #                 print(response)

         
# #                 match = re.search(
# #                     r"\{.*\}",
# #                     response,
# #                     re.DOTALL
# #                 )

# #                 if not match:
# #                     return {}

# #                 json_text = match.group(0)

# #                 return json.loads(json_text)

# #     except Exception as e:

# #         print(
# #             "Dimension Analysis Error:",
# #             e
# #         )

# #         return {}

# import aiohttp
# import json
# import re

# OLLAMA_URL = "http://localhost:11434/api/generate"


# async def analyze_dimensions(text: str, rating):

#     try:
#         rating = int(rating)
#     except:
#         rating = 0

#     prompt = f"""
#     Analyze this employee review.

#     Overall rating: {rating}/5

#     Extract sentiment for these dimensions:

#     - Salary
#     - Management
#     - Work Culture
#     - Work Life Balance
#     - Career Growth
#     - Learning Opportunities
#     - Team
#     - Job Security

#     Return ONLY valid JSON.

#     Example:

#     {{
#       "Salary": "Positive",
#       "Management": "Negative"
#     }}

#     Review:
#     {text}
#     """

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

#                 data = await resp.json()

#                 response = data.get(
#                     "response",
#                     "{}"
#                 ).strip()

#                 print("RAW LLM RESPONSE:")
#                 print(response)

#                 match = re.search(
#                     r"\{.*\}",
#                     response,
#                     re.DOTALL
#                 )

#                 if not match:
#                     return {}

#                 json_text = match.group(0)

#                 return json.loads(json_text)

#     except Exception as e:

#         print(
#             "Dimension Analysis Error:",
#             e
#         )

#         return {}