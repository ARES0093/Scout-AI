# Scout-AI
An autonomous AI ATS. It uses local Llama 3 for semantic skill-gap analysis on resumes, auto-routes physical PDFs into categorized folders, and syncs candidate data to Zoho CRM without duplicates.

# 🤖 AI-Powered Applicant Tracking System (ATS) Agent

> An enterprise-grade, autonomous recruitment pipeline that bridges the gap between raw candidate data and actionable HR intelligence. 

By leveraging a local Large Language Model (LLM), this system automatically ingests unstructured resumes, performs semantic skill-gap analysis against dynamic employer requirements, physically categorizes files, and synchronizes candidate statuses directly to a cloud-based CRM.

---

## 🚨 Problem Statement
Modern recruitment faces a critical bottleneck: the manual screening of resumes. HR professionals spend countless hours reading unstructured documents (PDFs, Word files) searching for specific keywords. This process is not only slow and highly susceptible to human error, but it also penalizes candidates who possess the right skills but use slightly different terminology (e.g., writing "Node.js" when the recruiter searches for "JavaScript"). Furthermore, maintaining a clean, duplicate-free candidate database across hiring sprints is a massive administrative burden.

## 💡 The Solution
We engineered an autonomous AI pipeline that acts as a digital HR assistant. Instead of relying on rigid keyword filters, the system uses semantic AI understanding to evaluate candidates contextually. 

It identifies not just what skills a candidate has, but specifically what they are missing compared to the job requirements, assigning them a match status (**Shortlisted**, **Near Match**, or **Not Shortlisted**). It then handles all administrative overhead by automatically sorting the physical resume files into corresponding folders and securely updating the company's CRM without creating duplicate records.

---

## ⚙️ Technical Approach
The architecture follows a highly decoupled Extract, Transform, Load (ETL) methodology:

* **Extraction:** A Python-based document parser bypasses file formatting to scrape raw text from incoming applications.
* **Transformation:** The unstructured text, alongside the recruiter's specific target skills, is fed into a local Llama 3 model. Through strict prompt engineering, the AI returns a standardized JSON payload detailing the candidate's profile, skill gaps, and recommended training tracks.
* **Loading (Dual-Branch):** The parsed JSON triggers two simultaneous actions. First, a local routing script physically moves the PDF into the correct status folder. Second, an API connector searches Zoho CRM by the candidate's email and executes a "Lookup & Update" protocol to cleanly merge the new intelligence into the database.

---

## ✨ Key Features
* **Semantic Skill Matching:** Moves beyond basic `CTRL+F` keyword searches to understand the context and variations of technical skills.
* **Automated Skill Gap Analysis:** Highlights exact missing requirements and suggests educational pathways for "Near Match" candidates.
* **Talent Pool Recycling:** Automatically re-evaluates previously rejected candidates against new job requirements before processing new applicants.
* **Smart File Routing:** Acts as an autonomous librarian, physically organizing thousands of resumes into distinct categorical folders on the local drive.
* **Duplicate-Free CRM Sync:** Integrates with Zoho CRM via OAuth 2.0, ensuring a single source of truth for every candidate profile.

---

## 🔄 Project Workflow
1. **Recruiter Input:** The user defines the "Target Skills" for the current hiring sprint via the interface.
2. **Data Ingestion:** The orchestrator sweeps the `/resumes` folder (new candidates) and the `/Not_Shortlisted` folder (recycling past candidates).
3. **The Eyes (Extraction):** Raw text is stripped from PDFs and DOCX files.
4. **The Brain (AI Analysis):** Llama 3 analyzes the text against the Target Skills and generates the structured JSON profile.
5. **The Hands (Execution):** 
   * **Local:** The file is copied to `/Shortlisted`, `/Near_Match`, or `/Not_Shortlisted`.
   * **Cloud:** Zoho CRM is queried via email and updated with the latest AI assessment.

---

## 🛠️ Tech Stack

**Backend Architecture:**
* **Language:** Python (3.10+)
* **AI Engine:** Llama 3 (running locally via Ollama)
* **Database/CRM:** Zoho CRM API (v3)
* **Data Processing:** `PyPDF2`, `python-docx`, `json`, `shutil`

**Frontend UI:**
* **Framework:** React.js powered by Vite
* **Styling:** Tailwind CSS
* **Interactivity:** Framer Motion (animations), React Dropzone (file handling), Lucide React (iconography)

---

## 🚀 Setup and Installation

### 1. Backend Initialization

Clone the repository to your local machine, then run the following commands:

```bash
# Install required Python dependencies
pip install -r requirements.txt

# Start the local AI server (Ensure Ollama is installed first)
ollama run llama3

# python main.py
```

## 🔮 Future Improvements
* **Explainable AI (XAI) Dashboard Integration: Surface the AI's exact reasoning for rejection directly on the frontend candidate cards to ensure ethical hiring practices.
* **Automated Candidate Communication: Integrate an SMTP protocol to automatically email "Near Match" candidates with links to the AI-recommended training courses to help them upskill.
* **FastAPI Bridge: Wrap the Python backend in a FastAPI server to allow real-time, bi-directional communication between the React drag-and-drop interface and the Llama 3 processing engine.
