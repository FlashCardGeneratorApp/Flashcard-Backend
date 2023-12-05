import openai
from dotenv import load_dotenv
import os
model = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview"}
load_dotenv()
client = openai.OpenAI(api_key=os.environ["CUSTOMCONNSTR_OPENAI_KEY"])

def get_prompts(file="prompt.txt"):
    with open(file, "r") as f:
        prompts = f.read().split("\n\n")
        return[prompt.replace("\n", "") for prompt in prompts]

def generate_questions(user_prompt):
    prompts = get_prompts()
    messages = [
        {"role": "system", "content": prompts[0]},
        {"role": "user", "content": prompts[1]},
        {"role": "assistant", "content": prompts[2]},
        {"role": "user", "content": f"{user_prompt}"},
    ]

    # Create completion using OpenAI API
    response = client.chat.completions.create(
        model=model[3],
        messages=messages,
        n=1,
    )

    # Extract content from the API response
    generated_content = response.choices[0].message.content

    # Assuming generated_content is in a specific format, transform it to a dictionary
    # Here's an example structure:
    generated_questions = {
        "Question": generated_content.get("question"),
        "Options": generated_content.get("options"),
        "Answer": generated_content.get("answer")
    }

    return generated_questions

def main():
    user_input = input("Text: ")
    print(generate_questions(user_prompt = user_input))

if __name__ == "__main__":
    main()