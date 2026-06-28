import random
import re


def analyze_sentiment(text):
    positive_words = ["innovative", "revolutionary", "disruptive", "scalable", "sustainable",
                      "efficient", "user-friendly", "impactful", "game-changing", "pioneering",
                      "unique", "transformative", "breakthrough", "visionary"]
    negative_words = ["expensive", "complex", "difficult", "risky", "uncertain",
                      "limited", "outdated", "inefficient", "expensive", "slow"]
    text_lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    total = pos_count + neg_count
    if total == 0:
        return {"sentiment": "Neutral", "score": 50, "positive_words": pos_count, "negative_words": neg_count}
    score = int((pos_count / total) * 100)
    if score >= 70:
        sentiment = "Very Positive"
    elif score >= 50:
        sentiment = "Positive"
    elif score >= 30:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    return {"sentiment": sentiment, "score": score, "positive_words": pos_count, "negative_words": neg_count}


def generate_tags(idea):
    tags = set()
    industry_tag = idea.get_industry_display()
    tags.add(industry_tag)
    tags.add("Startup")
    if idea.business_model:
        bm_lower = idea.business_model.lower()
        if "saas" in bm_lower or "subscription" in bm_lower:
            tags.add("SaaS")
            tags.add("Subscription")
        if "marketplace" in bm_lower:
            tags.add("Marketplace")
        if "ecommerce" in bm_lower or "e-commerce" in bm_lower:
            tags.add("E-Commerce")
        if "advertising" in bm_lower or "advertisement" in bm_lower:
            tags.add("Advertising")
    if idea.target_customers:
        tc_lower = idea.target_customers.lower()
        if "b2b" in tc_lower or "business" in tc_lower:
            tags.add("B2B")
        if "b2c" in tc_lower or "consumer" in tc_lower:
            tags.add("B2C")
    words = re.findall(r'\b\w+\b', idea.problem_statement + " " + idea.proposed_solution)
    tech_keywords = ["ai", "machine learning", "blockchain", "iot", "cloud", "mobile",
                     "web", "data", "analytics", "automation", "digital", "platform"]
    for kw in tech_keywords:
        if kw in " ".join(words).lower():
            tags.add(kw.title())
    return list(tags)[:8]


def generate_legal_checklist(idea):
    industry = idea.get_industry_display().lower()
    checklist = [
        {"item": "Business Registration & Incorporation", "required": True, "status": "pending"},
        {"item": "Tax Registration (GST/VAT/Income Tax)", "required": True, "status": "pending"},
        {"item": "Trademark Registration (Business Name & Logo)", "required": True, "status": "pending"},
        {"item": "Terms of Service Agreement", "required": True, "status": "pending"},
        {"item": "Privacy Policy (GDPR/CCPA compliant)", "required": True, "status": "pending"},
    ]
    if "technology" in industry or "software" in industry:
        checklist.append({"item": "Software License Agreement (EULA)", "required": True, "status": "pending"})
        checklist.append({"item": "Data Processing Agreement (DPA)", "required": True, "status": "pending"})
    if "health" in industry or "healthcare" in industry:
        checklist.append({"item": "HIPAA Compliance Certification", "required": True, "status": "pending"})
        checklist.append({"item": "Medical Device Clearance (FDA)", "required": False, "status": "pending"})
    if "finance" in industry or "fintech" in industry:
        checklist.append({"item": "SEC/FCA Registration", "required": True, "status": "pending"})
        checklist.append({"item": "Anti-Money Laundering (AML) Policy", "required": True, "status": "pending"})
    if idea.business_model:
        bm_lower = idea.business_model.lower()
        if "marketplace" in bm_lower:
            checklist.append({"item": "Marketplace Seller Agreement", "required": True, "status": "pending"})
        if "subscription" in bm_lower:
            checklist.append({"item": "Subscription Billing Terms", "required": True, "status": "pending"})
    checklist.append({"item": "Employment/Contractor Agreements", "required": True, "status": "pending"})
    checklist.append({"item": "Non-Disclosure Agreement (NDA)", "required": True, "status": "pending"})
    if idea.required_investment > 10000:
        checklist.append({"item": "Investor Agreements & Shareholder Documents", "required": True, "status": "pending"})
        checklist.append({"item": "Intellectual Property Assignment Agreement", "required": True, "status": "pending"})
    return checklist


