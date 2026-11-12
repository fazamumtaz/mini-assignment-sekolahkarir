
import re
from dataclasses import dataclass

from .schemas import CandidateProfile


@dataclass
class EvidenceCheck:
    field: str
    value: str
    supported: bool


def normalize_text(text: str) -> str:
    """Normalize text for simple evidence matching."""
    return re.sub(r"\s+", " ", text).casefold().strip()


def check_evidence(
    value: str,
    source_text: str
) -> bool:
    """Check whether a value appears in the source CV."""
    return normalize_text(value) in normalize_text(source_text)


def validate_evidence(
    candidate: CandidateProfile,
    cv_text: str
) -> list[EvidenceCheck]:
    """Validate selected candidate fields against CV text."""

    checks = []

    # Skills
    for skill in candidate.skills:
        checks.append(
            EvidenceCheck(
                field="skills",
                value=skill,
                supported=check_evidence(skill, cv_text)
            )
        )

    # Education
    for education in candidate.education:
        checks.append(
            EvidenceCheck(
                field="education.institution",
                value=education.institution,
                supported=check_evidence(
                    education.institution, cv_text
                )
            )
        )

    # Experience
    for experience in candidate.experience:
        checks.append(
            EvidenceCheck(
                field="experience.organization",
                value=experience.organization,
                supported=check_evidence(
                    experience.organization, cv_text
                )
            )
        )

    # Projects
    for project in candidate.projects:
        checks.append(
            EvidenceCheck(
                field="projects.name",
                value=project.name,
                supported=check_evidence(
                    project.name, cv_text
                )
            )
        )

    return checks
