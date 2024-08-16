# AI-Interview-Prepper-Prepr-

## Description
This project is a comprehensive system designed to conduct and analyze interviews using a combination of computer vision, natural language processing (NLP), and audio analysis. It simulates an interview process, offering feedback on eye contact, keyword usage, and filler words to help users improve their interview skills. Some key components include: a specch translation model for audio input, eye tracking software for facial detection, and a behavioral analysis at the end of the interview session. Additionally, the trained Open AI model selects prompts based on responses.

## Getting Started
### Installation

To set up this project on your local machine, follow these steps:

### Prerequisites

  1. Python
  Ensure you have Python installed on your system. The recommended version is Python 3.7 or higher.
### Dependencies

  2. Required Python Libraries
  Install the necessary Python libraries using pip. You can do this by running the following commands in your terminal or command prompt:
  pip install numpy
  pip install mediapipe
  pip install Flask
  pip install openai
  pip install opencv-python
  pip install multiprocessing
  pip install SpeechRecognition
  pip install gtts
  pip install playsound
  pip install flask-cors
  pip install whisper
You can install these dependencies using `pip`. To do this, first make sure you have `pip` installed and then run:

### Executing program

* Clone the repository: git clone https://github.com/yourusername/your-repo-name.git
* Navigate to the project directory: cd your-repo-name
* Install dependencies: pip install -r requirements.txt
* Create a config.py file in the root directory with your bot's token:
* To use OpenAI's GPT model, you'll need an API key. You can obtain one by signing up on the OpenAI website. Store the API key securely (the script assumes it’s stored in a module named secretkey.py).
* Start the Flask server and the interview process by running the main script. The application will launch, and you can interact with it via the provided API endpoints.

## Authors

Contributors names and contact info

Mohit Darla - darlamohit@gmail.com
