# Resume Screener

A web-based application that automatically matches candidate resumes against job descriptions using Natural Language Processing (NLP) techniques. This tool helps recruiters and hiring managers quickly identify the most suitable candidates by analyzing both keyword matches and semantic similarity.

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

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-screener.git
   cd resume-screener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Start the application:
   ```bash
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
├── uploads/                  # Directory for uploaded files
├── requirements.txt          # Python dependencies
└── test_upload.py           # Test script
```

## Algorithm Details

The matching algorithm uses a combination of keyword matching and semantic similarity:

1. **Keyword Matching (50% of final score)**:
   - Extracts lemmatized keywords from both job description and resume
   - Calculates the percentage of job description keywords found in the resume
   - Handles variations of words (e.g., "programming" and "programmer")

2. **Semantic Similarity (50% of final score)**:
   - Uses spaCy's document similarity to measure contextual similarity
   - Considers the overall meaning and context of the text
   - Helps identify candidates with relevant experience even if exact keywords don't match

## Testing

You can test the application using the provided test script:

```bash
python test_upload.py
```

This will upload sample job description and resume files and verify the application's functionality.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
