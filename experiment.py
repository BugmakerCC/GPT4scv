import openai
import os
from func_timeout import func_set_timeout
import func_timeout
messages = []
@func_set_timeout(100)
def generate_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    res_msg = completion.choices[0].message
    return res_msg["content"].strip()
openai.api_key = ''
messages = [{"role": "system", "content": "You are a vulnerability detector for a smart contract."}]

xx = os.listdir("./results_gpt4_5")
xxx = []
for i in xx:
    xxx.append(i[:-4] + '.sol')
filenames = list(set(os.listdir("./smartbugs-curated-main/dataset/all")) - set(xxx))
position_file = 0

def preprocess(text):
    l = ['vulnerable_at_lines:', '// <yes> <report> DENIAL_OF_SERVICE', '// <yes> <report> ARITHMETIC', '// <yes> <report> BAD_RANDOMNESS', '// <yes> <report> ACCESS_CONTROL', '// <yes> <report> FRONT_RUNNING', '// <yes> <report> REENTRANCY', '// <yes> <report> SHORT_ADDRESSES', '// <yes> <report> TIME_MANIPULATION', '// <yes> <report> UNCHECKED_LL_CALLS']
    for i in l:
        text = text.replace(i,'')
    return text

messages = [{"role": "system", "content": "You are a vulnerability detector for a smart contract."}]
error_cnt = 0

while position_file < len(filenames):
    print(filenames[position_file])
    with open("./smartbugs-curated-main/dataset/all/" + filenames[position_file], 'r' , encoding='utf-8') as f:
        codes = f.read()
    codes_processed = preprocess(codes)
    messages.append({"role": "user", "content": "You are a vulnerability detector for a smart contract. Here are nine common vulnerabilities. First, Reentrancy, also known as or related to race to empty, recursive call vulnerability, call to the unknown. Second, Access Control. Third, Arithmetic Issues, also known as integer overflow and integer underflow. Fourth, Unchecked Return Values For Low Level Calls, also known as or related to silent failing sends, unchecked-send. Fifth, Denial of Service, including gas limit reached, unexpected throw, unexpected kill, access control breached. Sixth, Bad Randomness, also known as nothing is secret. Seventh, Front-Running, also known as time-of-check vs time-of-use (TOCTOU), race condition, transaction ordering dependence (TOD). Eighth, Time manipulation, also known as timestamp dependence. Nineth, Short Address Attack, also known as or related to off-chain issues, client vulnerabilities. Think step by step, carefully. Check the following smart contract for the above vulnerabilities. The input is " + codes_processed})
    try:
        res = generate_answer(messages)
    except func_timeout.exceptions.FunctionTimedOut:
        print("time out")
    except openai.error.RateLimitError:
        print("rate limitation")
    except Exception as e:
        print('error:', e)
        position_file += 1
    else:
        print('success, outputting...')
        with open('./results_gpt4_5/' + filenames[position_file][:-4] + '.txt', 'w') as f:
            f.write(res)
        position_file += 1
    finally:
        messages = messages[:-1]