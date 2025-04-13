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
 

@app.get("/")
async def read_root():
  key_terms = extract_key_terms('.')
  context = context_from_wikipedia(key_terms)

  
  return context


  # return text

@app.get('/wiki')
async def get_wiki(query: str):
    



    WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    url = f"{WIKI_API}{query}"
  
    try:
      res = requests.get(url)
      res.raise_for_status()
      data = res.json()

      if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"]["info"])
      
      search_results = data.get("query", {}).get("search", [])
      if search_results:
          result = search_results[0]
          return {
              "title": result["title"],
              "snippet": result["snippet"],
              "url": f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}"
          }
      else:
          return {"message": "No results found."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error contacting Wikipedia API: {e}"}
    