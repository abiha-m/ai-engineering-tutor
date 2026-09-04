"""
Concept Explainer Module
Generates structured explanations of engineering concepts
"""

import json
import logging
from typing import Dict, Any, Optional
from tutor_engine import TutorEngine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConceptExplainer:
    """
    Explains engineering concepts with structured output
    Includes definition, formula, application, and real-world examples
    """
    
    def __init__(self, engine: Optional[TutorEngine] = None):
        """
        Initialize the concept explainer
        
        Args:
            engine: Optional TutorEngine instance (creates one if not provided)
        """
        self.engine = engine or TutorEngine()
        logger.info("Concept Explainer initialized")
    
    def explain_concept(self, concept: str, topic_context: str = "General Engineering") -> Dict[str, Any]:
        """
        Generate a comprehensive explanation of an engineering concept
        
        Args:
            concept: The concept to explain (e.g., "Ohm's Law")
            topic_context: Engineering topic context
            
        Returns:
            Dictionary with structured explanation
        """
        logger.info(f"Explaining concept: {concept} in context: {topic_context}")
        
        # Get engineering context
        eng_context = self.engine.get_engineering_context(topic_context)
        
        # Construct system prompt
        system_prompt = """
        You are an expert engineering tutor with years of teaching experience.
        Your explanations are clear, structured, and engaging.
        You use analogies and real-world examples to make complex concepts understandable.
        
        Follow these principles:
        - Start with the simplest explanation possible
        - Build complexity gradually
        - Use clear, jargon-free language
        - Provide concrete examples
        - Connect to everyday experiences
        - Explain WHY, not just WHAT
        
        Always structure your response as a valid JSON object.
        """
        
        # Construct user prompt
        user_prompt = f"""
        Explain the engineering concept: "{concept}"
        
        Context: This is in the field of {topic_context}.
        
        Engineering Context: {eng_context}
        
        Provide your explanation as a JSON object with the following structure:
        
        {{
            "concept": "{concept}",
            "definition": "A clear, comprehensive definition of the concept",
            "key_formula": "The main formula (if applicable) with explanation of each variable",
            "step_by_step": "Step-by-step explanation of how to apply the concept",
            "real_world_example": "A concrete real-world example with numbers or scenarios",
            "common_mistakes": [
                "List of common mistakes to avoid",
                "Include at least 3 common errors"
            ],
            "analogy": "A simple analogy to help understand the concept",
            "difficulty_level": "Basic/Intermediate/Advanced"
        }}
        
        Requirements:
        - Be thorough but clear
        - Use proper mathematical notation when applicable
        - Include units in formulas
        - Make the example realistic and practical
        - Keep the explanation at an appropriate level for engineering students
        """
        
        # Generate response
        response = self.engine.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5,  # Lower temperature for more consistent output
            max_tokens=800,
            operation="explain_concept"
        )
        
        # Check for errors
        if 'error' in response:
            logger.error(f"Error in explanation: {response['error']}")
            return {
                'error': response['error'],
                'concept': concept,
                'definition': f"Error explaining {concept}. Please try again."
            }
        
        # Parse JSON response
        try:
            # Clean the response (remove markdown code blocks if present)
            content = response['content']
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            explanation = json.loads(content)
            logger.info(f"Successfully parsed explanation for {concept}")
            return explanation
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Raw response: {response['content'][:200]}...")
            
            # Fallback: Return raw text with structure
            return {
                'concept': concept,
                'definition': response['content'],
                'key_formula': "See explanation above",
                'step_by_step': "See explanation above",
                'real_world_example': "See explanation above",
                'common_mistakes': ["See full explanation above"],
                'analogy': "See explanation above",
                'difficulty_level': "Intermediate",
                'raw_response': response['content']
            }
    
    def explain_multiple(self, concepts: list, topic_context: str = "General Engineering") -> list:
        """
        Explain multiple concepts
        
        Args:
            concepts: List of concept names
            topic_context: Engineering topic context
            
        Returns:
            List of explanations
        """
        results = []
        for concept in concepts:
            result = self.explain_concept(concept, topic_context)
            results.append(result)
            logger.info(f"Explained {len(results)}/{len(concepts)} concepts")
        return results
    
    def get_cost_summary(self) -> str:
        """Get cost summary from the engine"""
        return self.engine.get_cost_summary()
    
    def get_total_cost(self) -> float:
        """Get total cost from the engine"""
        return self.engine.get_total_cost()