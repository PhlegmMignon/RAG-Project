# RAG-Project

User input

Get wikipedia + SerpAPI

Send results to gemini + query. 'Get the information from the 2 results that best answers the question'

Test cases:
What is x
X may be ambiguous, like apple
Solve math
Empty input

Extras:
Images
Citation
Suggest related query
Multi turn query

Included SerpAPI as failsafe in case of nonexistant/fake wiki article
Tell AI to detect which is false if doesn't align
Tell AI to detect if it needs to prompt user for more clarify if sources conflict

User -> my code -> send query to Gemini

Test:
What's 2+2
Difference between sun and moon
MLK
What caused World War II and how did it end

Frontend filters empty inputs and too long strings
