import os 
import json

def compare_json_files(folder_path):
    # Dictionary to store content based on specified keys
    content_dict = {}
    # List to store files to be removed
    files_to_remove = []

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract relevant content from the file
                content_key = (data['Body']['Absender'], 
                               data['Body']['Name des Kindes'], 
                               data['Body']['Geburtsdatum des Kindes'], 
                               data['Body']['Schwimmabzeichen'])

                # Check if content exists
                if content_key in content_dict:
                    # If content is duplicated, add file to remove list
                    files_to_remove.append(filename)
                else:
                    # Otherwise, store content
                    content_dict[content_key] = file_path

    # Iterate over files to remove
    for filename in files_to_remove:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Check if 'To' key contains specific value
            if 'js@hilden.dlrg.de' in data['To']:
                # If yes, remove the file
                os.remove(file_path)

# Example usage
folder_path = f"{os.path.dirname(os.path.realpath(__file__))}/registration_mails/"
compare_json_files(folder_path)