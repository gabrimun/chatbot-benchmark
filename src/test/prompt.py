PROMPT='''
You are an expert at generating realistic user questions for software testing purposes.
You will be given the documentation of a management software. Your task is to generate a list of questions that a real, non-technical user might ask when trying to use the software.
Follow these rules strictly:
- Questions must focus on general goals and outcomes, not specific steps or menu navigation
- Avoid overly specific or technical questions (no questions about exact field names, IDs, button labels, or internal logic)
- Keep questions broad and goal-oriented — a user should sound like they know what they want to achieve, but not necessarily how
- Write questions as a real end-user would phrase them — naturally, sometimes vague or incomplete
- Cover a variety of use cases and user goals described in the documentation
- Generate between 20 and 30 questions
- Write ONLY the list of questions, one per line
- Do NOT write any introduction, explanation, greeting, or closing remark before or after the list
- Do NOT ask questions about your own task or the documentation itself
Here is the documentation:
[DOCUMENTATION]
'''