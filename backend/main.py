from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)
CORS(app)

template = """ 
You are a compassionate, friendly, short-spoken, charming, supportive, and non-judgmental personal therapist.

Your goal is to help the user express themselves, feel understood, and gently offer insights or questions that can help them reflect and grow.

here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

context = ""

@app.route("/chat", methods=["POST"])

def chat():
    global context
    data = request.json
    user_input = data.get("message", "")
    result = chain.invoke({"context": context, "question": user_input})
    context += f"You: {user_input}\nTherapist: {result}\n"
    print("BOT RESPONSE:", result)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)

