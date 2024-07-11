from flask import Flask, request, jsonify, render_template, redirect, url_for, session
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.form
    genre = data.get('genre')
    story_type = data.get('story_type')
    word_count = data.get('word_count')
    age_group = data.get('age_group')

    if not all([genre, story_type, word_count, age_group]):
        return jsonify({'error': 'All fields are required'}), 400

    model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config={"temperature": 0.7})
    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = (
    f"Generate a {story_type} story in the {genre} genre with {word_count} words for the {age_group} age group. "
    "Ensure the story is suitable for that age group, avoiding explicit language, hate speech, or offensive content."
)


    character_count = 0
    for key, value in data.items():
        if key.startswith('gender_character_'):
            character_count += 1
            gender = value
            description = data.get(f'description_character_{character_count}', '')
            prompt += f" Character {character_count}: {gender}, {description},"

    prompt += (
        f" Make sure the story is engaging and follows a coherent plot."
    )

    response = chat.send_message(prompt)
    result = response.candidates[0].content.parts[0].text

    session['story'] = result
    return redirect(url_for(f'show_{genre.lower()}'))

@app.route('/show_horror')
def show_horror():
    story = session.get('story', 'No story generated yet.')
    return render_template('horror.html', story=story)

@app.route('/show_romcom')
def show_romcom():
    story = session.get('story', 'No story generated yet.')
    return render_template('romcom.html', story=story)

@app.route('/show_thrill')
def show_thrill():
    story = session.get('story', 'No story generated yet.')
    return render_template('thrill.html', story=story)

@app.route('/show_detective')
def show_detective():
    story = session.get('story', 'No story generated yet.')
    return render_template('detective.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)
