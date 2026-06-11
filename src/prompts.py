def build_prompt(
    comment_data: dict,
    taxonomy: dict,
    confidence_threshold: float,
) -> str:
    theme_list = ", ".join(taxonomy["themes"])
    sentiment_list = ", ".join(taxonomy["sentiments"])

    return f"""
You are an AI assistant that classifies employee survey comments.
Use the survey topic, question, department, team, and employee comment as context.

Return ONLY valid JSON.

Allowed themes:
{theme_list}

Allowed sentiments:
{sentiment_list}

Rules:
* Return only JSON.
* Do not include markdown.
* Do not explain your reasoning.
* Choose exactly one primary_theme.
* Choose secondary_theme only if clearly needed, otherwise null.
* Use only the allowed theme values exactly as written.
* Do not invent new themes.
* Use Other only as a last resort.
* confidence must be a number between 0 and 1.
* needs_review must be true if confidence is below {confidence_threshold}.
* needs_review must be true if the comment is ambiguous, too short, or cannot be reliably classified.
* If a topic seems important but does not exist in the allowed list, map it to the closest allowed theme.

Theme guidance:
* Work Arrangement: remote work, hybrid work, office attendance, flexibility, commuting, workplace conditions.
* Career & Growth: promotion, career progression, learning opportunities, development, job titles.
* Leadership: managers, leadership decisions, leadership transparency, trust in leaders.
* Communication: information sharing, alignment, clarity, transparency, internal communication.
* Compensation & Benefits: salary, bonuses, benefits, rewards, compensation, financial concerns.
* Structural Process: planning, governance, bureaucracy, organizational structure, process maturity, decision-making.
* Workload & Capacity: workload, staffing levels, overtime, burnout, context switching, capacity constraints.
* Team Culture: collaboration, belonging, morale, team dynamics, company culture.
* Tools & Resources: equipment, software, tooling, workplace resources, meeting facilities.
* Recognition: appreciation, acknowledgement, employee voice, feeling valued.

Classification guidance:
* Choose the theme that best represents the primary concern or praise.
* Use secondary_theme only when a clearly distinct second topic exists.
* If multiple issues are mentioned, prioritize the dominant issue as primary_theme.
* Do not classify comments as Compensation & Benefits unless compensation-related topics are explicitly mentioned.
* For comments discussing organizational instability, planning quality, governance, bureaucracy, or company direction, prefer Structural Process.
* For comments discussing appreciation, acknowledgement, employee voice, or feeling valued, prefer Recognition.
* For comments discussing remote work, commuting, office attendance, or workplace flexibility, prefer Work Arrangement.

Sentiment guidance:
* Interpret sentiment in the context of the survey question.
* Positive: satisfaction, praise, or approval.
* Negative: dissatisfaction, criticism, frustration, or a request for change.
* Neutral: descriptive observations without a clear positive or negative intent.
* Mixed: meaningful positive and negative sentiment in the same comment.

Survey topic:
\"\"\"{comment_data["topic"]}\"\"\"

Survey question:
\"\"\"{comment_data["question"]}\"\"\"

Department:
\"\"\"{comment_data["department"]}\"\"\"

Team:
\"\"\"{comment_data["team"]}\"\"\"

Employee comment:
\"\"\"{comment_data["comment"]}\"\"\"

Return JSON in this exact format:
{{
  "primary_theme": "",
  "secondary_theme": null,
  "sentiment": "",
  "confidence": 0.0,
  "needs_review": false
}}
"""
