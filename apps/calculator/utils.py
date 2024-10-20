import google.generativeai as ai
import ast
import json
from PIL import Image
from constants import GEMINI_API_KEY


ai.configure(api_key=GEMINI_API_KEY)

model = ai.GenerativeModel(model_name="gemini-1.5-flash")

def process_image(img: Image, dict_of_vars:dict):
    dict_of_vars_to_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
    "You are given an image containing mathematical expressions, equations, or graphical problems. "
    "Solve them following the PEMDAS rule: Parentheses, Exponents, Multiplication/Division (left to right), "
    "and Addition/Subtraction (left to right). "
    "Example: "
    "Q1. 2 + 3 * 4 => (3 * 4) = 12; 2 + 12 = 14. "
    "Q2. 2 + 3 + 5 * 4 - 8 / 2 => (5 * 4) = 20; (8 / 2) = 4; (2 + 3) = 5; 5 + 20 = 25; 25 - 4 = 21. "
    "There are five types of problems in the image. Only one case will apply each time: "
    
    "1. **Simple Mathematical Expressions:** Solve expressions like 2 + 2, 3 * 4, etc. "
    "Return a LIST with one DICT: [{'expr': 'given expression', 'result': calculated_answer}]. "
    
    "2. **Set of Equations:** Solve for variables in equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, etc. "
    "Return a COMMA SEPARATED LIST of DICTS, one for each variable: [{'expr': 'x', 'result': value, 'assign': True}]. "
    
    "3. **Variable Assignments:** Handle assignments like x = 4, y = 5, etc. "
    "Return a LIST of DICTS: [{'expr': 'x', 'result': 4, 'assign': True}]. "
    
    "4. **Graphical Math Problems:** Solve word problems based on drawings, such as trigonometry, collisions, etc. "
    "Return a LIST with one DICT: [{'expr': 'given problem', 'result': calculated answer}]. "
    
    "5. **Abstract Concept Detection:** Identify abstract ideas from drawings (e.g., love, patriotism). "
    "Return a LIST with one DICT: [{'expr': 'explanation', 'result': 'abstract concept'}]. "
    
    "Use the following dictionary of user-assigned variables if any appear in the expression: {dict_of_vars_str}. "
    "Escape characters like \\f and \\n should be written as \\\\f and \\\\n. "
    "DO NOT USE backticks or Markdown formatting. "
    "Ensure all dictionary keys and values are properly quoted for easy parsing with Python's ast.literal_eval."
    )

    response = model.generate_content([prompt, img])

    print(response.text)

    answers = []

    try:
        answers = ast.literal_eval(response.text)
    except Exception as error:
        print(f"Sorry andi..!, ERROR {error}")

    print("answers: ", answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers



