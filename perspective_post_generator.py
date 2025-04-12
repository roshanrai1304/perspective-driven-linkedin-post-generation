import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re
import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PerspectivePostGenerator:
    def __init__(self, perspective_statements: List[str], model_name: str = "gemini-2.0-flash"):
        """
        Initialize the post generator with physician's perspective statements.
        
        Args:
            perspective_statements: List of statements representing the physician's perspective
            model_name: Gemini model to use
        """
        self.perspective_statements = perspective_statements
        self.model = genai.GenerativeModel(model_name)
        
    def extract_article_content(self, url: str) -> str:
        """Extract the main content from an article URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
                
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Remove blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 2000 characters for summary purposes
            return text[:2000]
        except Exception as e:
            print(f"Error extracting content from URL: {e}")
            return ""
    
    def generate_post(self, 
                     article_input: str, 
                     is_url: bool = False, 
                     word_count: int = 225) -> Dict:
        """
        Generate a LinkedIn post based on article content and physician's perspective.
        
        Args:
            article_input: Either an article URL or a summary of an article
            is_url: Whether the article_input is a URL
            word_count: Target word count for the LinkedIn post
            
        Returns:
            Dictionary containing the generated post and confidence score
        """
        # Process input
        if is_url:
            article_content = self.extract_article_content(article_input)
            if not article_content:
                return {
                    "post": "",
                    "confidence_score": 0.0,
                    "error": "Could not extract content from URL"
                }
        else:
            article_content = article_input
            
        # Construct the prompt
        prompt = self._construct_prompt(article_content, word_count)
        
        # Generate content
        response = self.model.generate_content(prompt)
        
        # Extract the post and confidence score
        try:
            result = self._parse_response(response.text)
            return result
        except Exception as e:
            return {
                "post": response.text,
                "confidence_score": self._calculate_confidence(response.text),
                "error": str(e)
            }
    
    def _construct_prompt(self, article_content: str, word_count: int) -> str:
        """Construct the prompt for the AI model."""
        perspective_text = "\n".join([f"- {p}" for p in self.perspective_statements])
        
        prompt = f"""
        You are an AI assistant helping a physician create LinkedIn posts about healthcare AI topics.
        
        # ARTICLE CONTENT
        {article_content}
        
        # PHYSICIAN'S PERSPECTIVE ON AI IN HEALTHCARE
        {perspective_text}
        
        # TASK
        Generate a LinkedIn post (approximately {word_count} words) that discusses the article content from the physician's perspective.
        
        The post should:
        1. Reflect the physician's "AI as enabler" philosophy
        2. Maintain a professional, thoughtful tone
        3. Include a brief commentary on the implications for healthcare
        4. End with a thought-provoking question or call to action
        5. Be written in first person as if the physician is writing it
        6. Use 2-3 relevant emojis strategically placed throughout the post
        7. Format the content into 2-3 paragraphs for better readability
        
        # OUTPUT FORMAT
        Your response must strictly follow this exact format:

        POST:
        [Your LinkedIn post content with emojis and paragraph breaks]

        CONFIDENCE_SCORE: 0.85
        
        REASONING:
        [Your explanation for the confidence score]

        Important: For the CONFIDENCE_SCORE, you must provide a single decimal number between 0.7 and 0.95. Do not include any text, just the number. For example: "CONFIDENCE_SCORE: 0.82" or "CONFIDENCE_SCORE: 0.75"
        """
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse the response to extract the post and confidence score."""
        post_match = re.search(r"POST:(.*?)(?:CONFIDENCE_SCORE:|$)", response_text, re.DOTALL)
        confidence_match = re.search(r"CONFIDENCE_SCORE:(.*?)(?:REASONING:|$)", response_text, re.DOTALL)
        
        post = post_match.group(1).strip() if post_match else response_text
        
        confidence_text = confidence_match.group(1).strip() if confidence_match else "0.7"
        # Extract decimal number from the confidence text
        confidence_number = re.search(r"(\d+\.\d+|\d+)", confidence_text)
        confidence_score = float(confidence_number.group(1)) if confidence_number else 0.7
        
        return {
            "post": post,
            "confidence_score": confidence_score,
            "error": None
        }
    
    def _calculate_confidence(self, post: str) -> float:
        """
        Calculate a confidence score based on how well the post aligns with the perspective statements.
        This is a fallback method if the model doesn't provide a score.
        """
        score = 0.7  # Default score
        
        # Count how many perspective statements are reflected in the post
        keywords = set()
        for statement in self.perspective_statements:
            # Extract key terms from each perspective statement
            terms = re.findall(r'\b\w{4,}\b', statement.lower())
            keywords.update(terms)
        
        # Count matches
        matches = 0
        for keyword in keywords:
            if keyword.lower() in post.lower():
                matches += 1
        
        # Calculate score based on percentage of keywords matched
        if keywords:
            keyword_score = min(matches / len(keywords), 1.0)
            # Blend with default score
            score = 0.3 * score + 0.7 * keyword_score
            
        return score 