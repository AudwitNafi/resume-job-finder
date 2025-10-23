from pydantic import BaseModel, Field
from typing import List, Optional

# Pydantic models for structured output
class Education(BaseModel):
    degree: str = Field(description="Degree or certification obtained")
    institution: str = Field(description="Name of institution")
    year: Optional[str] = Field(description="Year or date range")
    field: Optional[str] = Field(description="Field of study")


class Experience(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    duration: Optional[str] = Field(description="Duration or date range")
    responsibilities: List[str] = Field(description="Key responsibilities and achievements")


class Certification(BaseModel):
    name: str = Field(description="Certification name")
    issuer: Optional[str] = Field(description="Issuing organization")
    year: Optional[str] = Field(description="Year obtained")


class ContactInfo(BaseModel):
    name: Optional[str] = Field(description="Full name")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    location: Optional[str] = Field(description="Location/Address")
    linkedin: Optional[str] = Field(description="LinkedIn profile")
    github: Optional[str] = Field(description="GitHub profile")


class ParsedResume(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str] = Field(description="Professional summary or objective")
    skills: List[str] = Field(description="Technical and soft skills")
    education: List[Education]
    experience: List[Experience]
    certifications: List[Certification]
    languages: List[str] = Field(description="Spoken languages")
    projects: List[str] = Field(description="Notable projects")