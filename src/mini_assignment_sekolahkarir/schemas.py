
from pydantic import BaseModel, Field
from typing import Literal


class Education(BaseModel):
    institution: str

    degree: str | None = Field(
        description=(
            "Academic degree or qualification level, "
            "such as Bachelor, Master, or Diploma. "
            "Exclude the field of study."
        )
    )

    field_of_study: str | None = Field(
        description=(
            "Academic major or discipline, such as "
            "Computer Science, Software Engineering, "
            "or Information Systems. Extract it even "
            "when included in the degree title."
        )
    )

    graduation_year: int | None


class Experience(BaseModel):
    organization: str
    role: str
    start_date: str | None
    end_date: str | None
    description: list[str]


class Project(BaseModel):
    name: str
    role: str | None
    technologies: list[str]
    description: list[str]


class Certification(BaseModel):
    name: str
    issuer: str | None
    year: int | None


class CandidateProfile(BaseModel):
    name: str | None

    education: list[Education]
    skills: list[str]
    experience: list[Experience]
    projects: list[Project]
    certifications: list[Certification]

    extraction_caveats: list[str] = Field(
        description="Missing or ambiguous information from the CV"
    )

class CandidateOverview(BaseModel):
    summary: str = Field(
        description=(
            "A concise, factual summary of the candidate's "
            "education, technical skills, experience, and projects. "
            "Do not evaluate suitability for any specific job."
        )
    )

    caveats: list[str] = Field(
        description=(
            "Relevant missing, ambiguous, or unverified "
            "candidate information."
        )
    )


class JobRequirements(BaseModel):
    job_id: str
    title: str
    required_skills: list[str]
    preferred_skills: list[str]
    min_experience_years: int = Field(ge=0)
    requirements_confirmed: bool = False


class MatchResult(BaseModel):
    job_id: str
    candidate_name: str | None

    matched_required_skills: list[str]
    unverified_required_skills: list[str]

    matched_preferred_skills: list[str]
    unverified_preferred_skills: list[str]

    experience_requirement: int
    experience_status: str

    caveats: list[str]

class CandidateRecommendation(BaseModel):
    status: Literal["review_recommended", "manual_review_required"] = Field(
        description=(
            "Advisory review status only. "
            "Never represents hiring approval or rejection."
        )
    )

    reasoning: str = Field(
        description=(
            "Explain the recommendation using only "
            "the provided candidate overview and job matching results."
        )
    )

    strengths: list[str] = Field(
        description="Relevant candidate qualifications supported by evidence."
    )

    caveats: list[str] = Field(
        description="Missing, ambiguous, or unverified information."
    )

    suggested_follow_up: list[str] = Field(
        description="Specific questions or checks for the HR reviewer."
    )

    requires_human_review: bool = Field(
        description="Always true. Human review is mandatory."
    )
