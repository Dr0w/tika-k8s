from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    tika_response = parse_with_tika(file)
    return render_template('results.html', result=tika_response)


def parse_with_tika(file):
    tika_url = 'http://localhost:9998/tika'
    files = {'file': (file.filename, file.stream)}
    headers = {'Accept': 'text/xml'}
    response = requests.put(tika_url, files=files, headers=headers)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.content)
        # Extract information from the XML as needed
        # For example, extracting text content:
        text_content = root.find('.//{http://www.w3.org/1999/xhtml}body').text
        return text_content
    else:
        # Handle error cases
        return f"Error: {response.status_code}, {response.text}"


if __name__ == '__main__':
    app.run(debug=True)
