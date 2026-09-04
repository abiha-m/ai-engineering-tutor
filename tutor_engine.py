"""
Core Tutor Engine for AI Engineering Tutor
Orchestrates all tutoring operations
"""

import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from cost_tracker import CostTracker

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TutorEngine:
    """
    Core engine for the AI Engineering Tutor
    Handles all interactions with the OpenAI API
    """
    
    def __init__(self, model: str = None):
        """
        Initialize the tutor engine
        
        Args:
            model: OpenAI model to use (defaults to gpt-3.5-turbo)
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.model = model or os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
        self.client = OpenAI(api_key=self.api_key)
        self.cost_tracker = CostTracker()
        logger.info(f"Tutor Engine initialized with model: {self.model}")
    
    def generate_response(self, 
                         prompt: str, 
                         system_prompt: str, 
                         temperature: float = 0.7,
                         max_tokens: int = 1000,
                         operation: str = "general") -> Dict[str, Any]:
        """
        Generate a response from the AI
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Creativity (0-1)
            max_tokens: Maximum tokens in response
            operation: Name of operation for tracking
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Estimate tokens before call
            estimated_input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            estimated_output_tokens = max_tokens
            
            # Get cost estimate
            estimated_cost = self.cost_tracker.estimate_cost(
                operation,
                input_tokens=int(estimated_input_tokens),
                output_tokens=estimated_output_tokens,
                model=self.model
            )
            
            logger.info(f"Estimated cost for {operation}: ${estimated_cost:.4f}")
            logger.info(f"Prompt length: {len(prompt)} characters")
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract response
            content = response.choices[0].message.content
            token_usage = {
                'input': response.usage.prompt_tokens,
                'output': response.usage.completion_tokens,
                'total': response.usage.total_tokens
            }
            
            # Track cost
            cost_details = self.cost_tracker.track_usage(
                operation,
                token_usage,
                self.model
            )
            
            logger.info(f"Tokens used: {token_usage['total']}")
            logger.info(f"Actual cost: ${cost_details['total_cost']:.4f}")
            
            return {
                'content': content,
                'tokens': token_usage,
                'cost': cost_details,
                'model': self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                'error': str(e),
                'content': f"Error: {str(e)}"
            }
    
    def get_engineering_context(self, topic: str) -> str:
        """
        Get engineering context for a specific topic
        
        Args:
            topic: Engineering topic
            
        Returns:
            Context description
        """
        context_map = {
            "Circuit Analysis": """
                Circuit analysis involves the study of electrical circuits and their behavior.
                Key areas include Ohm's Law, Kirchhoff's Laws, Thevenin's Theorem, and 
                Norton's Theorem. It's fundamental to electrical engineering and electronics.
            """,
            "Mechanics": """
                Mechanics deals with the behavior of physical bodies under forces and motion.
                Key areas include Newton's Laws of Motion, kinematics, dynamics, statics,
                and work-energy principles. It's fundamental to mechanical engineering.
            """,
            "Thermodynamics": """
                Thermodynamics studies heat, work, temperature, and energy transfer.
                Key areas include the First Law (energy conservation), Second Law (entropy),
                and thermodynamic cycles. It's crucial for mechanical and chemical engineering.
            """,
            "Calculus": """
                Calculus is the mathematical study of continuous change. It includes 
                differential calculus (rates of change) and integral calculus (accumulation).
                It's essential for all engineering disciplines.
            """,
            "Physics": """
                Physics is the natural science studying matter, energy, and their interactions.
                Key areas include mechanics, waves, electromagnetism, and quantum physics.
                It's the foundation of all engineering disciplines.
            """
        }
        return context_map.get(topic, "General engineering principles")
    
    def get_cost_summary(self) -> str:
        """
        Get summary of all costs
        
        Returns:
            Formatted cost summary
        """
        return self.cost_tracker.get_summary()
    
    def get_total_cost(self) -> float:
        """
        Get total cost so far
        
        Returns:
            Total cost in USD
        """
        return self.cost_tracker.get_total_cost()
    
    def reset_costs(self):
        """Reset cost tracking"""
        self.cost_tracker.reset()
        logger.info("Cost tracking reset")