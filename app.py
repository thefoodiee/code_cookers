from flask import Flask, request, render_template
from groq import Groq
import os

app = Flask(__name__)

os.environ["GROQ_API_KEY"] = "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"
client = Groq()

def llama(prompt):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        stream=False,
        stop=None,
    )

    response = completion.choices[0].message.content.strip()
    return response

def identify_gases(gas_data):
    prompt = f"List the harmful gases from this data without any sentences: {gas_data}"
    response = llama(prompt)
    return response

def get_toxicity_levels(gases):
    prompt = f"Provide the toxicity levels for the following gases as 'low', 'medium', or 'high' without any further explanation about the gas. do not use any formal language or anything. give straight to the point answers only: {gases}"
    response = llama(prompt)
    return response

def get_neutralization(gases):
    prompt = f"Provide very short one-line 10 words solutions for neutralizing or reusing the following gases: {gases}"
    response = llama(prompt)
    return response

def removal_methods(gases):
    prompt = f"Provide 3 removal methods for the following gases. they should be one word answers only: {gases}"
    response = llama(prompt)
    return response

def alternative(gases):
    prompt = f"Provide an alternative use for each gas according to its concentration level. it should tell which industry can further use this gas as input. give only industry name in answer: {gases}"
    response = llama(prompt)
    return response

def compile_info(gas_data):
    gases = identify_gases(gas_data)
    
    toxicity = get_toxicity_levels(gases)
    
    neutralization = get_neutralization(gases)

    removal = removal_methods(gases)

    alt = alternative(gases)
    
    result = {
        "gases": gases,
        "toxicity": toxicity,
        "solutions": neutralization,
        "removal": removal,
        "alternative": alt
    }

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'show_all' in request.form:
            return render_template('all_chemicals.html', chemicals=[])
    return render_template('index.html')

@app.route('/sensor_data', methods=['GET', 'POST'])
def sensor_data():
    if request.method == 'POST':
        co = request.form.get('CO', type=int)
        no2 = request.form.get('NO2', type=int)
        so2 = request.form.get('SO2', type=int)
        
        gas_data = {
            "CO": co,
            "NO2": no2,
            "SO2": so2
        }
        
        info = compile_info(gas_data)
        return render_template('results.html', result=info)
    
    return render_template('sensor_data.html')

if __name__ == '__main__':
    app.run(debug=True)
