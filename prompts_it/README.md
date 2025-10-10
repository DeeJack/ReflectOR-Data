# System Prompts

System prompts used in the ReflectOR system.
The prompts are created for LangChain and Pydantic. {variable_name} puts the value of a variable in python into the prompt before it's sent to the LLM.

- [coordinator_agent.txt](./coordinator_agent.txt): For the Coordinator agent, the supervisor of the workflow;
- [discussion.txt](./discussion.txt): For the Discussion planner sub-agent;
- [errors.txt](./errors.txt): Error Identification sub-agent;
- [fields.yaml](./fields.yaml): Fields used for the PDF report, tool descriptions, etc.
- [gemini_diarization.txt](./gemini_diarization.txt): For the transcription+diarization with Gemini;
- [improve.txt](./improve.txt): Improve the transcript with LLM;
- [materials.txt](./materials.txt): Creates the list of materials used in the operation;
- [operation.txt](./operation.txt): Extracts metadata information about the operation;
- [operation_outcome.txt](./operation_outcome.txt): Analyzes the outcome of the operation;
- [operation_team.txt](./operation_team.txt): Information on the team performing the operation;
- [patient.txt](./patient.txt): Extracts information about the patient;
- [performance_analysis.txt](./performance_analysis.txt): Evaluates the performance for the students performing the operation;
- [summary_execute](./summary_execute.txt): Executes the summary of the operation;
- [timeline.txt](./timeline.txt): Extracts the key events of the operation;
- [transcript_filter.txt](./transcript_filter.txt): Filter the transcript (not used);
