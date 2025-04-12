import argparse
from perspective_post_generator import PerspectivePostGenerator

# Sample physician perspectives
DEFAULT_PERSPECTIVES = [
    "AI should augment healthcare professionals, not replace them",
    "Technology must enhance the human connection in medicine, not diminish it",
    "Data privacy and ethical considerations must be prioritized in healthcare AI",
    "AI tools should reduce administrative burden to allow more time with patients",
    "Healthcare AI should focus on improving patient outcomes and experience",
    "AI solutions must be accessible to all healthcare providers, not just large institutions",
    "Clinicians should be involved in the development of healthcare AI systems"
]

def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn posts from a physician's perspective")
    parser.add_argument("--input", required=True, help="Article URL or summary text")
    parser.add_argument("--is-url", action="store_true", help="Whether the input is a URL")
    parser.add_argument("--word-count", type=int, default=225, help="Target word count")
    parser.add_argument("--perspectives-file", help="Path to a file containing perspective statements (one per line)")
    
    args = parser.parse_args()
    
    # Load custom perspectives if provided
    perspectives = DEFAULT_PERSPECTIVES
    if args.perspectives_file:
        try:
            with open(args.perspectives_file, 'r') as f:
                perspectives = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading perspectives file: {e}")
            print("Using default perspectives instead.")
    
    # Initialize generator
    generator = PerspectivePostGenerator(perspectives)
    
    # Generate post
    result = generator.generate_post(args.input, args.is_url, args.word_count)
    
    # Print results
    print("\n" + "="*50)
    print("GENERATED LINKEDIN POST:")
    print("="*50)
    print(result["post"])
    print("\n" + "-"*50)
    print(f"Confidence Score: {result['confidence_score']:.2f}")
    if result.get("error"):
        print(f"Error: {result['error']}")
    print("="*50)

if __name__ == "__main__":
    main() 