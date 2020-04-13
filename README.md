# Questions About Art

With the use of question templates, the system generates questions in Russian about art movements, art works and their creators. Ten different templates are used.

After every question, the user should type in the answer. Before displaying the next question, the system provides the user with the feedback on his/her answer by stating "true" or "false".

The information needed for filling in the templates was extracted from the Wikidata.

### Examples

- Какое движение последовало за движением маньеризм? "What movement followed the movement Mannerism?" (Барокко "Baroque")
- Кто создал произведение 'Венера перед зеркалом'? "Who created the work 'Venus with a Mirror'?" (Тициан "Titian")
- В каком году родился/родилась Франсуа Буше? "When was François Boucher born?" (1703)

### Languages used
- Python: downloading information for filling the templates, generationn of questions
- SPARQL: extracting information from the Wikidata

### How to run
In order to generate questions, download the folder "code_generate" and run the program "generate_questions.py".
