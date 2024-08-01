
# AI Story Generator

Welcome to the AI Story Generator! This project leverages Google GenAI to create compelling and unique stories based on user inputs. The application is built using Flask, providing a simple and intuitive web interface for users to interact with the AI.


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
## Introduction

The AI Story Generator is a web application that allows users to generate stories in various genres, including horror, detective, thrill, and romcom. By leveraging Google GenAI, the application can produce high-quality, coherent narratives based on user-provided prompts and parameters.
## Features

- Multi-genre Support: Generate stories in multiple genres such as horror, detective, thrill, and romcom.
- User Inputs: Customize story generation with specific prompts and parameters.
- Responsive Design: A user-friendly web interface built with Flask and Bootstrap.
- Scalable: Easily deployable on various platforms, including local servers and cloud environments.

## Installation

### Prerequisites

- Python 3.8+
- Virtual env

### Clone the Repository

```bash
git clone https://github.com/yourusername/ai-story-generator.git
cd ai-story-generator 
```

### Clone the Repository
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and add your Google GenAI API key:

```env
GOOGLE_API_KEY=your_google_genai_api_key
FLASK_ENV=development
```
### Running the Application

```bash
flask run
```
Open your web browser and navigate to http://127.0.0.1:5000 to access the AI Story Generator.

## Generating a Story
- Choose a genre (Horror, Detective, Romcom).
- Enter a prompt or a few keywords.
- Click "Generate Story."
- Enjoy your AI-generated story!
    ## API Endpoints

### `POST /generate`

Generate a story based on user inputs.

- **URL:** `/generate`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "genre": "horror",
    "prompt": "A dark and stormy night"
  }

### `GET /`

The main web interface for the AI Story Generator.
## Contributing

Contributions are always welcome!

We welcome contributions to enhance the AI Story Generator. To contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/your-feature).
- Create a new Pull Request.


## License

[MIT](https://choosealicense.com/licenses/mit/)

