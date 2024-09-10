import requests, json, re
from urllib import parse

def post_data_to_webapp(json_data, webapp_url):
    # Post the data to the webapp
    response = requests.post(webapp_url, json=json_data)

    if response.status_code == 200:
        print("Data posted successfully!")
    else:
        print(f"Failed to post data. Status code: {response.status_code}")

# Function to get the content of a website
def get_website_content(url):
    try:
        # Make a GET request to the website
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the content of the website
            content = response.text  # or response.content for raw bytes
            content = json.loads(content)
            return content
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def process_main(EP, SCRAPE_SITE, KEYWORDS):
    data = []
    for keyword in KEYWORDS:
        webapp_url = 'https://script.google.com/macros/s/AKfycby555e_VnQFJQ6IQr_OKya9Eq74yz53VGU-Wm2IA1hGkHEgaB0j5rO7xVbFQAsbXZyt/exec?keyword='+keyword
        try:
          keyword =parse.parse_qs(parse.urlparse(keyword).query)['q'][0]
          split_url = parse.urlsplit(keyword)
          base_domain = split_url.scheme+"://"+split_url.netloc
    
          API_EP = EP +'/get?url='+ SCRAPE_SITE + keyword +'&tag=article'
          website_content = get_website_content(API_EP)
    
          if "Failed" not in website_content and len(website_content['results']) > 0:
            for count, value in enumerate(website_content['results']):
              href = base_domain+value['hrefs'][0]
              find_id = re.search(r'~([a-z0-9]+)\/\?', href)
    
              jobText = value['articleText']
              jobTags = jobText.split("\n\n")
    
              sub_data = {}
              sub_data['keyword'] = keyword
              sub_data['job_id'] = find_id.group(1)
              sub_data['articleText'] = jobText.replace("\n\n"+jobTags[len(jobTags)-1], "")
              sub_data['job_tags'] = jobTags[len(jobTags)-1].replace("\n", ",")
              sub_data['link'] = href
    
              data.append(sub_data)
        except Exception as e:
          print("error")
          print(e)
          pass
    
    data_json = json.dumps(data)
    post_data_to_webapp(data, webapp_url)
