from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from authentication.views import SESSION
import requests
import json
import asyncio
from functools import wraps

def check_session(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):

        cookie = request.COOKIES.get('session_id', None)
        
        if cookie in SESSION:

            return await func(request, *args, **kwargs)
        
        else:
            
            return JsonResponse({

                "message": "You need to login first"
            }, status = 401)
    
    return wrapper

# Create your views here.
@csrf_exempt
@check_session
async def optimize_prompt(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        user_prompt = data.get("user_prompt", None)

        if not user_prompt or user_prompt == None:
            return JsonResponse({"message": "Invalid prompt"}, status = 300)

        try:

            request = await asyncio.to_thread(requests.post, url=config("BASE_URL"), 
                    headers={
                        "Authorization": f"Bearer {config("API_KEY")}",
                        "Content-Type": "application/json"
                    },data=json.dumps({
                            "model": "nvidia/nemotron-nano-9b-v2:free",
                            "messages": [
                            {
                                "role": "system",
                                "content": """You are a professional prompt optimization assistant. Your role is to take any user’s raw prompt and refine it into a clear, effective, and structured prompt. When optimizing, always ensure the instructions are explicit and unambiguous, provide sufficient context, and adopt a suitable persona if necessary to improve consistency and tone. If the user’s prompt is too broad, narrow its scope to make it more focused and actionable. When appropriate, reframe the prompt to include a specific format request such as a summary, a list, or a table so that the answer will be structured and easy to interpret. Avoid over-leading the response so that the model retains flexibility to reason properly. If the user’s input is complex, make the optimized version concise yet comprehensive enough to handle the task effectively. Always output the result strictly in JSON format as follows: {"users_prompt": "<original prompt here>", "optimize_prompt": "<optimized prompt here>"}. Do not include any extra text or explanations outside of this JSON structure.
                                Below are examples you must follow when optimizing:
                                {"users_prompt": "Tell me about WW2.", "optimize_prompt": "Act as a history professor and provide a concise summary of the key causes, major events, and outcomes of World War II in no more than 300 words, structured into three sections: causes, events, and outcomes."}
                                {"users_prompt": "Write me a poem.", "optimize_prompt": "Write a four-line rhyming poem in a lighthearted tone about the joy of drinking coffee in the morning."}
                                {"users_prompt": "Explain AI.", "optimize_prompt": "Act as a computer science teacher and explain artificial intelligence in simple terms suitable for a beginner, using short paragraphs and one real-world example."}
                                {"users_prompt": "Make me a diet plan.", "optimize_prompt": "Act as a certified nutritionist and create a 7-day balanced diet plan for a healthy adult, including breakfast, lunch, dinner, and snacks, presented in a table format with calorie estimates."}
                                {"users_prompt": "Code me a login system.", "optimize_prompt": "Act as a senior backend engineer and write a secure Python Flask login system with JWT-based authentication, input validation, and password hashing using bcrypt. Provide code with comments for clarity."}
                                {"users_prompt": "Summarize this article.", "optimize_prompt": "Summarize the given article in under 200 words, highlighting the main argument, three key supporting points, and the conclusion. Present the summary in paragraph form without direct quotes."}
                                {"users_prompt": "Teach me Spanish.", "optimize_prompt": "Act as a Spanish language tutor and create a beginner-friendly lesson covering common greetings, introductions, and polite expressions. Include example sentences and English translations."}
                                {"users_prompt": "Help me write a business email.", "optimize_prompt": "Write a professional business email to a potential client introducing a new software product. Use a polite, persuasive tone, and include a clear call to action at the end."}
                                """
                            },
                            {
                                "role": "user",
                                "content": user_prompt
                            }
                            ],
                        }),
                        )
            
            if(request.status_code == 200):
                
                result = request.json()

                result_raw = result["choices"][0]["message"]["content"]

                clean_json = json.loads(result_raw)

                response = JsonResponse(clean_json, status = 200)

                return response
            
            else:

                return JsonResponse({

                    "Status Code": request.status_code,
                    "Message": request.text
                }, status = int(request.status_code))

        except Exception as e:

            response = JsonResponse({

                "Message": f"{e}"
            })

            return response

