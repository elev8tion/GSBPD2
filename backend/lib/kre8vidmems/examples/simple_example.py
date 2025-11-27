#!/usr/bin/env python3
"""
Simple example: Create and search a knowledge base
"""
from kre8vidmems import Kre8VidMemory

def main():
    print("=== Kre8VidMems Simple Example ===\n")
    
    # Create memory
    print("Creating memory...")
    mem = Kre8VidMemory()
    
    # Add some facts
    mem.add("The Eiffel Tower is located in Paris, France. It was completed in 1889.")
    mem.add("The Great Wall of China is over 13,000 miles long.")
    mem.add("The Statue of Liberty was a gift from France to the United States in 1886.")
    mem.add("Mount Everest is the highest mountain in the world at 29,032 feet.")
    mem.add("The Amazon rainforest produces 20% of the world's oxygen.")
    
    # Save as video
    mem.save("simple_knowledge")
    
    print("\n" + "="*50)
    input("\nPress Enter to search the memory...")
    
    # Load and search
    print("\n=== Searching ===\n")
    mem = Kre8VidMemory.load("simple_knowledge")
    
    queries = [
        "tell me about France",
        "what's the tallest mountain?",
        "facts about oxygen"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 40)
        results = mem.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. [Score: {result['score']:.2f}]")
            print(f"   {result['text']}\n")

if __name__ == "__main__":
    main()
