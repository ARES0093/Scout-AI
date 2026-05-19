import requests

NOTION_TOKEN = "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" 
DATABASE_ID = "356e7616647480e8b822dc384808bb48"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def add_candidate_to_notion(name, email, tech_skills, soft_skills, experience):
    url = "https://api.notion.com/v1/pages"
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "name": {"title": [{"text": {"content": name}}]},
            "email": {"email": email},
            "technicalSkills": {"rich_text": [{"text": {"content": tech_skills}}]},
            "softSkills": {"rich_text": [{"text": {"content": soft_skills}}]},
            "yearsOfExperience": {"number": experience if experience else 0} 
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Successfully added {name} to Notion!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)