import pandas as pd
from fuzzywuzzy import process
from flask import Flask, request, render_template

app = Flask(__name__)
df = pd.read_csv("data.csv")


def search_chem(chemical_name, df):
    chemicals = df['chemical'].tolist()
    closest_match, score = process.extractOne(chemical_name, chemicals)
    
    if score > 80:
        result = df[df['chemical'].str.lower() == closest_match.lower()]
        result_dict = result.to_dict(orient='records')[0]  
        print(result_dict)
        return result_dict
    else:
        return {"error": "No close match found for the provided chemical name."}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search' in request.form:
            chemical_name = request.form.get('chemical_name')
            result = search_chem(chemical_name, df)
            return render_template('result.html', result=result)
        elif 'show_all' in request.form:
            sorted_chemicals = sorted(df['chemical'].tolist())
            return render_template('all_chemicals.html', chemicals=sorted_chemicals)
    return render_template('index.html')

@app.route('/chemical/<name>', methods=['GET'])
def chemical_details(name):
    result = search_chem(name, df)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)