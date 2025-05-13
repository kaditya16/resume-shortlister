import spacy
from collections import Counter
from typing import List, Tuple, Set, Dict
import numpy as np

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model not found (for development environment)
    import sys
    print("SpaCy model not found. Please download it using: python -m spacy download en_core_web_sm")
    sys.exit(1)

def extract_keywords(text: str) -> Set[str]:
    """
    Extract important keywords from text using spaCy.
    
    Args:
        text: Input text
        
    Returns:
        Set of lemmatized keywords
    """
    doc = nlp(text.lower())
    
    # Get lemmatized forms of tokens that are nouns, verbs, adjectives, or proper nouns
    # and are not stopwords or punctuation
    keywords = {token.lemma_ for token in doc 
                if token.is_alpha 
                and not token.is_stop 
                and not token.is_punct
                and (token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN'])}
    
    return keywords

def get_key_phrases(text: str, max_phrases: int = 10) -> List[str]:
    """
    Extract key phrases from text using spaCy's noun chunks.
    
    Args:
        text: Input text
        max_phrases: Maximum number of phrases to return
        
    Returns:
        List of key phrases
    """
    doc = nlp(text.lower())
    
    # Extract noun chunks as phrases
    phrases = [chunk.text for chunk in doc.noun_chunks 
               if len(chunk.text.split()) > 1]  # Only multi-word phrases
    
    # Get most common phrases
    common_phrases = Counter(phrases).most_common(max_phrases)
    
    return [phrase for phrase, _ in common_phrases]

def calculate_keyword_match(jd_keywords: Set[str], resume_keywords: Set[str]) -> Tuple[float, Set[str]]:
    """
    Calculate keyword match score based on the overlap between job description 
    and resume keywords.
    
    Args:
        jd_keywords: Set of keywords from job description
        resume_keywords: Set of keywords from resume
        
    Returns:
        Tuple containing:
        - Keyword match score (0-1)
        - Set of matching keywords
    """
    if not jd_keywords:
        return 0.0, set()
    
    # Find intersection of keywords
    matching_keywords = jd_keywords.intersection(resume_keywords)
    
    # Calculate match score: number of matching keywords / number of JD keywords
    match_score = len(matching_keywords) / len(jd_keywords)
    
    return match_score, matching_keywords

def calculate_semantic_similarity(jd_text: str, resume_text: str) -> float:
    """
    Calculate semantic similarity between job description and resume using spaCy's vector similarity.
    
    Args:
        jd_text: Job description text
        resume_text: Resume text
        
    Returns:
        Semantic similarity score (0-1)
    """
    # Process texts with spaCy
    jd_doc = nlp(jd_text)
    resume_doc = nlp(resume_text)
    
    # If either document has no vector representation, return 0
    if not jd_doc.has_vector or not resume_doc.has_vector:
        return 0.0
    
    # Calculate cosine similarity between the document vectors
    similarity = jd_doc.similarity(resume_doc)
    
    # Ensure similarity is between 0 and 1
    return max(0.0, min(similarity, 1.0))

def calculate_match_score(jd_text: str, resume_text: str) -> Tuple[float, float, float, List[str]]:
    """
    Calculate overall match score between job description and resume.
    
    Args:
        jd_text: Job description text
        resume_text: Resume text
        
    Returns:
        Tuple containing:
        - Overall match score (0-1)
        - Keyword match score (0-1)
        - Semantic similarity score (0-1)
        - List of matched keywords
    """
    # Extract keywords
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)
    
    # Calculate keyword match
    keyword_score, matched_keywords = calculate_keyword_match(jd_keywords, resume_keywords)
    
    # Calculate semantic similarity
    semantic_score = calculate_semantic_similarity(jd_text, resume_text)
    
    # Calculate overall score as weighted average
    # 50% keyword match, 50% semantic similarity
    overall_score = 0.5 * keyword_score + 0.5 * semantic_score
    
    return overall_score, keyword_score, semantic_score, list(matched_keywords)
