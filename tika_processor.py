import tika
from tika import parser as tika_parser
import argparse
import os


def find_available_filename(filename):
    base_name, extension = os.path.splitext(filename)
    extension = extension.lstrip(".")  # Remove leading period from extension
    counter = 1
    new_filename = f"{base_name}_{extension}_extract.txt"

    while os.path.exists(new_filename):
        new_filename = f"{base_name}_{extension}_extract_{counter}.txt"
        counter += 1
    return new_filename


def extract_and_save_text(input_file):
    # Specify OCR language
    headers = {
        "X-Tika-OCRLanguage": "eng+rus"
    }

    try:
        # Parse the file with Tika
        parsed = tika_parser.from_file(input_file, headers=headers, serverEndpoint='http://localhost:9998')

        # Extract text content
        text_content = parsed['content']

        if text_content is not None:
            # Remove leading empty lines
            text_lines = text_content.split('\n')
            non_empty_lines = [line for line in text_lines if line.strip()]
            cleaned_text = '\n'.join(non_empty_lines)

            # Get the folder and filename
            folder, filename = os.path.split(input_file)
            extracted_filename = find_available_filename(filename)

            # Create and write cleaned text to the new file
            with open(os.path.join(folder, extracted_filename), "w") as f:
                f.write(cleaned_text)

            print(f"Text extracted and saved to: {extracted_filename}")
        else:
            print("Tika failed to extract text content from the file.")
    except Exception as e:
        print(f"Error during extraction: {e}")


if __name__ == "__main__":
    tika.initVM()

    arg_parser = argparse.ArgumentParser(description="Extract text from a file using Tika")
    arg_parser.add_argument("input_file", help="Path to the input file")
    args = arg_parser.parse_args()

    extract_and_save_text(args.input_file)
