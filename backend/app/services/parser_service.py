"""
Resume Parser using LangChain and Ollama
Extracts key information from resumes including skills, education, experience, etc.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

class ResumeParser:
    def __init__(self, model_name: str = "mistral:7b"):
        """
        Initialize the Resume Parser with Ollama model.

        Args:
            model_name: Name of the Ollama model to use (e.g., 'llama3.2', 'mistral')
        """
        self.llm = OllamaLLM(model=model_name, temperature=0)
        self.extraction_prompt = self._create_extraction_prompt()
        self.chain = self.extraction_prompt | self.llm | StrOutputParser()

    def _create_extraction_prompt(self) -> PromptTemplate:
        """Create the prompt template for information extraction."""
        template = """You are an expert resume parser. Extract the following information from the resume text provided.
        Be thorough and accurate. If information is not present, use null or empty arrays as appropriate.
        
        Resume Text:
        {resume_text}
        
        Extract the information in the following JSON format:
        {{
            "contact_info": {{
                "name": "Full name",
                "email": "email@example.com",
                "phone": "+1234567890",
                "location": "City, State/Country",
                "linkedin": "LinkedIn URL",
                "github": "GitHub URL"
            }},
            "summary": "Professional summary or objective statement",
            "skills": ["skill1", "skill2", "skill3"],
            "education": [
                {{
                    "degree": "Degree name",
                    "institution": "University/College name",
                    "year": "2020-2024 or 2024",
                    "field": "Field of study"
                }}
            ],
            "experience": [
                {{
                    "title": "Job title",
                    "company": "Company name",
                    "duration": "Jan 2020 - Present",
                    "responsibilities": ["responsibility1", "responsibility2"]
                }}
            ],
            "certifications": [
                {{
                    "name": "Certification name",
                    "issuer": "Issuing organization",
                    "year": "2023"
                }}
            ],
            "languages": ["English", "Spanish"],
            "projects": ["Project name and brief description"]
        }}