def generate_terms_and_conditions(idea):
    company_name = idea.startup_name
    industry = idea.get_industry_display()
    return f"""
Terms and Conditions

Last Updated: {__import__('datetime').date.today().strftime('%B %d, %Y')}

1. INTRODUCTION
Welcome to {company_name} ("Company," "we," "our," "us"). These Terms and Conditions ("Terms") govern your use of our services, website, and platform.

2. ACCEPTANCE
By accessing or using {company_name}, you agree to be bound by these Terms. If you disagree, please do not use our services.

3. SERVICES DESCRIPTION
{company_name} provides {industry}-related solutions and services. We reserve the right to modify or discontinue services at any time.

4. USER OBLIGATIONS
- You must be at least 18 years old to use our services.
- You agree to provide accurate and complete information.
- You are responsible for maintaining the confidentiality of your account.

5. INTELLECTUAL PROPERTY
All content, trademarks, and intellectual property on our platform are owned by {company_name} unless otherwise stated. You may not reproduce, distribute, or create derivative works without our consent.

6. PAYMENT AND SUBSCRIPTION
Any fees, payment terms, and billing cycles will be as described during the checkout process. All payments are non-refundable unless otherwise stated.

7. LIMITATION OF LIABILITY
{company_name} shall not be liable for any indirect, incidental, or consequential damages arising from your use of our services.

8. TERMINATION
We may terminate or suspend your access immediately if you violate these Terms.

9. GOVERNING LAW
These Terms shall be governed by the laws of the jurisdiction in which {company_name} operates.

10. CHANGES TO TERMS
We reserve the right to update these Terms at any time. Continued use after changes constitutes acceptance.

11. CONTACT
For questions about these Terms, please contact us at legal@{company_name.lower().replace(' ', '')}.com
"""


def analyze_pitch_deck(idea):
    scores = {}
    if idea.problem_statement and len(idea.problem_statement) > 50:
        scores["problem_clarity"] = min(100, int(len(idea.problem_statement) * 0.4))
    else:
        scores["problem_clarity"] = 30
    if idea.proposed_solution and len(idea.proposed_solution) > 50:
        scores["solution_clarity"] = min(100, int(len(idea.proposed_solution) * 0.4))
    else:
        scores["solution_clarity"] = 30
    if idea.unique_selling_proposition and len(idea.unique_selling_proposition) > 30:
        scores["usp_strength"] = min(100, int(len(idea.unique_selling_proposition) * 0.5))
    else:
        scores["usp_strength"] = 20
    if idea.business_model and len(idea.business_model) > 50:
        scores["business_model"] = min(100, int(len(idea.business_model) * 0.35))
    else:
        scores["business_model"] = 25
    if idea.target_customers and len(idea.target_customers) > 30:
        scores["market_understanding"] = min(100, int(len(idea.target_customers) * 0.5))
    else:
        scores["market_understanding"] = 20
    if idea.competitor_analysis and len(idea.competitor_analysis) > 50:
        scores["competitive_awareness"] = min(100, int(len(idea.competitor_analysis) * 0.3))
    else:
        scores["competitive_awareness"] = 15
    overall = int(sum(scores.values()) / len(scores)) if scores else 0
    suggestions = []
    if scores.get("problem_clarity", 0) < 50:
        suggestions.append("Strengthen your problem statement with specific data points and real-world examples.")
    if scores.get("usp_strength", 0) < 50:
        suggestions.append("Clearly articulate what makes your solution unique and why customers would choose you.")
    if scores.get("business_model", 0) < 50:
        suggestions.append("Provide more detail on your revenue streams and pricing strategy.")
    if scores.get("competitive_awareness", 0) < 40:
        suggestions.append("Include a detailed competitive analysis with direct comparisons.")
    return {"scores": scores, "overall": overall, "suggestions": suggestions, "has_pitch_deck": bool(idea.pitch_deck)}


def analyze_elevator_pitch(text):
    word_count = len(text.split())
    time_estimate = max(15, word_count * 3)
    analysis = {}
    if word_count < 30:
        analysis["length"] = "Too short - aim for 50-100 words"
        analysis["length_score"] = 40
    elif word_count > 150:
        analysis["length"] = "Too long - aim for 50-100 words"
        analysis["length_score"] = 50
    else:
        analysis["length"] = "Good length for an elevator pitch"
        analysis["length_score"] = 90
    time_words = ["problem", "solution", "unique", "market", "customer"]
    found_words = sum(1 for w in time_words if w in text.lower())
    analysis["key_elements"] = f"Contains {found_words}/5 key pitch elements"
    analysis["structure_score"] = min(100, found_words * 20)
    sentiment = analyze_sentiment(text)
    analysis["sentiment"] = sentiment
    confident_words = ["we will", "we can", "we are", "our solution", "we solve"]
    uncertain_words = ["maybe", "perhaps", "hopefully", "might", "could"]
    confidence = sum(1 for w in confident_words if w in text.lower())
    uncertainty = sum(1 for w in uncertain_words if w in text.lower())
    analysis["confidence_score"] = min(100, max(0, 50 + confidence * 10 - uncertainty * 10))
    analysis["time_seconds"] = time_estimate
    analysis["word_count"] = word_count
    analysis["overall_score"] = int((analysis["length_score"] + analysis["structure_score"] + analysis["confidence_score"]) / 3)
    return analysis
