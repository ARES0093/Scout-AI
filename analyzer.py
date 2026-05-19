import ollama

def analyze_resume(raw_text, target_skills):
    # Notice we added 'target_skills' as an input variable!
    
    prompt = f"""
    You are an elite Technical HR Recruiter and AI Assessor. 
    The employer is looking for a candidate with the following TARGET SKILLS: {target_skills}

    Read the candidate's resume below. Compare their actual skills to the TARGET SKILLS to determine their Match Status.
    - If they have 80% or more of the target skills, status is 'Shortlisted'.
    - If they have 40% to 79% of the target skills, status is 'Near Match'.
    - If they have less than 40%, status is 'Not Shortlisted'.

    You MUST return ONLY a valid JSON object using exactly this blueprint:
    {{
        "name": "Extract name here, or 'Name Missing'",
        "email": "Extract email here, or 'Email Missing'",
        "technicalSkills": ["List ALL technical skills found on the resume"],
        "matchStatus": "Shortlisted | Near Match | Not Shortlisted",
        "missingSkills": ["List the specific TARGET SKILLS the candidate is missing"],
        "recommendedTraining": ["Suggest 1 or 2 specific course titles or topics to help them learn the missing skills"]
    }}

    Resume Text:
    {raw_text}
    """

    print("🧠 Sending text to Llama 3 for Skill Gap Analysis...")
    
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ], format='json')
    
    return response['message']['content']

# --- Testing the pipeline ---
if __name__ == "__main__":
    sample_file = "sample_resume.pdf" # Make sure this file is in your folder
    
    try:
        # 1. Extract text using the code we wrote earlier
        raw_text = extract_text_from_pdf(sample_file)
        
        # 2. Analyze the text using Llama 3
        ai_result = analyze_resume(raw_text)
        
        print("\n--- AI Extraction Result ---")
        print(ai_result)
        
    except FileNotFoundError:
        print(f"Error: Please ensure '{sample_file}' is in your folder.")