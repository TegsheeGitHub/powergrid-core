"""
RAG Service.
Handles the logic of retrieving context and querying the LLM.
"""
import os
import openai
from dotenv import load_dotenv
from app.core.models import QueryResponse, SourceCitation

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
# Note: In a real enterprise, we would use AzureOpenAI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------------------------------------------
# STATIC KNOWLEDGE BASE (The "Retrieval" part of RAG)
# -----------------------------------------------------------------------------
# This simulates a document regarding Energy Efficiency Directive (EED).
CONTEXT_DOCUMENT = """
REGULATION: EU Energy Efficiency Directive (EED) 2023 Recast.
SECTION 1: Energy Savings Obligation.
Member States must achieve cumulative end-use energy savings equivalent to new annual savings of at least 0.8% of final energy consumption.
SECTION 2: Public Sector.
Public bodies must renovate 3% of the total floor area of heated and/or cooled buildings owned and occupied by central government each year.
SECTION 3: Metering.
Final customers for electricity, natural gas, district heating, district cooling and domestic hot water should be provided with competitively priced individual meters that accurately reflect the final customer's actual energy consumption and that provide information on actual time of use.
"""

class IntelligenceEngine:
    def __init__(self):
        self.model = "gpt-3.5-turbo" # Cost-effective for demo
        self.system_prompt = f"""
        You are an Expert Compliance Officer for Fortum, a major energy company.
        You only answer questions based on the provided Regulatory Context.
        
        CONTEXT:
        {CONTEXT_DOCUMENT}
        
        RULES:
        1. If the answer is in the context, answer clearly and cite the section.
        2. If the answer is NOT in the context, state: "I cannot find this in the current regulatory database."
        3. Do not hallucinate or use outside knowledge.
        """

    def ask_llm(self, user_question: str) -> QueryResponse:
        """
        Sends the user question + context to OpenAI.
        """
        try:
            # 1. Check if API Key is present (Fail gracefully if user forgot it)
            if not os.getenv("OPENAI_API_KEY"):
                return self._mock_fallback(user_question)

            # 2. Call OpenAI API
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.1 # Low temperature for factual accuracy
            )

            answer_text = response.choices[0].message.content

            # 3. Construct Response
            return QueryResponse(
                answer=answer_text,
                citations=[SourceCitation(document="EU EED Directive 2023", section="Derived from Context")],
                confidence_score=0.98
            )

        except Exception as e:
            print(f"LLM Error: {e}")
            return QueryResponse(
                answer="Error contacting Intelligence Service. Please check API Key configuration.",
                citations=[],
                confidence_score=0.0
            )

    def _mock_fallback(self, question: str) -> QueryResponse:
        """
        Fallback response if no API Key is provided, ensuring the frontend doesn't break.
        """
        return QueryResponse(
            answer="[SIMULATION MODE - NO API KEY] The EU Energy Efficiency Directive requires 3% renovation of public buildings annually.",
            citations=[SourceCitation(document="Simulation DB", section="Mock Section")],
            confidence_score=1.0
        )