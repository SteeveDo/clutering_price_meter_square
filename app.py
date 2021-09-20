#imports
from flask import Flask, render_template, session, request, flash, redirect
from score_data import predict


token = 0

app = Flask(__name__)
#flask app secret code
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#initialisation of the first route (home page)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#route which actives the prediction
@app.route('/api', methods=['GET', 'POST'])
def inference():
    """Function to realize the prediction on selected files.

    Args:
        None

    Returns:
        json file: predictions contained in the json file

    """
    if request.method == 'POST':
        #get back the text
        text = request.form['adress']
    
        #check if the text is no empty and realize prediction by calling the model (function predict imported)
        if text == '':
            flash('Enter a valid adress', 'error')
            return redirect('/')

        if not isinstance(text, str):
            flash('Enter a valid adress', 'error')
            return redirect('/')

        if text != '':
            pred, min, max = predict(text)
            session['pred'] = pred
            session['scoremin'] = min
            session['scoremax'] = max
            return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session['pred'] = 0
    session['scoremin'] = 0
    session['scoremax'] = 0
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)