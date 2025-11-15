"""
Resume Parser using LangChain and Ollama
Extracts key information from resumes including skills, education, experience, etc.
"""

import time
import json
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from app.core.logger import logger
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from app.schemas.resume import ParsedResume

# MODEL_NAME = "mistral:7b"
MODEL_NAME = "openai/gpt-oss-120b"

load_dotenv()

class ResumeParser:
    def __init__(self, model_name: str = MODEL_NAME):
        """
        Initialize the Resume Parser with Ollama model.

        Args:
            model_name: Name of the Ollama model to use (e.g., 'llama3.2', 'mistral')
        """
        # self.llm = OllamaLLM(model=model_name, temperature=0)
        self.llm = ChatGroq(model=model_name, temperature=0)
        self.extraction_parser = PydanticOutputParser(pydantic_object=ParsedResume)
        self.extraction_prompt = self._create_extraction_prompt()
        self.chain = self.extraction_prompt | self.llm | self.extraction_parser

    def _create_extraction_prompt(self) -> PromptTemplate:
        """Create the prompt template for information extraction."""
        template = """You are an expert resume parser. Extract the following information from the resume text provided.
        Be thorough and accurate. If information is not present, use null or empty arrays as appropriate.
        
        Resume Text:
        {resume_text}
        
        Extract the information in the following JSON format and conforming to the following format instructions:
        
        {format_instructions}

        Return ONLY the JSON object, no additional text or explanation.
        """
        return PromptTemplate(
            template=template,
            input_variables=["resume_text"],
            partial_variables={"format_instructions": self.extraction_parser.get_format_instructions()}
        )

    def load_document(self, file_path: str | Path) -> str:
        """
        Load resume document from various formats.

        Args:
            file_path: Path to the resume file

        Returns:
            Extracted text content
        """
        file_path = Path(file_path.resolve())

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
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

        logger.info(f"Loading document: {file_path}")
        documents = loader.load()
        return "\n\n".join([doc.page_content for doc in documents])

    def parse_resume(self, file_path: str | Path) -> ParsedResume:
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
        try:
            logger.info(f"Parsing resume: {file_path}")
            result = self.chain.invoke({"resume_text": resume_text})
            return result
        except Exception as e:
            print(f"Error parsing resume: {e}")
            raise

    def parse_resume_text(self, resume_text: str | Path) -> Dict:
        """
        Parse resume from text directly.

        Args:
            resume_text: Resume text content

        Returns:
            Dictionary containing parsed resume information
        """
        try:
            logger.info("Parsing resume from text")
            result = self.chain.invoke({"resume_text": resume_text})
            return result
        except Exception as e:
            print(f"Error parsing resume: {e}")
            raise

    def save_parsed_data(self, parsed_data: ParsedResume, output_path: str | Path):
        """
        Save parsed resume data to JSON file.

        Args:
            parsed_data: Parsed resume dictionary
            output_path: Path to save the JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            logger.info(f"Saving parsed data to: {output_path}")
            json.dump(parsed_data.model_dump(), f, indent=2, ensure_ascii=False)
        print(f"Parsed data saved to: {output_path}")

def parse_all_resumes(parser: ResumeParser, resume_dir: Path, parsed_data_dir: Path):
    start_total = time.time()

    # ensure save dir exists
    parsed_data_dir.mkdir(parents=True, exist_ok=True)

    resume_files = list(resume_dir.glob("*"))
    logger.info(f"Found {len(resume_files)} resume files to parse.")

    for file_path in resume_files:
        if file_path.suffix.lower() not in [".pdf", ".docx", ".doc", ".txt"]:
            logger.warning(f"Skipping unsupported file: {file_path.name}")
            continue

        logger.info(f"Parsing: {file_path.name}")
        start = time.time()

        try:
            parsed_data = parser.parse_resume(file_path)
            output_file = parsed_data_dir / f"{file_path.stem}.json"
            parser.save_parsed_data(parsed_data, output_file)

            elapsed = time.time() - start
            logger.info(f"✅ Parsed {file_path.name} in {elapsed:.2f} seconds")

        except Exception as e:
            logger.error(f"❌ Failed parsing {file_path.name}: {e}")

    total_elapsed = time.time() - start_total
    logger.info(f"✅ Finished parsing all resumes in {total_elapsed:.2f} seconds total")

def main():
    parser = ResumeParser(model_name=MODEL_NAME)

    logger.info("Parse ALL resumes from directory")
    try:
        resume_dir = Path("../../sample-resumes")
        parsed_data_dir = Path("../../parsed-data")

        parse_all_resumes(parser, resume_dir, parsed_data_dir)

    except FileNotFoundError:
        logger.error("File not found.")

if __name__ == "__main__":
    main()