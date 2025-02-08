import sys
import numpy as np
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import seaborn as sns
import re
import os
import multiprocessing
import scipy

save_path = './'

brackets = list(np.array([0, 97, 394.75, 842, 1607.25, 2041, 5103])*100/12)
quantiles = [0, 0.25, 0.5, 0.75, 1.0]

from datetime import datetime
world_start_time = datetime.strptime('2001.01', '%Y.%m')

prompt_cost_1k, completion_cost_1k = 0.001, 0.002

def prettify_document(document: str) -> str:
    # Remove sequences of whitespace characters (including newlines)
    cleaned = re.sub(r'\s+', ' ', document).strip()
    return cleaned


def get_multiple_completion(dialogs, num_cpus=15, temperature=0, max_tokens=100):
    from functools import partial
    get_completion_partial = partial(get_completion, temperature=temperature, max_tokens=max_tokens)
    with multiprocessing.Pool(processes=num_cpus) as pool:
        results = pool.map(get_completion_partial, dialogs)
    total_cost = sum([cost for _, cost in results])
    return [response for response, _ in results], total_cost

def get_completion(dialogs, temperature=0, max_tokens=100):
    from openai import OpenAI
    # base_url = "https://openkey.cloud/v1"
    # api_key = "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"
    # client = OpenAI(base_url=base_url, api_key=api_key)
    base_url = "https://api.zhizengzeng.com/v1"
    api_key = "sk-zk2a99045e89d085b33b071d8d3b1edf5ae67301be585b1f"
    client = OpenAI(base_url=base_url, api_key=api_key)


    import time
    
   
    retries = 0
    while True:  # Keep retrying until we get a valid response
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=dialogs,
                temperature=temperature,
                max_tokens=max_tokens
            )

            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            this_cost = (prompt_tokens / 1000 * prompt_cost_1k) + (completion_tokens / 1000 * completion_cost_1k)

            return response.choices[0].message.content, this_cost  # Return the content and the cost

        except Exception as e:
            retries += 1
            print(f"Attempt {retries} failed: {type(e).__name__} - {e}")

            # If you want to continue retrying, increase the sleep time with each failure (exponential backoff)
            wait_time = 6 * retries  # Exponential backoff, you can tweak the factor if needed
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

def format_numbers(numbers):
    return '[' + ', '.join('{:.2f}'.format(num) for num in numbers) + ']'

def format_percentages(numbers):
    return '[' + ', '.join('{:.2%}'.format(num) for num in numbers) + ']'
