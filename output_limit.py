import os
import openai
from func_timeout import func_set_timeout
import func_timeout
messages = []
@func_set_timeout(30)
def generate_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    res_msg = completion.choices[0].message
    return res_msg["content"].strip()
openai.api_key = ''

filenames = list(set(os.listdir("./results_gpt4_2")) - set(os.listdir("./ana_gpt4_2")))
position_file = 0
messages = [{"role": "system", "content": "You are a semantic analyzer of text."}]
error_cnt = 0

while position_file < len(filenames):
    print(filenames[position_file])
    try:
        with open("./results_gpt4_2/" + filenames[position_file], 'r' , encoding='utf-8') as f:
            content = f.read()

        messages.append({"role": "user", "content": "You are a semantic analyzer of text. Here are nine common vulnerabilities. First, Reentrancy, also known as or related to race to empty, recursive call vulnerability, call to the unknown. Second, Access Control. Third, Arithmetic Issues, also known as integer overflow and integer underflow. Fourth, Unchecked Return Values For Low Level Calls, also known as or related to silent failing sends, unchecked-send. Fifth, Denial of Service, including gas limit reached, unexpected throw, unexpected kill, access control breached. Sixth, Bad Randomness, also known as nothing is secret. Seventh, Front-Running, also known as time-of-check vs time-of-use (TOCTOU), race condition, transaction ordering dependence (TOD). Eighth, Time manipulation, also known as timestamp dependence. Nineth, Short Address Attack, also known as or related to off-chain issues, client vulnerabilities. Think step by step, carefully. The following text is a vulnerability detection result for a smart contract. Use 0 or 1 to indicate whether whether there are specific types of vulnerabilities. For example: 'Reentrancy: 1'. The input is " + content})
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
            with open('./ana_gpt4_2/' + filenames[position_file][:-4] + '.txt', 'w') as f:
                f.write(res)
            position_file += 1
        finally:
            messages = messages[:-1]
    except Exception as e:
        position_file += 1
        print(f"exception: {e}")
        continue