Return ONLY the JSON object, no additional text or explanation.
"""
        return PromptTemplate(template=template, input_variables=["resume_text"])

    def load_document(self, file_path: str) -> str:
        """
        Load resume document from various formats.

        Args:
            file_path: Path to the resume file

        Returns:
            Extracted text content
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Select appropriate loader based on file extension
        if file_path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(str(file_path))
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            loader = Docx2txtLoader(str(file_path))
        elif file_path.suffix.lower() == '.txt':
            loader = TextLoader(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        documents = loader.load()
        return "\n\n".join([doc.page_content for doc in documents])

    def parse_resume(self, file_path: str) -> Dict:
        """
        Parse resume and extract structured information.

        Args:
            file_path: Path to the resume file

        Returns:
            Dictionary containing parsed resume information
        """
        # Load document
        resume_text = self.load_document(file_path)

        # Extract information using LLM
        result = self.chain.invoke({"resume_text": resume_text})

        # Clean and parse JSON response
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()

        try:
            parsed_data = json.loads(result)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {result}")
            raise

    def parse_resume_text(self, resume_text: str) -> Dict:
        """
        Parse resume from text directly.

        Args:
            resume_text: Resume text content

        Returns:
            Dictionary containing parsed resume information
        """
        result = self.chain.invoke({"resume_text": resume_text})

        # Clean and parse JSON response
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()

        try:
            parsed_data = json.loads(result)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {result}")
            raise

    def save_parsed_data(self, parsed_data: Dict, output_path: str):
        """
        Save parsed resume data to JSON file.

        Args:
            parsed_data: Parsed resume dictionary
            output_path: Path to save the JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        print(f"Parsed data saved to: {output_path}")

    def print_summary(self, parsed_data: Dict):
        """
        Print a formatted summary of parsed resume data.

        Args:
            parsed_data: Parsed resume dictionary
        """
        print("\n" + "=" * 60)
        print("RESUME PARSING RESULTS")
        print("=" * 60)

        # Contact Info
        if parsed_data.get('contact_info'):
            print("\n📧 CONTACT INFORMATION:")
            contact = parsed_data['contact_info']
            if contact.get('name'):
                print(f"  Name: {contact['name']}")
            if contact.get('email'):
                print(f"  Email: {contact['email']}")
            if contact.get('phone'):
                print(f"  Phone: {contact['phone']}")
            if contact.get('location'):
                print(f"  Location: {contact['location']}")
            if contact.get('linkedin'):
                print(f"  LinkedIn: {contact['linkedin']}")
            if contact.get('github'):
                print(f"  GitHub: {contact['github']}")

        # Summary
        if parsed_data.get('summary'):
            print(f"\n📝 SUMMARY:\n  {parsed_data['summary']}")

        # Skills
        if parsed_data.get('skills'):
            print(f"\n💡 SKILLS ({len(parsed_data['skills'])}):")
            for skill in parsed_data['skills']:
                print(f"  • {skill}")

        # Education
        if parsed_data.get('education'):
            print(f"\n🎓 EDUCATION ({len(parsed_data['education'])}):")
            for edu in parsed_data['education']:
                print(f"  • {edu.get('degree', 'N/A')} - {edu.get('institution', 'N/A')}")
                if edu.get('field'):
                    print(f"    Field: {edu['field']}")
                if edu.get('year'):
                    print(f"    Year: {edu['year']}")

        # Experience
        if parsed_data.get('experience'):
            print(f"\n💼 EXPERIENCE ({len(parsed_data['experience'])}):")
            for exp in parsed_data['experience']:
                print(f"  • {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                if exp.get('duration'):
                    print(f"    Duration: {exp['duration']}")
                if exp.get('responsibilities'):
                    print(f"    Key Responsibilities: {len(exp['responsibilities'])} items")

        # Certifications
        if parsed_data.get('certifications'):
            print(f"\n📜 CERTIFICATIONS ({len(parsed_data['certifications'])}):")
            for cert in parsed_data['certifications']:
                print(f"  • {cert.get('name', 'N/A')}", end="")
                if cert.get('issuer'):
                    print(f" - {cert['issuer']}", end="")
                if cert.get('year'):
                    print(f" ({cert['year']})", end="")
                print()

        # Languages
        if parsed_data.get('languages'):
            print(f"\n🌐 LANGUAGES: {', '.join(parsed_data['languages'])}")

        # Projects
        if parsed_data.get('projects'):
            print(f"\n🚀 PROJECTS ({len(parsed_data['projects'])}):")
            for project in parsed_data['projects']:
                print(f"  • {project}")

        print("\n" + "=" * 60 + "\n")


# Example usage
def main():
    # Initialize parser
    parser = ResumeParser(model_name="mistral:7b")

    # Example 1: Parse from file
    print("Example: Parsing resume from file...")
    try:
        resume_file = "sample_resume.pdf"  # Change to your file path
        parsed_data = parser.parse_resume(resume_file)

        # Print summary
        parser.print_summary(parsed_data)

        # Save to JSON
        parser.save_parsed_data(parsed_data, "parsed_resume.json")

    except FileNotFoundError:
        print(f"File not found. Skipping file parsing example.")

    # Example 2: Parse from text
    # print("\nExample: Parsing resume from text...")
    # sample_resume_text = """
    # John Doe
    # Email: john.doe@email.com | Phone: +1-555-0123
    # Location: San Francisco, CA | LinkedIn: linkedin.com/in/johndoe
    #
    # PROFESSIONAL SUMMARY
    # Experienced software engineer with 5+ years in full-stack development.
    #
    # SKILLS
    # Python, JavaScript, React, Node.js, Docker, Kubernetes, AWS, MongoDB
    #
    # EXPERIENCE
    # Senior Software Engineer | Tech Corp | Jan 2021 - Present
    # - Led development of microservices architecture serving 1M+ users
    # - Reduced API response time by 40% through optimization
    #
    # Software Engineer | StartupXYZ | Jun 2019 - Dec 2020
    # - Built RESTful APIs using Python and Flask
    # - Implemented CI/CD pipelines with Jenkins
    #
    # EDUCATION
    # Bachelor of Science in Computer Science
    # University of California, Berkeley | 2015 - 2019
    #
    # CERTIFICATIONS
    # - AWS Certified Solutions Architect | Amazon Web Services | 2022
    # - Certified Kubernetes Administrator | CNCF | 2023
    # """
    #
    # parsed_data = parser.parse_resume_text(sample_resume_text)
    # parser.print_summary(parsed_data)
    # parser.save_parsed_data(parsed_data, "sample_parsed_resume.json")


if __name__ == "__main__":
    main()