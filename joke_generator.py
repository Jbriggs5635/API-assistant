"""
Random Joke Generator - Python Version
With Category Support
Powered by JokeAPI (https://jokeapi.dev)
"""

import requests
import json
import os
from typing import Dict, Optional

# API Base URL
API_BASE_URL = "https://v2.jokeapi.dev/joke"

# Available joke categories
CATEGORIES = {
    '1': {'key': 'any', 'name': 'Any (Random)'},
    '2': {'key': 'programming', 'name': 'Programming'},
    '3': {'key': 'knock-knock', 'name': 'Knock-Knock'},
    '4': {'key': 'general', 'name': 'General'},
    '5': {'key': 'dark', 'name': 'Dark Humor'},
    '6': {'key': 'pun', 'name': 'Pun'},
    '7': {'key': 'spooky', 'name': 'Spooky'},
}


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_joke(category: str = 'any') -> Optional[Dict]:
    """
    Fetch a joke from JokeAPI based on the selected category
    
    Args:
        category (str): The joke category (default: 'any')
    
    Returns:
        dict: Joke data if successful, None otherwise
    """
    try:
        # Map category to API format
        category_map = {
            'any': 'Any',
            'programming': 'Programming',
            'knock-knock': 'Knock-Knock',
            'general': 'General',
            'dark': 'Dark',
            'pun': 'Pun',
            'spooky': 'Spooky'
        }
        
        api_category = category_map.get(category, 'Any')
        url = f"{API_BASE_URL}/{api_category}"
        
        # Make API request
        response = requests.get(url, timeout=5)
        
        # Check if request was successful
        if response.status_code == 200:
            joke_data = response.json()
            
            # Check for API errors
            if joke_data.get('error'):
                print("❌ API Error: Could not fetch joke from this category")
                return None
            
            return joke_data
        else:
            print(f"❌ Error: API returned status code {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. Please check your internet connection.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Failed to connect to API - {e}")
        return None
    except json.JSONDecodeError:
        print("❌ Error: Failed to parse API response")
        return None


def display_joke(joke_data: Dict) -> None:
    """
    Display the joke in a formatted way
    
    Args:
        joke_data (dict): The joke data from API
    """
    print("\n" + "="*60)
    print(f"📌 Category: {joke_data.get('category', 'Unknown')}")
    print(f"📝 Type: {'Single Liner' if joke_data.get('type') == 'single' else 'Two-Part Joke'}")
    print("="*60)
    
    if joke_data.get('type') == 'single':
        # Single-line joke
        print(f"\n😂 {joke_data.get('joke', 'No joke found')}\n")
    elif joke_data.get('type') == 'twopart':
        # Two-part joke (setup and punchline)
        print(f"\n🎬 Setup: {joke_data.get('setup', 'No setup found')}")
        print(f"\n😄 Punchline: {joke_data.get('delivery', 'No punchline found')}\n")
    
    print("="*60 + "\n")


def show_menu() -> None:
    """Display the menu of available categories"""
    print("\n🎭 JOKE GENERATOR - SELECT A CATEGORY 🎭\n")
    
    for key, value in CATEGORIES.items():
        print(f"{key}. {value['name']}")
    
    print("8. Exit\n")


def get_user_choice() -> str:
    """
    Get and validate user input
    
    Returns:
        str: The user's choice
    """
    while True:
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice in list(CATEGORIES.keys()) + ['8']:
            return choice
        else:
            print("❌ Invalid choice! Please enter a number between 1-8.\n")


def main() -> None:
    """Main function to run the joke generator"""
    clear_screen()
    
    print("╔════════════════════════════════════════════════════════╗")
    print("║         🎉 WELCOME TO JOKE GENERATOR! 🎉               ║")
    print("║                                                        ║")
    print("║  Get random jokes from different categories!          ║")
    print("║  Powered by JokeAPI (https://jokeapi.dev)            ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    while True:
        show_menu()
        choice = get_user_choice()
        
        # Check if user wants to exit
        if choice == '8':
            print("👋 Thanks for using Joke Generator! Goodbye!\n")
            break
        
        # Get selected category
        selected_category = CATEGORIES[choice]['key']
        category_name = CATEGORIES[choice]['name']
        
        print(f"\n⏳ Getting {category_name.lower()} joke...\n")
        
        # Fetch joke
        joke = get_joke(selected_category)
        
        # Display joke if successfully fetched
        if joke:
            display_joke(joke)
        else:
            print("Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")