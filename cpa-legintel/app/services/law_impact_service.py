import json
from sqlalchemy.orm import Session

from app.models import Client, Law, LawVersion, LawImpact
from app.services.llm_client import get_llm
from app.services.prompts import law_impact_prompt


def generate_law_impact(
    db: Session,
    client: Client,
    law: Law,
    version: LawVersion,
) -> LawImpact:
    # 🔒 Cache: do not regenerate for same version
    existing = (
        db.query(LawImpact)
        .filter(
            LawImpact.client_id == client.id,
            LawImpact.law_version_id == version.id,
        )
        .one_or_none()
    )
    if existing:
        return existing

    prompt = law_impact_prompt(
        client_name=client.name,
        client_state=client.state,
        entity_type=client.entity_type,
        law_text=version.text,
    )

    llm = get_llm()

    response = llm.chat.completions.create(
        model="gpt-4o-mini",  # fast + cheap
        messages=[
            {"role": "system", "content": "You are a legal compliance expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # graceful fallback
        data = {
            "summary": content[:500],
            "reasoning": "LLM output not valid JSON",
            "confidence": 0.3,
        }

    impact = LawImpact(
        client_id=client.id,
        law_id=law.id,
        law_version_id=version.id,
        summary=data.get("summary", ""),
        reasoning=data.get("reasoning"),
        confidence=float(data.get("confidence", 0.5)),
    )

    db.add(impact)
    db.commit()
    db.refresh(impact)
    return impact
