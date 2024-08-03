from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load environment variables
load_dotenv()

# Configure the Google Generative AI model
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key is None:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable.")

genai.configure(api_key=google_api_key)

# Mock user database
users = {}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (replace with your own logic)
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials.')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Simple user creation (replace with your own logic)
        if username not in users:
            users[username] = password
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('signup.html', error='Username already exists.')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = request.form
    genre = data.get('genre')
    story_type = data.get('story_type')
    word_count = data.get('word_count')
    age_group = data.get('age_group')
    language = data.get('language', 'English')  # Default to English if not provided
    author_likelihood = data.get('author_likelihood', '')  # Optional field

    if not all([genre, story_type, word_count, age_group]):
        return jsonify({'error': 'All fields except author likelihood and language are required'}), 400

    model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config={"temperature": 0.5})
    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = (
        f"Generate a {story_type} story in the {genre} genre with {word_count} words for the {age_group} age group. "
        f"Ensure the story is suitable for that age group, avoiding explicit language, hate speech, or offensive content. "
        f"The story should be in {language}. "
    )
    
    if author_likelihood:
        prompt += f"Reflect an author likelihood of {author_likelihood}. "

    prompt += (
        "In case of romcom, make sure it is very safe and the story is suitable for that age group, avoiding sexually explicit language, hate speech, or offensive content. "
        "Avoid any references to sexual activity, violence, harassment, or other inappropriate content. "
        "Ensure that the story promotes positive values and respectful interactions."
    )

    character_count = 0
    for key, value in data.items():
        if key.startswith('gender_character_'):
            character_count += 1
            gender = value
            description = data.get(f'description_character_{character_count}', '')
            prompt += f" Character {character_count}: {gender}, {description},"

    prompt += " Make sure the story is engaging and follows a coherent plot."

    try:
        response = chat.send_message(prompt)
        result = response.candidates[0].content.parts[0].text
        session['story'] = result
    except genai.types.generation_types.StopCandidateException as e:
        result = "The generated story was flagged for safety concerns and could not be completed. Please try again with different parameters."
        session['story'] = result

    return redirect(url_for(f'show_{genre.lower()}'))

@app.route('/show_horror')
def show_horror():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    story = session.get('story', 'No story generated yet.')
    return render_template('horror.html', story=story)

@app.route('/show_romcom')
def show_romcom():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    story = session.get('story', 'No story generated yet.')
    return render_template('romcom.html', story=story)

@app.route('/show_thrill')
def show_thrill():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    story = session.get('story', 'No story generated yet.')
    return render_template('thrill.html', story=story)

@app.route('/show_detective')
def show_detective():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    story = session.get('story', 'No story generated yet.')
    return render_template('detective.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)
