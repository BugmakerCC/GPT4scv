import openai
import os
openai.api_key = ''
def generate_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    res_msg = completion.choices[0].message
    return res_msg["content"].strip()

def preprocess(text):
    l = ['vulnerable_at_lines:', '// <yes> <report> DENIAL_OF_SERVICE', '// <yes> <report> ARITHMETIC', '// <yes> <report> BAD_RANDOMNESS', '// <yes> <report> ACCESS_CONTROL', '// <yes> <report> FRONT_RUNNING', '// <yes> <report> REENTRANCY', '// <yes> <report> SHORT_ADDRESSES', '// <yes> <report> TIME_MANIPULATION', '// <yes> <report> UNCHECKED_LL_CALLS']
    for i in l:
        text = text.replace(i,'')
    return text

messages = [{"role": "system", "content": "Help me detect vulnerabilities in smart contracts"}]
messages.append({"role": "user", "content": "There are nine common types of vulnerabilities in smart contracts. Next, I will tell you their definitions and scenarios, learn and remember them. After I teach you all kinds of vulnerabilities, I will give you a smart contract code, and you can judge whether there are the above vulnerabilities in the code."})
res_msg = generate_answer(messages)


messages.append({"role": "user", "content": "First, Reentrancy. Reentrancy occurs when external contract calls are allowed to make new calls to the calling contract before the initial execution is complete. For a function, this means that the contract state may change in the middle of its execution as a result of a call to an untrusted contract or the use of a low level function with an external address."})


res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Second, Access Control. One usually accesses a contract's functionality through its public or external functions. While insecure visibility settings give attackers straightforward ways to access a contract's private values or logic, access control bypasses are sometimes more subtle. These vulnerabilities can occur when contracts use the deprecated tx.origin to validate callers, handle large authorization logic with lengthy require and make reckless use of delegatecall in proxy libraries or proxy contracts."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Third, Arithmetic Issues. Integer overflows and underflows are not a new class of vulnerability, but they are especially dangerous in smart contracts, where unsigned integers are prevalent and most developers are used to simple int types (which are often just signed integers). If overflows occur, many benign-seeming codepaths become vectors for theft or denial of service."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Fourth, Unchecked Return Values For Low Level Calls. One of the deeper features of Solidity are the low level functions call(), callcode(), delegatecall() and send(). Their behavior in accounting for errors is quite different from other Solidity functions, as they will not propagate (or bubble up) and will not lead to a total reversion of the current execution. Instead, they will return a boolean value set to false, and the code will continue to run. This can surprise developers and, if the return value of such low-level calls are not checked, can lead to fail-opens and other unwanted outcomes. Remember, send can fail!"})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Fifth, Denial of Service. Denial of service is deadly in the world of Ethereum: while other types of applications can eventually recover, smart contracts can be taken offline forever by just one of these attacks. Many ways lead to denials of service, including maliciously behaving when being the recipient of a transaction, artificially increasing the gas necessary to compute a function, abusing access controls to access private components of smart contracts, taking advantage of mixups and negligence, etc. This class of attack includes many different variants and will probably see a lot of development in the years to come."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Sixth, Bad Randomness. Randomness is hard to get right in Ethereum. While Solidity offers functions and variables that can access apparently hard-to-predict values, they are generally either more public than they seem or subject to miners' influence. Because these sources of randomness are to an extent predictable, malicious users can generally replicate it and attack the function relying on its unpredictablility."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Seventh, Front-Running. Since miners always get rewarded via gas fees for running code on behalf of externally owned addresses (EOA), users can specify higher fees to have their transactions mined more quickly. Since the Ethereum blockchain is public, everyone can see the contents of others' pending transactions. This means if a given user is revealing the solution to a puzzle or other valuable secret, a malicious user can steal the solution and copy their transaction with higher fees to preempt the original solution. If developers of smart contracts are not careful, this situation can lead to practical and devastating front-running attacks."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Eighth, Time manipulation. From locking a token sale to unlocking funds at a specific time for a game, contracts sometimes need to rely on the current time. This is usually done via block.timestamp or its alias now in Solidity. But where does that value come from? From the miners! Because a transaction's miner has leeway in reporting the time at which the mining occurred, good smart contracts will avoid relying strongly on the time advertised. Note that block.timestamp is also sometimes (mis)used in the generation of random numbers as is discussed in #6. Bad Randomness."})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

messages.append({"role": "user", "content": "Nineth, Short Address Attack. Short address attacks are a side-effect of the EVM itself accepting incorrectly padded arguments. Attackers can exploit this by using specially-crafted addresses to make poorly coded clients encode arguments incorrectly before including them in transactions. "})
res_msg = generate_answer(messages)
messages.append({"role": "assistant", "content": res_msg})

error_cnt = 0
for i in os.listdir('./smartbugs-curated-main/dataset/all'):
    with open('./smartbugs-curated-main/dataset/all/' + i, 'r' , encoding='utf-8') as f:
        lines = f.readlines()
    print(i)
    codes = ''
    for line in lines:
        codes += line
    codes_processed = preprocess(codes)
    messages.append({"role": "user", "content": "My teaching is over. Check the following smart contract for the above vulnerabilities. The presence or absence of each vulnerability is indicated by true and false, respectively. Output your conclusion in a similar manner: Reentrancy: true\nAccess Control: true\nArithmetic Issues: false\nUnchecked Return Values For Low Level Calls: false\nDenial of Service: true\nBad Randomness: false\nFront-Running: false\nTime manipulation: true\nShort Address Attack: false. Only conclusions are needed, and no other analysis is required. \n"+ codes_processed})
    try:
        res_msg = generate_answer(messages)
        with open('./results2/' + i[:-4] + '.txt', 'w') as f:
            f.write(res_msg)
    except Exception as e:
        print('error:', e)
        error_cnt += 1
    finally:
        messages = messages[:-1]
print(error_cnt)