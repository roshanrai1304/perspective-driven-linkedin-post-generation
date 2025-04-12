from perspective_post_generator import PerspectivePostGenerator

# Sample physician perspectives
PHYSICIAN_PERSPECTIVES = [
    "AI should augment healthcare professionals, not replace them",
    "Technology must enhance the human connection in medicine, not diminish it",
    "Data privacy and ethical considerations must be prioritized in healthcare AI",
    "AI tools should reduce administrative burden to allow more time with patients",
    "Healthcare AI should focus on improving patient outcomes and experience",
    "AI solutions must be accessible to all healthcare providers, not just large institutions",
    "Clinicians should be involved in the development of healthcare AI systems"
]

# Initialize the generator
generator = PerspectivePostGenerator(PHYSICIAN_PERSPECTIVES)

# Sample article summaries
test_articles = [
    {
        "title": "AI-Powered Diagnostic Tool Shows Promise in Early Cancer Detection",
        "summary": "A new AI algorithm developed by researchers at Stanford has shown 94% accuracy in detecting early-stage pancreatic cancer from routine CT scans, potentially improving survival rates through earlier intervention. The tool is designed to assist radiologists by flagging suspicious findings for further review, not to replace human expertise."
    },
    {
        "title": "Study Reveals Physician Burnout Reduced by 30% with AI Documentation Assistants",
        "summary": "A recent study published in JAMA found that implementing AI-powered documentation assistants in primary care settings reduced physician burnout by 30% over six months. The technology transcribes patient-doctor conversations and automatically generates clinical notes, allowing physicians to spend more time engaging with patients and less time on paperwork."
    },
    {
        "title": "Concerns Raised Over Bias in Healthcare AI Systems",
        "summary": "A comprehensive review of healthcare AI systems published in Nature Medicine found significant biases in many algorithms, with models performing worse for underrepresented populations. Researchers call for more diverse training data and greater transparency in AI development to ensure these technologies don't exacerbate existing healthcare disparities."
    }
]

def run_tests():
    print("GENERATING SAMPLE LINKEDIN POSTS\n")
    
    for i, article in enumerate(test_articles, 1):
        print(f"SAMPLE {i}: {article['title']}")
        print("-" * 80)
        
        result = generator.generate_post(article['summary'])
        
        print(f"LINKEDIN POST (Confidence Score: {result['confidence_score']:.2f}):")
        print(result['post'])
        print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    run_tests() 