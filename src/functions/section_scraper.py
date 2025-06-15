from PyPDF2 import PdfReader

import re
import os

class SectionScraper:
    '''Scrapes sections out of PDF dumps'''

    skill_sections = [
        "skills",
        "skill highlights",
        "summary of skills",
    ]

    experience_sections = [
        "work history",
        "work experience",
        "experience",
        "professional experience",
        "professional history",
    ]

    education_sections = [
        "education",
        "education and training",
        "educational background",
    ]

    sections = skill_sections + experience_sections + education_sections + [
        "summary",
        "highlights",
        "professional summary",
        "core qualifications",
        "languages",
        "professional profile",
        "relevant experience",
        "affiliations",
        "certifications",
        "qualifications",
        "accomplishments",
        "additional information",
        "core accomplishments",
        "career overview",
        "core strengths",
        "interests",
        "professional affiliations",
        "online profile",
        "certifications and trainings",
        "credentials",
        "personal information",
        "career focus",
        "executive profile",
        "military experience",
        "community service",
        "presentasions",
        "publications",
        "community leadership positions",
        "license",
        "computer skills",
        "presentations",
        "volunteer work",
        "awards and publications",
        "activities and honors",
        "volunteer associations"
    ]
    
    def _read(self, cv_path) -> str:
        path = os.path.abspath(f"../{cv_path}")
        reader = PdfReader(path)

        text = ""
        for page in reader.pages:
            text = "\n".join([text, page.extract_text()])
        
        return text

    def scrape_skills(self, cv_path: str) -> str:
        text = self._read(cv_path)
        res = re.search(f"\n({'|'.join(self.skill_sections)})\n(.*\n)*?({'|'.join(self.sections)})?(\n|$)", text, re.IGNORECASE)
        if res:
            i, j = res.span()
            return text[i:j]
        else:
            return ""

    def scrape_experience(self, cv_path: str) -> str:
        text = self._read(cv_path)
        res = re.search(f"\n({'|'.join(self.experience_sections)})\n(.*\n)*?({'|'.join(self.sections)})?(\n|$)", text, re.IGNORECASE)
        if res:
            i, j = res.span()
            return text[i:j]
        else:
            return ""

    def scrape_education(self, cv_path: str) -> str:
        text = self._read(cv_path)
        res = re.search(f"\n({'|'.join(self.education_sections)})\n(.*\n)*?({'|'.join(self.sections)})?(\n|$)", text, re.IGNORECASE)
        if res:
            i, j = res.span()
            return text[i:j]
        else:
            return ""