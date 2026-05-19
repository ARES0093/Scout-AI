import os
import json
import shutil
from extractor import extract_text_from_file
from analyzer import analyze_resume 
# We will import your updated Zoho script in the next step!
from crm_uploader import add_candidate_to_zoho 

# Define your main folders
RESUME_FOLDER = "./resumes"
SORTED_FOLDER = "./sorted_resumes"

def process_all_resumes():
    print("========================================")
    print("🚀 HR AI AGENT: DYNAMIC HIRING SPRINT")
    print("========================================\n")
    
    # 1. Ask the recruiter for their target skills!
    target_skills = input("🎯 Enter Target Skills for this role (e.g. Python, React, SQL): ")
    print(f"\n⚙️ Starting pipeline for targets: [{target_skills}]...\n")
    
    for filename in os.listdir(RESUME_FOLDER):
        filepath = os.path.join(RESUME_FOLDER, filename)
        print(f"📄 Processing: {filename}")
        
        # EXTRACT
        raw_text = extract_text_from_file(filepath)
        if not raw_text:
            continue
            
        # TRANSFORM (Notice we now pass both the text AND the target skills to the AI)
        try:
            ai_json_string = analyze_resume(raw_text, target_skills)
            candidate_data = json.loads(ai_json_string) 
            status = candidate_data.get("matchStatus", "Not Shortlisted")
            
            print(f"   -> AI Status: {status}")
            if status == "Near Match":
                print(f"   -> Missing: {candidate_data.get('missingSkills')}")
                print(f"   -> Suggests: {candidate_data.get('recommendedTraining')}")
                
        except Exception as e:
            print(f"❌ Error parsing AI output for {filename}: {e}")
            continue
            
        # LOAD - Auto Routing Files based on Status
        # Create the specific folder for their status (e.g., ./sorted_resumes/Shortlisted)
        status_folder_path = os.path.join(SORTED_FOLDER, status.replace(" ", "_"))
        os.makedirs(status_folder_path, exist_ok=True)
        
        # Copy the file
        shutil.copy(filepath, os.path.join(status_folder_path, filename))
        print(f"📁 Filed in: {status_folder_path}")

        # ---------------------------------------------------------
        # PUSH TO CRM (MUST BE INDENTED HERE, INSIDE THE LOOP!)
        # ---------------------------------------------------------
        add_candidate_to_zoho(candidate_data)
        print("-" * 40) # Just prints a nice dividing line between candidates

# --- Make sure your file ends exactly like this below! ---
if __name__ == "__main__":
    process_all_resumes()
    print("✅ Hiring sprint complete!")