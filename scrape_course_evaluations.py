import pandas as pd
from tqdm import tqdm
from extract_info_from_html import get_info_from_html
import time
import random
import requests
from get_cookies import get_cookies
import pickle
import os

# Set target url here (omit in github)
TARGET_URL = "https://example.edu"
REPORT_URL = "test_report"

# replace term here
TERM = "term_12s"

if not os.path.exists(f"{TERM}_course_evaluations.csv"):
    breaking_point = None
else:
    old_df = pd.read_csv(f"{TERM}_course_evaluations.csv")
    breaking_point = old_df["Class ID"][len(old_df)-1]

base_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

df_headers = ["Term", "Class ID", "School", "Enrollment", "Eligible to Respond", "Response Count", "Response Rate"]

#rotating proxies; omit in github
proxy_list = []
COOKIE_LASTING_TIME = 50

proxy_cookies = []

proxy_num = 0
num_uses = 0

def get_valid_cookie():
    cookies = get_cookies(TARGET_URL)
    return cookies[4]["value"]

def make_request_with_rotating_proxy(url, headers, proxy_list, cookie):
        
    global proxy_num
    global num_uses
    global proxy_cookies

    # Select a proxy for this attempt
    proxy = proxy_list[proxy_num]
    
    # The proxies dictionary tells requests to use this proxy for both http and https
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    
    try:
        new_headers = {}
        new_headers['User-Agent'] = headers['User-Agent']
        new_headers['Cookie'] = f"PTGSESSID={cookie}"

        # It's good practice to set a timeout
        response = requests.get(url, headers=new_headers, proxies=proxies, timeout=10)
        # response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        proxy_num = (proxy_num + 1) % 5
        
        # print(f"Success! Fetched {url} using proxy ending in ...{proxy[-20:]}")
        return response
        
    except requests.exceptions.ProxyError as e:
        print(f"Proxy Error with {proxy}. It might be down or blocked. Trying another. Error: {e}")
    except requests.exceptions.ConnectTimeout as e:
        print(f"Connection timed out with proxy {proxy}. Trying another. Error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} for URL {url} with proxy {proxy}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    proxy_num = (proxy_num + 1) % 5
    return None

def get_url_from_row(row):
    class_section = row["Class Section"]
    term = row["Term"]
    section_abrv, class_num = class_section.split(" ")
    url = f"https://{TARGET_URL}/{REPORT_URL}/{section_abrv.lower()}{class_num}.{term.split("\n")[0].lower()}"
    return url

data = pd.read_csv(f"{TERM}_scraped_data.csv")

data_rows = []
cookie = get_valid_cookie()

breaking_point_reached = False
if breaking_point is None:
    breaking_point_reached = True

questions_lst = []
end_now = False

for index, row in tqdm(data.iterrows()):
    if not breaking_point_reached:
        # skip this since we've already looked at it
        try:
            class_section = row["Class Section"]
            term = row["Term"]
            section_abrv, class_num = class_section.split(" ")
            class_id = f"{section_abrv.lower()}{class_num}.{term.split("\n")[0]}"
            class_id = class_id.upper()
            if class_id == breaking_point:
                breaking_point_reached = True
            continue
        except:
            # cant deal with this rn
            continue

    status_code = 404
    first_attempt = True

    try:
        url = get_url_from_row(row)
    except:
        print(f"Weird error. Section {row["Class Section"]}, Term {row["Term"]}")
        continue

    while status_code != 200:
        if not first_attempt:
            print("Rate limit exceeded. Please try again later.", url)
            status_code = 200
            end_now = True
        
        # print("starting request at", url)
        r = make_request_with_rotating_proxy(url, base_headers, proxy_list, cookie)
        if r is None:
            print("Rate limit exceeded. Please try again later.", url)
            status_code = 200
            end_now = True
        
        else:
            status_code = r.status_code
            first_attempt = False

            if status_code == 200:
                try:
                    data = get_info_from_html(r.content)
                except:
                    data = None
    
    if end_now:
        break

    if data is None:
        print("data is none at url", url, "saving html to file")
        with open(row["Class Section"]+row["Term"]+".html", "w") as file:
            # Write the string into the file
            file.write(r.text)
        continue

    questions_lst = []
    data_row = []
    question_num = 1

    # questions that appear twice are a weird edge case, just ignore the second count to not mess up the .csv
    past_questions = set()
    for q, responses in data:
        if q in past_questions:
            continue
        if q != "-":
            past_questions.add(q)
            questions_lst.append(f"Q{question_num}: {q}")
            question_num += 1
        data_row.extend(responses)

    if len(data_row) != 97:
        print("PROBLEM AT", url)
    else:
        data_rows.append(data_row)
    
    # follow guideline from robots.txt
    time.sleep(random.uniform(30, 35))

for i in range(len(questions_lst)):
    for q_type in ["SD", "D", "N", "A", "SA", "TOT"]:
        df_headers.append(f"Q{i+1} - {q_type}")

with open(f"{TERM}_questions.txt", 'w') as file:
    file.write("\n".join(questions_lst))

if len(data_rows) > 0:
    print("Num questions:", len(questions_lst))
    print("Num rows added:", len(data_rows))
    df_new = pd.DataFrame(data_rows, columns=df_headers)
    print('df new has been created')
    if os.path.exists(f"{TERM}_course_evaluations.csv"):
        df_old = pd.read_csv(f"{TERM}_course_evaluations.csv")
        df_final = pd.concat([df_old, df_new])
        df_final.to_csv(f"{TERM}_course_evaluations.csv", index=False)
    else:
        df_new.to_csv(f"{TERM}_course_evaluations.csv", index=False)
else:
    print("No data added")