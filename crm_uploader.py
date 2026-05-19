import requests
import json

# ==========================================
# 1. YOUR ZOHO CREDENTIALS (PASTE HERE)
# ==========================================
CLIENT_ID = "1000.0D133J2J20RVXTQ29558TX6UX1ML5G"
CLIENT_SECRET = "a3a1ea0125c243b1d405a4f7d51f5272f0f912b28a"
REFRESH_TOKEN = "1000.3e68ae49d6093a4b7bc1e2239959b198.07cc3e27e65e502dc02bee3c8fb668bf"

# Since you are on crm.zoho.in, we use the .in endpoints
AUTH_URL = "https://accounts.zoho.in/oauth/v2/token"
BASE_URL = "https://www.zohoapis.in/crm/v3/Contacts"

def get_access_token():
    """Silently trades the refresh token for a fresh 1-hour access token."""
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(AUTH_URL, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def add_candidate_to_zoho(candidate_data):
    """The Lookup & Update Engine"""
    access_token = get_access_token()
    if not access_token:
        print("❌ Failed to get Zoho Access Token.")
        return

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    # Extract core data
    name = candidate_data.get("name", "Unknown Candidate")
    email = candidate_data.get("email", "")
    status = candidate_data.get("matchStatus", "Not Shortlisted")
    skills = candidate_data.get("technicalSkills", [])
    
    # Format the rich text for the Description box (to show the Skill Gap analysis)
    description = f"--- LATEST AI ANALYSIS ---\nStatus: {status}\nMissing Skills: {', '.join(candidate_data.get('missingSkills', []))}\nRecommended Training: {', '.join(candidate_data.get('recommendedTraining', []))}"

    # Prepare the payload for Zoho
    record_data = {
        "Last_Name": name,
        "Email": email,
        "Technical_Skills": skills, # Change this if your API Name was different!
        "Description": description
    }

    print(f"🔄 Syncing {name} ({email}) to Zoho CRM...")

    # --- STEP 1: LOOKUP (Search by Email) ---
    search_url = f"{BASE_URL}/search?email={email}"
    search_response = requests.get(search_url, headers=headers)
    
    # --- STEP 2: UPDATE OR CREATE ---
    if search_response.status_code == 200 and search_response.json().get('data'):
        # CANDIDATE EXISTS! Let's UPDATE them.
        record_id = search_response.json()['data'][0]['id']
        update_url = f"{BASE_URL}/{record_id}"
        
        payload = {"data": [record_data]}
        update_response = requests.put(update_url, headers=headers, data=json.dumps(payload))
        
        if update_response.status_code in [200, 202]:
            print(f"✅ UPDATED existing profile for {name}.")
        else:
            print(f"❌ Failed to update {name}: {update_response.text}")
            
    else:
        # CANDIDATE IS NEW! Let's CREATE them.
        payload = {"data": [record_data]}
        create_response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        
        if create_response.status_code in [200, 201]:
            print(f"✨ CREATED brand new profile for {name}.")
        else:
            print(f"❌ Failed to create {name}: {create_response.text}")