from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class UserStoryInput(BaseModel):
    user_story: str

def generate_test_cases(user_story):
    prompt = f"Generate functional test cases for the following user story:\n\n{user_story}"

    # Run LLaMA 3 model using Ollama
    command = f'ollama run llama3 "{prompt}"'
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        return {"error": "Failed to generate test cases", "details": result.stderr}
    
    return {"test_cases": result.stdout.strip()}  # Return the cleaned output

@app.post("/generate_test_cases/")
def get_test_cases(input_data: UserStoryInput):
    return generate_test_cases(input_data.user_story)
