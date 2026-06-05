PROMPT = '''
You are an expert at generating realistic user questions for software testing purposes.
You will be given the documentation of a management software, scoped to a specific user role. Your task is to generate a list of questions that a real employee of THAT role might ask when trying to use the software.

Follow these rules strictly:

## Content Rules

- Questions must be directly and FULLY answerable using ONLY the provided documentation. Before writing each question, verify that its complete answer is explicitly stated in the text — not implied, not inferable, not partially covered. If in doubt, discard the question.
- Do NOT generate questions about features or concepts that are merely mentioned as examples in the documentation. If the text uses something in a list of examples (e.g., "such as X, Y or Z" to illustrate a generic concept), do not write a question specifically about X, Y or Z — write a question about the generic concept instead.
- Do NOT generate questions about a feature that appears to belong to a different user role. Focus only on procedures that a user of THIS specific role performs directly in the interface described in the documentation.
- If the documentation describes only how to VIEW or READ a value, do NOT generate a question about how to MODIFY or EDIT that value.
- Do NOT generate questions about the reverse or inverse of a documented procedure (e.g., if the doc describes going from state A to state B, do not ask how to go from B to A).
- Do NOT generate questions about the consequences or side effects of an action (e.g., "what happens after clicking X", "what does activating Y affect") unless the documentation explicitly and directly describes that outcome.
- Do NOT generate questions about the content requirements of a field (e.g., "what should I write in field X") unless the documentation explicitly states what to enter.
- Do NOT generate questions about external laws, regulations, or normative frameworks (e.g., d.lgs. 231/2007), even if the software mentions compliance with them.
- Do NOT generate questions about error handling, troubleshooting, or system malfunctions unless the documentation explicitly provides guidance on those scenarios.

## Style Rules

- Questions must sound natural and conversational, but MUST use the EXACT domain terminology found in the documentation. Do NOT paraphrase, translate, or rephrase technical terms — if the documentation calls something "spread" or "fermo cautelativo", use those exact words.
- Questions must be specific enough that a search system (RAG) can identify exactly which section or procedure is being asked about. Avoid questions so generic that they could apply to any section or any software (e.g., "where is the search bar").
- Do NOT make the questions vague or incomplete. The user's specific goal must be clear.
- Focus on practical tasks, step-by-step procedures, and navigation based directly on the provided text.
- Incorporate the role context into each question where relevant (e.g., "Dalla vista Back Office...", "Dalla sezione Laboratorio...") so that it is clear who is asking and from which interface.
- Generate between 20 and 30 questions.

## Format Rules

- Write ONLY the list of questions, one per line.
- Do NOT write any introduction, explanation, greeting, or closing remark before or after the list.
- Do NOT ask questions about your own task or the documentation itself.

Here is the documentation:
[DOCUMENTATION]
'''