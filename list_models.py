import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the .env file.")
        return
        
    print("Initializing Google GenAI client...")
    client = genai.Client(api_key=api_key)
    
    print("Fetching available models...")
    try:
        models = client.models.list()
        
        print("\n=== Models Supporting Content Generation ===")
        count = 0
        all_models = []
        
        for model in models:
            all_models.append(model)
            supported = False
            
            # Check supported_generation_methods attribute
            if hasattr(model, 'supported_generation_methods') and model.supported_generation_methods:
                if 'generateContent' in model.supported_generation_methods:
                    supported = True
            
            # Fallback to supported_actions if present
            elif hasattr(model, 'supported_actions') and model.supported_actions:
                if 'generateContent' in model.supported_actions:
                    supported = True
            
            if supported:
                # Remove 'models/' prefix if present for cleaner output
                clean_name = model.name.replace("models/", "") if model.name else "Unknown"
                print(f"- {clean_name}")
                count += 1
        
        if count == 0:
            print("No models specifically listing 'generateContent' were found based on attributes.")
            print("Here are all available models and their supported methods:")
            for model in all_models:
                methods = getattr(model, 'supported_generation_methods', getattr(model, 'supported_actions', 'Unknown'))
                clean_name = model.name.replace("models/", "") if model.name else "Unknown"
                print(f"- {clean_name} (Methods: {methods})")
                count += 1
                
        print(f"\nTotal suitable models found: {count}")
    except Exception as e:
        print(f"Failed to fetch models: {e}")

if __name__ == "__main__":
    main()
