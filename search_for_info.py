from duckduckgo_search import DDGS
import time

def search(prompt) :
    failure = 0
    prompt = "Chess Opening :" + prompt.strip()
    while(True):
        try:
            # text = DDGS().chat(prompt, model='o3-mini', timeout=200)
            text = DDGS().text(prompt, max_results=4, backend= "html")
            break
        except Exception as e:
            if(failure == 0) :
                prompt = prompt.replace("Chess Opening :", "")
            print(prompt)
            print(f"number of failures: {failure}")
            print(e)
            failure += 1
            time.sleep(9)
            if(failure == 2):
                text = [{'title': 'False'}]
                break

    # print(text)
    # print(failure)
    return text
# search("Black Knights Tango")