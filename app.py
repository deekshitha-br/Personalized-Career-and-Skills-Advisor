import streamlit as st
import re
from difflib import SequenceMatcher
import matplotlib.pyplot as plt

# Expanded abbreviation dictionary
ABBREVIATION_MAP = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "ds": "data science",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "db": "databases",
    "js": "javascript",
    "seo": "search engine optimization",
    "k8s": "kubernetes",
    "pm": "product management",
    # add more
}

CAREER_DB = [
    {
        "name": "Data Scientist",
        "skills": ["python", "statistics", "machine learning", "data visualization", "sql", "deep learning"],
        "description": "Work with data to extract valuable insights and build predictive models using advanced techniques.",
        "courses": [
            {"name": "Python for Data Science", "duration_weeks": 4},
            {"name": "Statistics and Probability", "duration_weeks": 6},
            {"name": "Machine Learning A-Z", "duration_weeks": 8},
            {"name": "Deep Learning Specialization", "duration_weeks": 10},
        ]
    },
    {
        "name": "Cloud Engineer",
        "skills": ["cloud computing", "kubernetes", "docker", "networking", "security"],
        "description": "Design and manage scalable cloud infrastructure and services.",
        "courses": [
            {"name": "Cloud Fundamentals", "duration_weeks": 4},
            {"name": "Kubernetes Basics", "duration_weeks": 5},
            {"name": "Cloud Security Essentials", "duration_weeks": 6},
        ]
    },
    {
        "name": "Product Manager",
        "skills": ["communication", "agile", "user experience", "leadership", "market analysis"],
        "description": "Lead product development cycles and align with customer needs and market trends.",
        "courses": [
            {"name": "Agile Project Management", "duration_weeks": 4},
            {"name": "User Experience Fundamentals", "duration_weeks": 5},
            {"name": "Business Analytics", "duration_weeks": 6},
        ]
    },
    {
        "name": "Cybersecurity Analyst",
        "skills": ["network security", "threat analysis", "incident response", "firewalls", "cryptography"],
        "description": "Protect computer networks from cyber threats and breaches.",
        "courses": [
            {"name": "Cybersecurity Fundamentals", "duration_weeks": 5},
            {"name": "Network Defense Techniques", "duration_weeks": 6},
            {"name": "Ethical Hacking", "duration_weeks": 8},
        ]
    },
    {
        "name": "AI Research Scientist",
        "skills": ["python", "machine learning", "deep learning", "research methodology", "data mining"],
        "description": "Conduct research to create novel AI algorithms and improve existing methods.",
        "courses": [
            {"name": "Advanced Machine Learning", "duration_weeks": 10},
            {"name": "Neural Networks and Deep Learning", "duration_weeks": 8},
            {"name": "Research Methods in AI", "duration_weeks": 6},
        ]
    },
    {
        "name": "Graphic Designer",
        "skills": ["photoshop", "illustrator", "creativity", "typography", "ui design"],
        "description": "Create visual concepts to communicate ideas prompting audience engagement.",
        "courses": [
            {"name": "Graphic Design Basics", "duration_weeks": 3},
            {"name": "Adobe Photoshop Masterclass", "duration_weeks": 4},
            {"name": "UI Design Principles", "duration_weeks": 5},
        ]
    },
    {
        "name": "Business Analyst",
        "skills": ["data analysis", "communication", "requirements gathering", "sql", "stakeholder management"],
        "description": "Analyze business needs, collect requirements, and help implement solutions.",
        "courses": [
            {"name": "Business Analysis Fundamentals", "duration_weeks": 4},
            {"name": "Data Analysis with SQL", "duration_weeks": 5},
            {"name": "Effective Communication Skills", "duration_weeks": 3},
        ]
    },
    {
        "name": "Mobile App Developer",
        "skills": ["java", "kotlin", "swift", "react native", "ui/ux"],
        "description": "Build and maintain mobile applications for Android and iOS platforms.",
        "courses": [
            {"name": "Java Programming for Android", "duration_weeks": 6},
            {"name": "iOS App Development with Swift", "duration_weeks": 6},
            {"name": "Cross-platform Development in React Native", "duration_weeks": 5},
        ]
    }
]
def expand_abbreviations(text):
    words = re.split(r'\W+', text.lower())
    expanded_words = [ABBREVIATION_MAP.get(w, w) for w in words]
    return expanded_words

