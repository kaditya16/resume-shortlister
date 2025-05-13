# Resume Shortlisting Application

A web-based application that matches candidate resumes against job descriptions using Natural Language Processing (NLP) techniques.

## Features

- Upload job descriptions in PDF, DOCX, or plain text format
- Upload multiple candidate resumes (PDF or DOCX)
- Extract text from documents using pdfplumber and docx2txt
- Perform keyword extraction using spaCy NLP
- Calculate match scores based on:
  - Keyword overlap between job description and resumes
  - Semantic similarity using spaCy's document similarity
- Shortlist candidates with match scores above 70%
- Display detailed match results with visualizations

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, Bootstrap CSS, JavaScript
- **NLP**: spaCy with en_core_web_sm model
- **Document Processing**: pdfplumber, docx2txt

## How to Use

1. Start the application:
   ```
   python main.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. On the main page:
   - Enter a job title
   - Upload a job description file (PDF, DOCX, or TXT)
   - Upload one or more resume files (PDF or DOCX)
   - Click "Compare and Shortlist"

4. View the results:
   - A list of all resumes ranked by match score
   - Detailed analysis for each resume
   - Shortlisted candidates (match score ≥ 70%)

## API Endpoints

- `GET /`: Main upload form
- `POST /upload/`: Process uploaded files and display results
- `GET /health`: Health check endpoint (returns `{"status": "healthy"}`)

## Project Structure

```
├── main.py                   # FastAPI application
├── utils/
│   ├── matching.py           # Matching logic & score calculation
│   └── parsing.py            # Text extraction from documents
├── templates/
│   ├── index.html            # Upload form template
│   └── results.html          # Results display template
└── uploads/                  # Directory for uploaded files
```

## Algorithm Details

- **Keyword Matching**: Extracts lemmatized keywords from both job description and resume, then calculates the percentage of job description keywords found in the resume.
- **Semantic Similarity**: Uses spaCy's document similarity to measure the contextual similarity between the job description and resume.
- **Final Score**: Weighted average of keyword match (50%) and semantic similarity (50%).

## Testing

You can test the application using the provided test files:

```python
python test_upload.py
```

This will upload sample job description and resume files and verify the application's functionality.