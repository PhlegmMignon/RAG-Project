# RAG-Project-Darren-Mah

Live link: https://rag-project-1.onrender.com/

May take a little while to load since I'm using free hosting.
Also, please note I'm aware the .env file is pushed. It's late and I don't want to risk breaking my deployments by making a gitignore and fixing the issue.
## How to run locally

1. Clone repository
2. Navigate to `/server`. Optionally, make a virtual envirnoment.
3. `pip install requirements.txt`
4. `uvicorn main:app --reload` to host backend
5. Navigate to `/client` and run `npm i`
6. `npm run dev` to host frontend

You'll need to create a .env and get a Gemini Api key to declare GEMINI_KEY for the backend to work

## Dependencies

Relies on Gemini to parse key terms from user input.
Relies on wikipedia to gather context from key terms.
Relies on Gemini to process context and user input to generate a reply.

## Overview

I've set out with the goal of creating a general all purpose answer machine that should handle a variety of responses well. However, there are significant problems such as the Gemini api failing when called too often and inconsistent answers given the same user input.

## Challenges

- I had trouble finding a unique direction to take this project. With the time constraints, I just went with the basic implementation.
- Fine tuning the prompt to cover a wider range of responses is tricky and hasn't been perfected yet
- Gathering knowledge on how the Wikipedia and Gemini APIs work

## Some features I would've liked to add

Backend

- Include 2nd knowledge source when context gathering fails for the first one. Comparing context as well
- Solutions to Gemini being called too often
- Fine tuning prompts to handle more low context inputs
- Add test files

Frontend

- Better text formatting for AI reply
- Scrollbar adjustments
- Optional featuers listed in assignment description
