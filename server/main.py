from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from google import genai
import time
import json
from schemas import UserInput
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=GEMINI_KEY)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def extract_key_terms(input: str):
  prompt = f"Extract up to 5 of the most important nouns, entities, and concepts from the text: {input}. Try to only return terms in the text. The returned terms should be in an array. Your response should not be anything but an array or I'll die. Do not return anything else"

  
  retries, delay = 1, 2 #Retries once after 2s

  for attempt in range(retries+1):
    try:
      res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
      terms = json.loads(res.text)
            
      if not isinstance(terms, list):
         raise ValueError(f'Gemini returning incorrect format: {terms}')
      return(terms)
    
    except Exception as e:
      if attempt == retries:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini: {str(e)}")
      time.sleep(delay)

async def context_from_wikipedia(terms: list):
  WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

  context = ''
  for term in terms:
    retries, delay = 1, 2 #Retries once after 2s

    for attempt in range(retries+1):
      try:
        res = requests.get(WIKIPEDIA_API.format(title=term))
        res = res.json()
        context += res['extract'] + ' '
        break
      
      except requests.exceptions.Timeout:
        print(f"Timeout error for {term}")
      except requests.exceptions.RequestException as e:
        print(f"Request error for {term}: {e}")
      except ValueError:
        print(f"Error parsing JSON response for {term}")
      except KeyError:
        print(f"KeyError: 'extract' field is missing for {term}")
      except Exception as e:
        print(f"Unexpected error for {term}: {e}")

      if attempt < retries:
        time.sleep(delay)
       
  return context 

def ans_from_gemini(context: str, user_input: str):
  prompt = f"Answer the user question by expanding off the given context unless the user input doesn't contain nouns, or makes no sense. Sometimes you'll not be given context. If the user input doesn't make sense or contains no nouns, or the context is empty. Ignore everything reply with your normal behavior. Provide a citation if you can. Context: {context}  User question: {user_input}"

  retries, delay = 1, 2 
  for attempt in range(retries+1):
    try:
      res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    except Exception as e:
        if attempt == retries:
          raise HTTPException(status_code=500, detail=f"Error calling Gemini: {str(e)}")
        time.sleep(delay)

  return res.text


@app.post("/")
async def reply(user_input: UserInput):  
  key_terms = extract_key_terms(user_input)
  context = context_from_wikipedia(key_terms)
  output = ans_from_gemini(context, user_input)
  
  return output

