# FilmFinder

## Overview
FilmFinder is a mood-based movie recommendation web application that enhances traditional recommendation systems by incorporating user moods to generate more relevant movie suggestions. The project explores how mood influences recommendation accuracy and user engagement.

## Features
- Personalized movie recommendations based on user-selected mood.
- Flask-based backend with JavaScript-based frontend.
- Data processing and recommendation generation using Python.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python (Flask)
- **Database**: SQLite (or any other configured DB)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/filmfinder.git
   cd filmfinder
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables
   ```sh
   export FLASK_APP=app.py
   ```
5. Run the application:
   ```sh
   flask run
   ```
6. Access the app at `http://127.0.0.1:5000/`.

## Usage
1. Create an account for recommendation functionality
2. Select a mood from the available options.
3. Receive a list of recommended movies based on the selected mood.

## Future Improvements
- Integration with streaming service links.
- Custom weighting for mood influence.
- Sorting and filtering options for recommendations.

## License
This project is licensed under the MIT License.

