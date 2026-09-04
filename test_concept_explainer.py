"""
Test script for Concept Explainer
Tests the concept explanation feature with various engineering topics
"""

import json
from concept_explainer import ConceptExplainer

def test_concept_explanation():
    """Test the concept explanation feature"""
    print("=" * 60)
    print("TESTING CONCEPT EXPLAINER")
    print("=" * 60)
    
    # Initialize explainer
    explainer = ConceptExplainer()
    
    # Test concepts
    test_concepts = [
        ("Ohm's Law", "Circuit Analysis"),
        ("Thevenin's Theorem", "Circuit Analysis"),
        ("Newton's Second Law", "Mechanics"),
        ("First Law of Thermodynamics", "Thermodynamics"),
        ("Fourier Transform", "Signal Processing")
    ]
    
    for concept, topic in test_concepts[:3]:  # Test first 3 to save API costs
        print(f"\n{'='*40}")
        print(f"Testing: {concept} (Context: {topic})")
        print('='*40)
        
        try:
            # Get explanation
            result = explainer.explain_concept(concept, topic)
            
            # Display results
            print(f"\nDefinition: {result.get('definition', 'N/A')[:100]}...")
            print(f"Formula: {result.get('key_formula', 'N/A')}")
            
            # Check for required fields
            required_fields = ['definition', 'key_formula', 'step_by_step', 
                             'real_world_example', 'common_mistakes', 'analogy']
            missing_fields = [f for f in required_fields if f not in result]
            
            if missing_fields:
                print(f"⚠️ Missing fields: {missing_fields}")
            else:
                print("✅ All required fields present")
            
            print(f"Difficulty: {result.get('difficulty_level', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Show cost summary
    print("\n" + "=" * 60)
    print("COST SUMMARY")
    print("=" * 60)
    print(explainer.get_cost_summary())
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_concept_explanation()