import random
import gradio as gr
from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def random_response(message, history):
    # Debug logging
    print(f"Current message: {message}")
    print(f"History type: {type(history)}")
    print(f"History content: {history}")
    
    # Create messages list for the API
    messages = []
    
    # Add previous messages from history if available
    if history and len(history) > 0:
        try:
            # In Gradio's ChatInterface, history is a list of [user_message, bot_message] pairs
            for i, exchange in enumerate(history):
                print(f"Processing exchange {i}: {exchange}")
                
                # Try to extract user and assistant messages
                try:
                    # Handle different possible formats
                    if isinstance(exchange, (tuple, list)) and len(exchange) >= 2:
                        user_msg = exchange[0]
                        assistant_msg = exchange[1]
                    elif isinstance(exchange, dict):
                        user_msg = exchange.get("user", "")
                        assistant_msg = exchange.get("assistant", "")
                    else:
                        print(f"Exchange {i} is in an unrecognized format")
                        continue
                    
                    # Only add if both messages are non-empty
                    if user_msg and assistant_msg:
                        messages.append({"role": "user", "content": user_msg})
                        messages.append({"role": "assistant", "content": assistant_msg})
                        print(f"Added exchange {i} to context")
                    else:
                        print(f"Exchange {i} has empty messages")
                except Exception as e:
                    print(f"Error processing exchange {i}: {e}")
        except Exception as e:
            print(f"Error processing history: {e}")
    
    # Add the current message
    messages.append({
        "role": "user",
        "content": message,
    })
    
    print(f"Final messages being sent to API: {messages}")
    
    # Make the API call
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    return chat_completion.choices[0].message.content
    
demo = gr.ChatInterface(random_response, type="messages", autofocus=False)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
