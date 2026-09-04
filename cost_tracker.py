"""
Cost Tracker for AI Engineering Tutor
Tracks OpenAI API usage and costs
Reused and adapted from Project 1
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional
import tiktoken

class CostTracker:
    """Track API usage costs for different operations"""
    
    # Pricing per 1000 tokens (as of January 2024)
    PRICING = {
        "gpt-4-turbo-preview": {
            "input": 0.01,   # $0.01 per 1K input tokens
            "output": 0.03   # $0.03 per 1K output tokens
        },
        "gpt-3.5-turbo": {
            "input": 0.0005,  # $0.0005 per 1K input tokens
            "output": 0.0015  # $0.0015 per 1K output tokens
        }
    }
    
    def __init__(self, cost_file="cost_data.json"):
        """
        Initialize the cost tracker
        
        Args:
            cost_file: Path to JSON file for storing cost data
        """
        self.cost_file = cost_file
        self.cost_data = self._load_cost_data()
        self.encoders = {}  # Cache for encoders
        
    def _load_cost_data(self) -> Dict:
        """Load existing cost data from file or create new"""
        if os.path.exists(self.cost_file):
            try:
                with open(self.cost_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._create_new_cost_data()
        return self._create_new_cost_data()
    
    def _create_new_cost_data(self) -> Dict:
        """Create new cost data structure"""
        return {
            "total_cost": 0.0,
            "total_tokens": 0,
            "total_requests": 0,
            "operations": {},
            "history": []
        }
    
    def _get_encoder(self, model: str):
        """Get or create token encoder for a model"""
        if model not in self.encoders:
            try:
                self.encoders[model] = tiktoken.encoding_for_model(model)
            except KeyError:
                # Fallback to cl100k_base for newer models
                self.encoders[model] = tiktoken.get_encoding("cl100k_base")
        return self.encoders[model]
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """
        Count tokens in a text string
        
        Args:
            text: Text to count tokens for
            model: Model name for encoding
            
        Returns:
            Number of tokens
        """
        if not text:
            return 0
        encoder = self._get_encoder(model)
        return len(encoder.encode(text))
    
    def track_usage(self, operation: str, tokens: Dict[str, int], model: str = "gpt-3.5-turbo") -> Dict:
        """
        Track usage for an operation
        
        Args:
            operation: Name of the operation
            tokens: Dictionary with 'input', 'output', 'total' token counts
            model: Model used for the operation
            
        Returns:
            Dictionary with cost breakdown
        """
        input_tokens = tokens.get('input', 0)
        output_tokens = tokens.get('output', 0)
        
        # Get pricing for model
        pricing = self.PRICING.get(model, self.PRICING["gpt-3.5-turbo"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        # Update tracking
        if operation not in self.cost_data["operations"]:
            self.cost_data["operations"][operation] = {
                "count": 0,
                "total_cost": 0.0,
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0
            }
        
        op_data = self.cost_data["operations"][operation]
        op_data["count"] += 1
        op_data["total_cost"] += total_cost
        op_data["total_tokens"] += input_tokens + output_tokens
        op_data["input_tokens"] += input_tokens
        op_data["output_tokens"] += output_tokens
        
        # Update totals
        self.cost_data["total_cost"] += total_cost
        self.cost_data["total_tokens"] += input_tokens + output_tokens
        self.cost_data["total_requests"] += 1
        
        # Add to history
        self.cost_data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": total_cost
        })
        
        # Save to file
        self._save_cost_data()
        
        return {
            "operation": operation,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    
    def _save_cost_data(self):
        """Save cost data to file"""
        try:
            with open(self.cost_file, 'w') as f:
                json.dump(self.cost_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cost data: {e}")
    
    def get_total_cost(self) -> float:
        """Get total cost"""
        return self.cost_data["total_cost"]
    
    def get_operation_stats(self) -> Dict:
        """Get statistics by operation"""
        return self.cost_data["operations"]
    
    def get_summary(self) -> str:
        """Get a summary of all costs"""
        summary = f"""
        COST TRACKER SUMMARY
        ====================
        Total Cost: ${self.cost_data['total_cost']:.4f}
        Total Tokens: {self.cost_data['total_tokens']:,}
        Total Requests: {self.cost_data['total_requests']}
        
        Operations Breakdown:
        """
        for op, data in self.cost_data["operations"].items():
            summary += f"\n  {op}:"
            summary += f"\n    Count: {data['count']}"
            summary += f"\n    Cost: ${data['total_cost']:.4f}"
            summary += f"\n    Tokens: {data['total_tokens']:,}"
        
        return summary
    
    def estimate_cost(self, operation: str, input_tokens: int = 0, output_tokens: int = 0, 
                     model: str = "gpt-3.5-turbo") -> float:
        """
        Estimate cost before making an API call
        
        Args:
            operation: Name of operation
            input_tokens: Estimated input tokens
            output_tokens: Estimated output tokens
            model: Model to use
            
        Returns:
            Estimated cost
        """
        pricing = self.PRICING.get(model, self.PRICING["gpt-3.5-turbo"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
    
    def reset(self):
        """Reset all cost data"""
        self.cost_data = self._create_new_cost_data()
        self._save_cost_data()
    
    def export_report(self, filename: str = None):
        """
        Export cost report to JSON file
        
        Args:
            filename: Optional filename (default: cost_report_TIMESTAMP.json)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cost_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.cost_data, f, indent=2)
        print(f"Cost report exported to {filename}")