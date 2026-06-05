
#Email processing based on AI and response from them 


#Prerequisites

- Python 3.10+
- Ollama installed locally (https://ollama.com)
- LLaMA 3.2 model pulled: `ollama pull llama3.2`

#Intallation guide

1. Create a virtual environment:
  python -m venv venv


2. Activate the virtual environment:
  .\venv\Scripts\Activate.ps1
   

3. Install dependencies:
  pip install -r requirements.txt


#Run to  the application 
4. Main Entry point:
python main.py 

5. Local Host web server http://localhost:8000/docs

# To test the workflow
python tests/test_workflow.py


## Project Structure

project/
├── agents/          
├── apis/            
├── models/          
├── prompts/         
├── workflows/       
├── utils/           
├── tests/           
├── config/          
├── logs/            
├── main.py  
|──README.md        
└── requirements.txt


