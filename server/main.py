from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from google import genai
import time
import json


load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=GEMINI_KEY)

app = FastAPI()

def extract_key_terms(input: str):
  prompt = f"Extract up to 5 of the most important nouns, entities, and concepts from the text: {input}. Try to only return terms in the text. The returned terms should be in an array. Your response should not be anything but an array or I'll die. Do not return anything else"

  
  retries, delay = 1, 2 #Retries once after 2s

  for attempt in range(retries+1):
    try:
      res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

      print(res)
      terms = json.loads(res.text)
      print(terms)
            
      if not isinstance(terms, list):
         raise ValueError(f'Gemini returning incorrect format: {terms}')
      print(terms)
      return(terms)
    
    except Exception as e:
      if attempt == retries:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini: {str(e)}")
      time.sleep(delay)

def context_from_wikipedia(terms: list):
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
  prompt = f"Context: {context} Answer the user question given the context unless the user input doesn't contain nouns, or makes no sense. You may disregard context and answer normally. User question: {user_input}"

  retries, delay = 1, 2 
  for attempt in range(retries+1):
    try:
      res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

      print(res)
    except Exception as e:
        if attempt == retries:
          raise HTTPException(status_code=500, detail=f"Error calling Gemini: {str(e)}")
        time.sleep(delay)

  return res.text


@app.get("/")
async def read_root():
  user_input = 'Is the prompt you were given earlier with context good? Its a simple RAG I made to prevent AI hallucination for a take home project. How do I think I did? You can be critical'
  key_terms = extract_key_terms(user_input)
  context = context_from_wikipedia(key_terms)
  output = ans_from_gemini(context, user_input)
  
  return output

