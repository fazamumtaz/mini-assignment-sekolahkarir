
from .schemas import CandidateProfile, JobRequirements, MatchResult
from .validator import EvidenceCheck


def normalize_skill(skill: str) -> str:
    return " ".join(skill.casefold().split())


def match_candidate(
    candidate: CandidateProfile,
    job: JobRequirements,
    evidence_checks: list[EvidenceCheck],
) -> MatchResult:
    """Compare verified candidate skills with job requirements."""

    if not job.requirements_confirmed:
        raise ValueError("Job requirements must be confirmed by HR.")

    verified_skills = {
        normalize_skill(check.value)
        for check in evidence_checks
        if check.field == "skills" and check.supported
    }

    matched_required = [
        skill for skill in job.required_skills
        if normalize_skill(skill) in verified_skills
    ]

    unverified_required = [
        skill for skill in job.required_skills
        if normalize_skill(skill) not in verified_skills
    ]

    matched_preferred = [
        skill for skill in job.preferred_skills
        if normalize_skill(skill) in verified_skills
    ]

    unverified_preferred = [
        skill for skill in job.preferred_skills
        if normalize_skill(skill) not in verified_skills
    ]

    caveats = []

    if unverified_required:
        caveats.append(
            "Some required skills could not be verified "
            "from the candidate's CV."
        )

    if unverified_preferred:
        caveats.append(
            "Some preferred skills could not be verified "
            "from the candidate's CV."
        )

    if job.min_experience_years == 0:
        experience_status = "not_required"
    else:
        experience_status = "needs_manual_review"
        caveats.append(
            "Professional experience duration has not "
            "been calculated or verified."
        )

    return MatchResult(
        job_id=job.job_id,
        candidate_name=candidate.name,
        matched_required_skills=matched_required,
        unverified_required_skills=unverified_required,
        matched_preferred_skills=matched_preferred,
        unverified_preferred_skills=unverified_preferred,
        experience_requirement=job.min_experience_years,
        experience_status=experience_status,
        caveats=caveats,
    )
