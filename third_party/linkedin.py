import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape info from linkedin profiles,
    manually scrape the info from linkedin profiles.§
    """
    try:
        if mock:
            print("mock")
            linkedin_profile_url = "https://gist.githubusercontent.com/diyaralyasiri/cc29fdafa18e936b16e6c907d014610d/raw/c946e728758b779d4f33b79a3e3430a90474abe5/diyar.json"
            response = requests.get(
                linkedin_profile_url,
                timeout=25,
            )
        else:
            api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
            header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
            response = requests.get(
                api_endpoint,
                params={"url": linkedin_profile_url},
                headers=header_dic,
                timeout=10,
            )
        response.raise_for_status()
        
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not in JSON format")
            print(f"Response text: {response.text}")
            data = None  
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        data = None
    
        
    data=response.json()
    
    data = {
    k: v
    for k, v in data.items()
    if v not in ([], "", "", None)
    and k not in ["people_also_viewed", "certifications"]
    }
    
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    
    return data
        
if __name__ =="__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/diyar-alyasiri/", mock = True
        )
    )