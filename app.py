from flask import Flask, request, render_template
import joblib

# Load the saved model and vectorizer
model = joblib.load('spam_model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

# Initialize Flask app
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')  # HTML for input form

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get input email text
    email_text = request.form.get('email_text', '')
    
    # Check if input is provided
    if not email_text:
        return render_template('index.html', error="Please enter email text to analyze.")
    
    # Preprocess and predict
    processed_text = [" ".join(email_text.lower().split())]  # Preprocess input
    input_vectorized = tfidf.transform(processed_text)
    prediction = model.predict(input_vectorized)[0]
    
    # Result
    if prediction == 1:
        result = "This email is classified as SPAM."
    else:
        result = "This email is NOT SPAM."
    
    return render_template('index.html', result=result, email_text=email_text)

if __name__ == '__main__':
    app.run(debug=True)
