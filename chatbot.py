import openai
import os
import time

openai.api_key = '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'

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def chat():
    print("------------------------[Conversation]--------------------------------")
    context = [ {'role':'system', 'content':"""
    You are a therapy chatbot. Your name is Kamlesh. you are supposed to carefully analyse the user\'s sentiments, \
    the user\'s past experiences and user\'s mindset in order to accurately and pleasantly \
    respond to the user. \
                 make sure reframe this in your own words when greeting the user\
                 if user inputs something other than therapy related, say that you're not trained for such replies
    """}, ]  # accumulate messages

    greet_prompt = f"""
        Introduce yourself using the context provided.
        Greet the user considering the time of day by fetching it from the internet.\
    """
    context += [{'role': 'system', 'content': f'{greet_prompt}'}]
    try: 
        response = get_completion_from_messages(context)
        print(f"{response}")

        while True:
            try:
                text = input("\n[YOU]: ")
                context += [{'role': 'user', 'content': f'{text}'}]
                if text.lower().__contains__('bye'):
                    break
                response = get_completion_from_messages(context)
                print(f"[KAMLESH]: {response}\n")
                context += [{'role': 'system', 'content': f"{response}"}]
            except openai.error.RateLimitError:
                time.sleep(60)
                print("[KAMLESH]: I apologize, can you repeat that?")

        bye_prompt = f"""
            Say your goodbyes to the user, thank them for chatting with you and giving you their time.
            Wish them for a good day or evening appropriately.
        """
        context += [{'role': 'system', 'content': f"{bye_prompt}"}]
        try:
            response = get_completion_from_messages(context)
            print(f"KAMLESH: {response}")
        except openai.error.RateLimitError:
            print("Rate limit reached")
    except openai.error.RateLimitError:
        print("Rate limit reached")

chat()