def normalize_skills(skills):
    # Lowercase and expand abbreviations
    normalized = set()
    for skill in skills:
        skill = skill.strip().lower()
        expanded = ABBREVIATION_MAP.get(skill, skill)
        normalized.add(expanded)
    return normalized

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def match_skills(user_skills, career_skills, threshold=0.6):
    # Match skills loosely using similarity score
    matched = set()
    for cskill in career_skills:
        for uskill in user_skills:
            if similar(uskill, cskill) > threshold:
                matched.add(cskill)
                break
    return matched

def plot_skill_gaps(career_name, matched, career_skills):
    missing = set(career_skills) - matched
    labels = ['Matched Skills', 'Missing Skills']
    sizes = [len(matched), len(missing)]
    colors = ['#4CAF50', '#F44336']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    plt.title(f'Skill Match for {career_name}')
    st.pyplot(fig)
    st.write(f"Missing Skills: {', '.join(missing)}")

def generate_career_statement(user_profile, best_career):
    statement = (
        f"As an individual with education level {user_profile['education']}, "
        f"possessing skills in {', '.join(sorted(user_profile['skills']))}, "
        f"and interested in {', '.join(sorted(user_profile['interests']))}, "
        f"I aim to excel as a {best_career['name']}."
    )
    return statement

# Streamlit App

st.set_page_config(page_title="Advanced NextGen AI Career Advisor", layout="wide")
st.title("Advanced NextGen AI Career Advisor")

if "profile" not in st.session_state:
    st.session_state.profile = {"skills": set(), "interests": set(), "education": ""}

def input_profile():
    st.header("Step 1: Tell us about Yourself")
    raw_skills = st.text_input("Enter your skills (comma or space separated)", "")
    raw_interests = st.text_input("Enter your interests (comma or space separated)", "")
    education = st.selectbox("Select your highest education level", ["High School", "Bachelor's", "Master's", "PhD"])

    if st.button("Save Profile"):
        skills_expanded = expand_abbreviations(raw_skills)
        interests_expanded = expand_abbreviations(raw_interests)
        st.session_state.profile["skills"] = normalize_skills(skills_expanded)
        st.session_state.profile["interests"] = normalize_skills(interests_expanded)
        st.session_state.profile["education"] = education
        st.success("Profile saved!")

def career_analysis():
    if not st.session_state.profile["skills"]:
        st.warning("Please enter and save your profile first.")
        return

    st.header("Step 2: Career Recommendations")

    career_matches = []
    for career in CAREER_DB:
        matched_skills = match_skills(st.session_state.profile["skills"], career["skills"])
        score = len(matched_skills) / len(career["skills"])
        career_matches.append((career, matched_skills, score))

    # Sort by best match
    career_matches.sort(key=lambda x: x[2], reverse=True)
    
    for career, matched, score in career_matches[:3]:
        st.subheader(f"{career['name']} - Match Score: {score:.2f}")
        st.write(career["description"])
        plot_skill_gaps(career['name'], matched, career['skills'])
        st.write("Recommended Courses and Timeline:")
        for course in career["courses"]:
            st.write(f"- {course['name']} (~{course['duration_weeks']} weeks)")
        st.markdown("---")

    # Career Identity Statement
    best_career = career_matches[0][0]
    cis = generate_career_statement(st.session_state.profile, best_career)
    st.header("Career Identity Statement")
    st.info(cis)

# Flow
if "profile_done" not in st.session_state:
    input_profile()
    if st.session_state.get("profile") and st.session_state["profile"]["skills"]:
        st.session_state["profile_done"] = True
else:
    career_analysis()
    if st.button("Edit Profile"):
        st.session_state["profile_done"] = False
