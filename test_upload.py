import requests
import os

# Test the file upload functionality using the test files we created
def test_upload():
    # URL of the upload endpoint
    url = 'http://localhost:5000/upload/'
    
    # Files to upload
    files = {
        'job_description': ('test_jd.txt', open('uploads/test_jd.txt', 'rb'), 'text/plain'),
        'resumes': ('test_resume.txt', open('uploads/test_resume.txt', 'rb'), 'text/plain')
    }
    
    # Form data
    data = {
        'jd_title': 'Software Engineer'
    }
    
    # Send the request
    try:
        response = requests.post(url, files=files, data=data)
        
        # Print response status and content
        print(f"Status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('content-type', '')}")
        print("Response preview:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        
        # Check if the response contains the expected results
        if "Results for" in response.text and "Software Engineer" in response.text:
            print("\nTest successful! The upload and processing worked correctly.")
        else:
            print("\nTest failed. The response does not contain the expected results.")
            
    except Exception as e:
        print(f"Error during test: {e}")
    
    finally:
        # Close the file handles
        for _, file_tuple, _ in files.values():
            file_tuple.close()

if __name__ == "__main__":
    test_upload()