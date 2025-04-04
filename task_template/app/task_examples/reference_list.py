import logging
from typing import Any, List
import json
from tasks.task_interface import Task, OpenAITask
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
    OpenAIBasedDataRequest,
    OpenAIBasedRequest
)

logger = logging.getLogger(__name__)

def get_system_prompt(objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to iteratively create a reference list.
            The details of the references list are as follows: {objective}
            You will get a message from the user in the form COMMENT_LINE: COMMENT_LINE is
            comments made by the user and it may contain a request for you to replace previously generated references
            with new ones. Your answer should take the references and the rest of the comment into consideration.
            If COMMENT_LINE is empty, you must answer by generating references according to the given details
            (topic, citation format and number of references).
            If COMMENT_LINE is not empty, you give your opinion or answer about the content of COMMENT_LINE that the user provided.
            If the user asks a question, you answer it. If COMMENT_LINE contains a request from the user to replace
            some references, you must answer by generating references that will replace the references the user is
            referring to. The user may refer to references with numbers or otherwise. If COMMENT_LINE indicates that the
            user is satisfied will all of the references, you must answer with a finalized reference list only including the
            bibliographic citations of the references in the specified citation format and in the correct order according to 
            the citation format. The user may indicate their satisfaction in various ways, for example by saying that they like
            the references or that they are satisfied with them.
            Your answer must follow this form: [REFERENCES] YOUR_COMMENT where REFERENCES is the references you generated
            and it has to be wrapped inside square brackets while YOUR_COMMENT is your answer or opinion about 
            the content of COMMENT_LINE. Always answer with YOUR_COMMENT and if COMMENT_LINE is empty or references are 
            requested, also answer with [REFERENCES]. If you generate [REFERENCES], you comment briefly something about 
            providing new references in YOUR_COMMENT.
            For each reference in REFERENCES you should provide the following information:
            the reference's running number, the reference's title, its bibliographic citation in the specified citation format,
            a summary of its content, where the reference has been published and a link to the original work.
            If you don't need to generate references anymore because the user is satisfied with all of the references,
            the REFERENCES should only be the bibliographic citations of the references as a JSON array of strings.
            If the COMMENT_LINE is empty, or the user asks for new references, each reference in REFERENCES must be a JSON
            and the REFERENCES must be a JSON array. For example, if REFERENCES would include two references, 
            it should follow the following example:\n
            [
              {{
                "number": "1",
                "title": "How the Design of YouTube Influences User Sense of Agency",
                "citation": "Lukoff, K., Lyngs, U., Zade, H., Liao, J. V., Choi, J., Fan, K., Munson, S. A., & Hiniker, A. (2021). How the Design of YouTube Influences User Sense of Agency. Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems, 1-17. https://doi.org/10.1145/3411764.3445467",
                "summary": "This study examines how YouTube's design affects user agency, finding that autoplay and recommendations reduce control, while playlists and search enhance it. Based on user surveys and co-design sessions, the authors suggest design improvements to help users regain intentionality in their media consumption.",
                "publisher": "Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems (CHI '21) by the Association for Computing Machinery (ACM)",
                "number_of_citations": "153",
                "link": "https://dl.acm.org/doi/10.1145/3411764.3445467"
              }},
              {{
                "number": "2",
                "title": "Don't put all social network sites in one basket: Facebook, Instagram, Twitter, TikTok, and their relations with well-being during the COVID-19 pandemic",
                "citation": "Masciantonio, A., Bourguignon, D., Bouchat, P., Balty, M., & Rimé, B. (2021). Don't put all social network sites in one basket: Facebook, Instagram, Twitter, TikTok, and their relations with well-being during the COVID-19 pandemic. PLOS ONE, 16(3), e0248384. https://doi.org/10.1371/journal.pone.0248384",
                "summary": "This study examines how different social network sites influenced well-being during COVID-19. Passive Facebook use worsens well-being through upward social comparison, while active Instagram and Twitter use boost life satisfaction via social support. Passive Twitter use reduces negative effects, and TikTok shows no significant impact. Findings highlight the need to differentiate SNS effects based on platform design and usage patterns.",
                "publisher": "PLOS ONE, a peer-reviewed open-access journal.",
                "number_of_citations": "250",
                "link": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0248384"
              }}
            ]
            Remember REFERENCES must be a valid JSON, all the key names and structure must follow the example exactly, 
            wrapped inside squared brackets, followed by the comment. Do not add redundant string such as "```json", "```",
            or equivalent. Only add the comment after the references.
            If the user would want to replace a reference from the example list above, they could state this by asking you
            to replace reference 1 or 2 since those are the example references' running numbers. You must keep the running 
            numbers the same: if the user asks you to replace reference 2, you must answer with a reference whose "number"
            value is 2.
            If the user is satisfied with all of the references, REFERENCES should only include the bibliographic citations
            of the references ordered correcly according to the citation format. The result must be a JSON array where each
            element is a bibliographic citation. For example, if REFERENCES would include two references and they would be 
            formatted in APA 7, it should follow the following example:\n
            [
              "Lukoff, K., Lyngs, U., Zade, H., Liao, J. V., Choi, J., Fan, K., Munson, S. A., & Hiniker, A. (2021). How the Design of YouTube Influences User Sense of Agency. Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems, 1-17. https://doi.org/10.1145/3411764.3445467",
              "Masciantonio, A., Bourguignon, D., Bouchat, P., Balty, M., & Rimé, B. (2021). Don't put all social network sites in one basket: Facebook, Instagram, Twitter, TikTok, and their relations with well-being during the COVID-19 pandemic. PLOS ONE, 16(3), e0248384. https://doi.org/10.1371/journal.pone.0248384"
            ]
            Remember REFERENCES must be a valid JSON array, the structure must follow the example exactly without adding key
            names or including JSON objects. Do not add redundant string such as "```json", "```",
            or equivalent. Only add the comment after the references.
            Your REFERENCES must not repeat what you have generated before.
            You are curious, and always ready and eager to ask the user question if needed."""
        return system_prompt

class ReferenceList(Task):


    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        commentline = json.dumps(request.inputData['comment'])

        return TaskRequest(
            text=f"{commentline}",
            system=get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
    
class PoetryOpenAI(OpenAITask):
    """ Implementation of the Poetry Task as an OpenAI like task"""

    def process_model_answer_openAI(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...        
        return TaskDataResponse(text=answer.text)

    def generate_model_request_openAI(self, request: OpenAIBasedDataRequest) -> OpenAIBasedRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # Add the system prompt (which is not allowed from the frontend)
        system_message = get_system_prompt(request.objective)
        messages = [{"role" : "system", "content" : system_message}]
        messages.extend([element for element in request.userMessages])
        return OpenAIBasedRequest(messages=messages)
        

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)