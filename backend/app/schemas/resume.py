from pydantic import BaseModel, Field
from typing import List, Optional

# Pydantic models for structured output
class Education(BaseModel):
    degree: Optional[str] = Field(default=None, description="Degree or certification obtained")
    institution: Optional[str] = Field(default=None, description="Name of institution")
    year: Optional[str] = Field(default=None, description="Year or date range")
    field: Optional[str] = Field(default=None, description="Field of study")


class Experience(BaseModel):
    title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    duration: Optional[str] = Field(default=None, description="Duration or date range")
    responsibilities: Optional[List[str]] = Field(default=None, description="Key responsibilities and achievements")


class Certification(BaseModel):
    name: Optional[str] = Field(default=None, description="Certification name")
    issuer: Optional[str] = Field(default=None, description="Issuing organization")
    year: Optional[str] = Field(default=None, description="Year obtained")


class Project(BaseModel):
    name: Optional[str] = Field(default=None, description="Project name")
    description: Optional[str] = Field(default=None, description="Project description")
    technologies: Optional[List[str]] = Field(default_factory=list, description="Technologies used")
    url: Optional[str] = Field(default=None, description="Project URL or repository")


class ContactInfo(BaseModel):
    name: Optional[str] = Field(default=None, description="Full name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="Location/Address")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile")
    github: Optional[str] = Field(default=None, description="GitHub profile")


class ParsedResume(BaseModel):
    contact_info: Optional[ContactInfo] = Field(default=None, description="Contact information")
    summary: Optional[str] = Field(default=None, description="Professional summary or objective")
    skills: Optional[List[str]] = Field(default_factory=list, description="Technical and soft skills")
    education: Optional[List[Education]] = Field(default_factory=list, description="Education history")
    experience: Optional[List[Experience]] = Field(default_factory=list, description="Work experience")
    certifications: Optional[List[Certification]] = Field(default_factory=list, description="Certifications")
    languages: Optional[List[str]] = Field(default_factory=list, description="Spoken languages")
    projects: Optional[List[Project]] = Field(default_factory=list, description="Notable projects")
