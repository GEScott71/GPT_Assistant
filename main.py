# This Python program uses OpenAI tools to create a very simple ChatGPT assistant to answer questions from minutes of a meeting.
# It takes a text file as an input, queries the user for questions, and displays the responses to the user.
#
# First, it uploads a text file to ChatGPT
# Next, it creates a ChatGPT assistant that references that text file
# Then it creates a thread
# Then it starts a loop asking the user for questions.  When a question is entered,
# It creates a message with the question, adds it to the thread, and runs the assistant on the thread
# Finally, it displays the response from ChatGPT and starts the loop again

# Input: a file such as a text file, and user-entered questions
# Output: displays responses to the questions about the file

import openai
from openai import OpenAI
import time # used in function to periodically check assistant status

openai.api_key = open(r"C:\Users\GESco\Documents\key.txt", "r").read().strip('\n')
client = OpenAI(
    api_key=openai.api_key
)

def upload_file(path):  # Upload a file to OpenAI with an "assistants" purpose
    file = client.files.create(
        file=open(path, "rb"),
        purpose="assistants"
    )
    return file


def create_assistant(file): # Create an assistant with OpenAI with instructions and a file to reference
    assistant = client.beta.assistants.create(
        name="Meeting Analyzer",
        instructions="You are a helpful and highly skilled AI assistant trained in language comprehension and summarization. Answer questions on the provided meeting transcription:",
        tools=[{"type": "retrieval"}],
        model="gpt-4-turbo-preview",
        file_ids = [file.id]
    )
    return assistant

def run_assistant(message_body): # Create a message, run the assistant on it, monitor it for completion, and display the output
    # Create a message in an existing thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content=message_body,
    )

    # Run the existing assistant on the existing thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Monitor the assistant and report status
    while run.status != "completed":
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run.status)
        time.sleep(2)

    # Extract the messages from the thread
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Display the output
    print("\nOutput:")
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)

    return messages

if __name__ == '__main__':

    # *** Run these if creating a new assistant with a new file
    # file = upload_file(r'Data/unp_Q4_2023_earnings_call_transcript_2024-01-26.txt')
    # assistant = create_assistant(file)

    ## *** Run these if using an existing assistant:
    # saved_assistant_id = 'asst_GUjvBwaOxfHJFdb9qgDddRDn' # Meeting analyzer with UNP Q3 earnings call transcript
    saved_assistant_id = 'asst_Td0UqBTDjsmu6uwWVSybaSGc' # Meeting analyzer with UNP Q4 earnings call transcript
    assistant = client.beta.assistants.retrieve(saved_assistant_id)

    thread = client.beta.threads.create() # Create a new thread

    # As the user for input and run the assistant on it. Loop until the user types 'exit'
    while True:
        user_input = input("Enter a question, or type 'exit' to end: ").strip().lower()
        if user_input == 'exit':
            break

        else:
            run_assistant(user_input)
