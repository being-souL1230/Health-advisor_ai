from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os
import re
import requests  # For catching network-related exceptions

# Load environment variables
env_vars = dotenv_values(".env")

# Retrieve environment variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Initialize chat log messages
messages = []

# Define the system prompt with enhanced instructions
System = f"""
Hello, I am {Username}, You are a highly accurate and advanced AI health assistant named {Assistantname}.
Your task is to understand the user's health condition described in their queries and provide clear, safe, and practical advice.
*** Do not provide any diagnosis that requires professional consultation but guide users on what they can do and when to see a doctor. ***
*** Reply only in English even if the input is in Hindi. ***
*** Format advice in bullet points with gaps (one empty line between points) for clarity when giving tips or advice. ***
*** Use friendly emojis (e.g., 😊👍) in responses to make them engaging, especially when providing tips or steps. ***
*** If the user asks for 'steps,' provide the response in a numbered list with clear, actionable steps. ***
*** If the user asks for 'tips' or 'advice,' provide practical suggestions in bullet points with gaps and emojis. ***
*** Avoid generic answers; be specific about health advice. ***
*** Do not add specific terms like 'tips' or 'steps' unless the user uses them; infer the format based on the query's intent. ***

If the user asks anything which is not related to health than reply in a friendly manner that you are only an ai health assistant , you cannot provide any other kind of info rathern than health related topic and reccommend the user to ask it from chatgpt , grok , deepseek etc. Do not provide any information other than health even when the user is asking consistently.
If the user asks consistently about other topics don't repeat the same reply as you gave before just change the replies of denial and you don't need to point your name repeatedly just give answer in a different manner politely don't repeat.

Sometimes you can give savage replies to the user like cool and sometimes use sarcasm and be friendly and cool, savage replies in some questions like when the user is asking repeatedly and other topics.
"""

# Define system chat prompt
SystemChatBot = [
    {"role": "system", "content": System}
]

# Ensure the 'Data' directory exists
if not os.path.exists('Data'):
    os.makedirs('Data')

# Load previous chat log from the file if exists, else create a new one
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to retrieve real-time information
def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour}:{minute}:{second} seconds.\n"
    return data

# Function to modify answers by formatting bullet points and ensuring gaps
def AnswerModifier(Answer):
    # Remove empty lines and clean up
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Detect if the response contains bullet points or numbered steps
    is_bullet_list = any(line.startswith('-') or line.startswith('*') for line in non_empty_lines)
    is_numbered_list = any(re.match(r'^\d+\.', line) for line in non_empty_lines)
    
    # If it's a bullet list, ensure gaps between points
    if is_bullet_list:
        formatted_lines = []
        for line in non_empty_lines:
            if line.startswith('-') or line.startswith('*'):
                # Ensure emoji is present, add 😊 if none
                if not any(char in line for char in ['😊', '👍', '✅']):
                    line = line.rstrip() + ' 😊'
                formatted_lines.append(line)
                formatted_lines.append('')  # Add gap
            else:
                formatted_lines.append(line)
        # Remove trailing empty line
        if formatted_lines and formatted_lines[-1] == '':
            formatted_lines.pop()
        return '\n'.join(formatted_lines)
    
    # If it's a numbered list (steps), ensure emoji and proper formatting
    elif is_numbered_list:
        formatted_lines = []
        for line in non_empty_lines:
            if re.match(r'^\d+\.', line):
                # Ensure emoji is present
                if not any(char in line for char in ['😊', '👍', '✅']):
                    line = line.rstrip() + ' 👍'
                formatted_lines.append(line)
                formatted_lines.append('')  # Add gap
            else:
                formatted_lines.append(line)
        if formatted_lines and formatted_lines[-1] == '':
            formatted_lines.pop()
        return '\n'.join(formatted_lines)
    
    # For non-list responses, join without extra gaps
    return '\n'.join(non_empty_lines)

# Main function to interact with the Groq API and process the user's query
def ChatBot(Query):
    try:
        # Add the user's query to the messages list
        messages.append({"role": "user", "content": Query})

        # Make the Groq API request
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Assuming the model is "llama3-70b-8192"
            messages=SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = ""
        finished = False

        # Process the response stream from Groq API
        for chunk in completion:
            # Only process the content of the response; suppress printing of the chunk data
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    Answer += content
                if chunk.choices[0].finish_reason == 'stop':
                    finished = True

            # If the response is complete (finish_reason='stop'), break the loop
            if finished:
                break

        # Clean the answer by removing unwanted tags
        Answer = Answer.replace("</s", "")

        # Add assistant's answer to the message history
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated messages to the file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Return the final answer with formatted output
        return AnswerModifier(Answer=Answer)

    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, Exception) as e:
        # Return a user-friendly error message instead of retrying
        error_message = """
No internet connection detected. Please check your network and try again.

- Ensure you're connected to Wi-Fi or mobile data. 🌐
- Restart your router if needed. 🔄
- Contact your ISP if the issue persists. 📞
"""
        # Add error message to chat history
        messages.append({"role": "assistant", "content": error_message})
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return AnswerModifier(error_message)

# Main loop to interact with the user
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        # Only print the final answer, suppress debug logs
        print(ChatBot(user_input))