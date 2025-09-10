from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import asyncio

base_url = "https://openrouter.ai/api/v1/chat/completions"

# Create your views here.
@csrf_exempt
async def optimize_prompt(request):
    if request.method == 'POST':

        user_prompt = request.POST.get("user_prompt", None)

        request = await asyncio.to_thread(requests.post, url=base_url, 
                  headers={
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/x-www-form-urlencoded"
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

            return JsonResponse(clean_json, status = 200)
        
        else:

            return JsonResponse({

                "Message" : "Error"
            }, status = 400)


