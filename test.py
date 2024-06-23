import requests

# Replace with your FastAPI endpoint URL
API_URL = 'http://localhost:8000/check-layout/'

def upload_logo():
    # Mock logo file path and data
    logo_filename = 'logo.png'  # Replace with your logo file path
    with open(logo_filename, 'rb') as f:
        logo_data = f.read()

    # Mock form data including logo file
    data = {
        'name': 'Company Name',
        'phone': '123-456-7890',
        'address': '123 Main St, City, Country',
        'shift_id': 1,
    }
    files = {
        'logo': (logo_filename, logo_data, 'image/png')  # Adjust content type as needed
    }

    try:
        # Send POST request to the FastAPI endpoint
        response = requests.post(API_URL, data=data, files=files)

        # Check response status code
        if response.status_code == 200:
            print("Logo uploaded successfully!")
            print("Response JSON:", response.json())
        else:
            print(f"Failed to upload logo. Status code: {response.status_code}")
            print("Response content:", response.text)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    upload_logo()
