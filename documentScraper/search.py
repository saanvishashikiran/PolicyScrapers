from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

KEYWORD_CATEGORIES = {
    "Infrastructure": [
        "Artificial Intelligence", "GenAI", "AI infrastructure", "cloud computing", "data centers",
        "edge computing", "AI accelerators", "GPU", "high-performance computing", "storage infrastructure",
        "distributed systems", "scalability", "cybersecurity", "data privacy",
        "Secure Identity and Access Management", "Data Governance", "Wireless infrastructure",
        "modernization", "energy infrastructure", "critical infrastructure"
    ],
    "Environment": [
        "Artificial Intelligence", "AI", "sustainable AI", "environmental impact", "green computing",
        "GHG emissions", "carbon footprint", "greenhouse gas emissions", "public disclosure",
        "transparency", "reporting requirements", "protocol standards", "verification", "responsible AI",
        "algorithm transparency", "digital sustainability", "corporate emissions", "measurement"
    ],
    "Perception": [
        "Perception", "Artificial Intelligence", "AI", "trust", "fear", "expectations", "attitudes",
        "acceptance", "public opinion", "ethics", "transparency", "misconceptions"
    ],
    "Security": [
        "Artificial Intelligence", "AI", "Cybersecurity", "Security", "Privacy", "Data privacy",
        "Risk Assessment", "Risk Management", "Data protection", "Data breach", "Authentication",
        "Encryption", "Access control", "Anomaly detection", "Malware detection", "Intrusion detection",
        "Threat intelligence", "Unauthorized access", "Information safeguarding", "Human oversight"
    ],
    "Education": [
        "Artificial Intelligence", "AI", "Education", "AI education", "AI literacy",
        "professional development", "workforce", "curriculum", "personalized learning",
        "adaptive learning", "instructional resources", "critical thinking", "STEM",
        "educational outcomes", "grant programs", "learning pathways", "postsecondary education",
        "machine learning"
    ],
    "Accessibility": [
        "Artificial Intelligence", "Accessibility", "AI Protections", "Safeguards",
        "Accountability", "Underrepresented students", "accessibility", "standards",
        "Web Content Accessibility Guidelines", "compliance", "Digital Divide", "Digital Inclusion",
        "Equitable AI", "Universal Access", "Affordability", "Technological Literacy",
        "Broadband access", "Internet connectivity", "Remote regions"
    ],
    "Equity and Diversity": [
        "Artificial Intelligence", "AI", "Equity", "Diversity", "Bias", "Anti-bias Testing",
        "Algorithmic Fairness", "Inclusion", "Discrimination", "Fairness", "Ethics",
        "Algorithmic Bias", "Equity in AI", "Diversity and Inclusion", "Protected Characteristic",
        "Unlawful Discrimination", "Underrepresented Communities", "Bias Mitigation",
        "Algorithmic Transparency", "Disparate Impact", "Inclusive Design",
        "Equitable Outcomes", "Ethical AI"
    ],
    "Data": [
        "Artificial Intelligence", "AI", "Data", "Generative AI", "Training Data", "Datasets",
        "Synthetic Data", "Data Collection", "Data Processing", "Data Quality", "Data Governance",
        "Data Privacy", "Data Ownership", "Data Sources", "Transparency", "Compliance",
        "Machine Learning", "Data Accessibility"
    ]
}

CATEGORY_DEFINITIONS = {
    "Infrastructure": "Infrastructure refers to the physical and digital systems—such as computing power, data centers, broadband networks, and cloud platforms—required to develop, deploy, and scale AI technologies.",
    "Environment": "Environment includes the ecological and sustainability impacts of AI development and deployment, including emissions, green computing practices, and regulatory transparency.",
    "Perception": "Perception refers to how the public and stakeholders view and understand AI, including ethical concerns, transparency, and trust.",
    "Security": "Security addresses the risks and protections related to AI systems, including cybersecurity, data protection, and risk management.",
    "Education": "Education concerns the development of AI literacy, educational infrastructure, and workforce readiness in AI-related fields.",
    "Accessibility": "Accessibility addresses ensuring equitable access to AI benefits, compliance with accessibility standards, and inclusion of underrepresented populations.",
    "Equity and Diversity": "Equity and Diversity involves ensuring that AI systems are fair, inclusive, and free from bias or discrimination.",
    "Data": "Data refers to the foundations of AI development, including data collection, processing, governance, and transparency."
}

def parse_output(text):
    return [url.strip() for url in text.strip().split('\n') if url.strip()]

def search_policy_links(category, state):
    keywords = KEYWORD_CATEGORIES.get(category)
    if not keywords:
        raise ValueError(f"Unsupported category: {category}")

    category_definition = CATEGORY_DEFINITIONS[category]
    keyword = keywords[0]  

    prompt = (
        f"Please provide a list of policy documents from government sources in {state} relating to Artificial Intelligence, {category}, and {keyword}. "
        f"{category} is defined as follows: {category_definition}. "
        f"Return only policy documents that are PDF sources from government websites. A policy document is a policy passed by the state Senate or Assembly, "
        f"or an Executive Order signed by the Governor, or a policy enacted by a state agency. Return only the URLs separated by line. Include no other text. Make sure these documents are from the last 10 years."
    )

    response = client.responses.create(
        model="gpt-4.1",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "US",
                "region": state,
            }
        }],
        input=prompt,
    )

    response_text = response.output_text.strip()
    urls = [url.strip() for url in response_text.split('\n') if url.strip()]

    return urls

