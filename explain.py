import os
import json
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini with the API Key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_api(prompt: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return ""

def generate_disease_explanation(disease_name: str) -> dict:
    """
    Generate detailed agricultural and treatment recommendations for the predicted disease.
    """
    
    if GEMINI_API_KEY:
        prompt = f'''
        You are an expert agricultural scientist. Provide a highly detailed, comprehensive, and structured analysis 
        for the plant status: "{disease_name}".
        
        CRITICAL INSTRUCTION: If "{disease_name}" indicates that the plant is HEALTHY (e.g., contains the word "healthy"):
        - Write a positive description about the healthy plant.
        - Set ALL arrays (symptoms, causes, chemical, organic, prevention) strictly to ["N/A"].
        - Set ALL strings in the timeline and application_notes strictly to "N/A".
        
        Provide the response strictly in valid JSON format (without markdown block ticks) with the following schema:
        {{
            "disease": (string),
            "description": (string),
            "symptoms": (array of strings),
            "causes": (array of strings),
            "treatment": {{
                "chemical": (array of strings),
                "organic": (array of strings),
                "application_notes": (string)
            }},
            "prevention": (array of strings),
            "timeline": {{
                "day_1_2": (string),
                "day_5_7": (string),
                "ongoing": (string)
            }}
        }}
        Ensure the JSON is strictly valid, with no unescaped quotes inside values or trailing commas.
        Keep the tone informative and highly detailed for an expert farmer.
        '''
        
        try:
            models_to_try = ['gemini-flash-latest', 'gemini-1.5-flash-latest', 'gemini-pro']
            response = None
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                    if response and response.text:
                        print(f"Successfully used model: {model_name}")
                        break
                except Exception as model_e:
                    print(f"Model {model_name} failed: {model_e}")
                    continue
            
            if response and response.text:
                text = response.text.strip()
                if text.startswith('```json'): text = text[7:]
                if text.startswith('```'): text = text[3:]
                if text.endswith('```'): text = text[:-3]
                return json.loads(text.strip())
        except Exception as e:
            print(f"Failed to generate or parse Gemini response as JSON: {e}")
            pass

    # Simplified default advice placeholder fallback if API fails or is not set
    return {
        "disease": disease_name,
        "description": "Information could not be loaded due to an API error or missing key.",
        "symptoms": ["N/A"],
        "causes": ["N/A"],
        "treatment": {
            "chemical": ["Apply a broad-spectrum copper hydroxide fungicide (Fallback)."],
            "organic": ["Spray organic neem oil (1-2% concentration) (Fallback)."],
            "application_notes": "Apply thoroughly on leaf surfaces."
        },
        "prevention": ["Ensure proper crop rotation and spacing."],
        "timeline": {
            "day_1_2": "Remove infected leaves.",
            "day_5_7": "Monitor for spread.",
            "ongoing": "Expected recovery in 10-14 days."
        }
    }

def chat_with_gemini(message: str, history: list, disease_name: str) -> str:
    """
    Continues the conversation about the diagnosed disease using Gemini Chat.
    """
    if not GEMINI_API_KEY:
        return "Sorry, the Agri-Chat feature is currently offline (API key missing)."
        
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Convert frontend history format to Gemini format
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["text"]]})
            
        chat_session = model.start_chat(history=formatted_history)
        
        # Add system context if this is the first real question
        if not history:
            context_prompt = f"Act as an expert agricultural assistant. The user just uploaded a leaf diagnosed with '{disease_name}'. Answer their following question concisely and helpfully. IMPORTANT: Always reply in the exact same language that the user uses to ask their question: {message}"
            response = chat_session.send_message(context_prompt)
        else:
            response = chat_session.send_message(message)
            
        return response.text
    except Exception as e:
        print(f"Gemini Chat API call failed: {e}")
        return "I encountered an error while processing your message. Please try again."
