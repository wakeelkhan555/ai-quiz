import os
import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuizRequest(BaseModel):
    question: str
    user_answer: str


# Load questions from JSON
with open("question.json", "r") as file:
    questions = json.load(file)


def generate_fun_fact(question):
    prompt = f"""
    You are a friendly educational AI tutor.

    Quiz question: {question}

    Your task:
    - Generate one interesting educational fun fact related to the question.
    - Use exactly 2 short sentences.
    - Use simple English that a student can understand.
    - Keep the total response under 50 words.
    - Avoid unnecessary introductions like "Did you know?"
    - Do not repeat the quiz question.
    - Avoid unsupported claims.
    - Return only the fun fact.

    Fun fact:
    """

    try:
        response = requests.post(
    os.getenv("OLLAMA_URL", "http://localhost:11434")
    + "/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"].strip()

    except requests.RequestException:
        return "The fun fact is temporarily unavailable."


# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/questions")
def get_questions():
    return questions


@app.post("/check-answer")
def check_answer(data: QuizRequest):

    for question in questions:

        if question["question"] == data.question:

            correct_answer = question["options"][question["answer"] - 1]

            is_correct = (
                data.user_answer.strip().lower()
                == correct_answer.strip().lower()
            )

            if is_correct:
                explanation = f"{correct_answer} is correct!"
            else:
                explanation = f"The correct answer is {correct_answer}."

            # Ask the local AI to generate a fun fact
            fun_fact = generate_fun_fact(data.question)

            return {
                "correct": is_correct,
                "score": 1 if is_correct else 0,
                "explanation": explanation,
                "fun_fact": fun_fact
            }

    return {
        "correct": False,
        "score": 0,
        "explanation": "Question not found.",
        "fun_fact": ""
    }