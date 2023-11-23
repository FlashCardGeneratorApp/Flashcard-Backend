import openai
from dotenv import load_dotenv
import os
model = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview"}
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))


prompt = """Your response must be a list of dictionary key-value pairing related
 to the users input. The length of the list of dictionaries is determined by the user.
 The correct answer is the dictonary key's value.

ww1 2 questions

[{":"Question": When did the second world war begin, 
"Options": ["1914", "1944", "1945", "1939"], 
"Answer": "1939"},
 {"Question": ""Who was the leader of Nazi Germany?",
 "Options": ["Jospeh Stalin", "Joseph Goebbels", "Heinrich Himmler", "Adolf Hitler"], 
 "Answer": "Adolf Hitler"}]"""

def get_prompts(prompt=prompt):
    prompts = prompt.split("\n\n")
    return[prompt.replace("\n", "") for prompt in prompts]
    
def generate_questions(user_prompt):
    prompts = get_prompts()
    print("prompt1: ",prompts[0])
    print("prompt2: ",prompts[1])
    print("prompt3: ",prompts[2])
    messages =[{"role": "system","content": prompts[0]},
    {"role": "user","content": prompts[1]},
    {"role":"assistant", "content":prompts[2]},
    {"role": "user","content": f"{user_prompt}"},]
    return client.chat.completions.create(
        model=model[3],
        messages = messages,
        n=1,
    ).choices[0].message.content

def main():
    user_input = input("Text: ")
    print(generate_questions(user_prompt = user_input))

if __name__ == "__main__":
    main()