"""
AI Engineering Tutor - Main Application
Streamlit UI for the engineering tutoring system
"""

import streamlit as st
import time
from datetime import datetime
from dotenv import load_dotenv
from tutor_engine import TutorEngine
from concept_explainer import ConceptExplainer

# Load environment variables
load_dotenv()

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Engineering Tutor",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'tutor_engine' not in st.session_state:
    st.session_state.tutor_engine = TutorEngine()

if 'concept_explainer' not in st.session_state:
    st.session_state.concept_explainer = ConceptExplainer(st.session_state.tutor_engine)

if 'cost_data' not in st.session_state:
    st.session_state.cost_data = {
        'total_cost': 0.0,
        'operations': {}
    }

if 'explanation_history' not in st.session_state:
    st.session_state.explanation_history = []

# Custom CSS for dark mode
st.markdown("""
    <style>
    /* Dark mode background */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* Main container background */
    .main > div {
        background-color: #0e1117 !important;
    }
    
    /* All text white by default */
    body, .stTextInput label, .stSelectbox label, .stRadio label, .stCheckbox label {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
    }
    
    /* Paragraph text */
    p, li, .stMarkdown, .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B !important;
        margin-bottom: 1rem;
    }
    
    /* Feature boxes - dark style */
    .feature-box {
        background-color: #1e1e2e !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #ffffff !important;
    }
    
    .definition-box {
        background-color: #1a2a1a !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50 !important;
        margin: 0.5rem 0;
        color: #ffffff !important;
    }
    
    .formula-box {
        background-color: #2a1a0a !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9800 !important;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 1.1rem;
        color: #ffffff !important;
    }
    
    .example-box {
        background-color: #0a1a2a !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196F3 !important;
        margin: 0.5rem 0;
        color: #ffffff !important;
    }
    
    .mistake-box {
        background-color: #2a0a0a !important;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336 !important;
        margin: 0.3rem 0;
        color: #ffffff !important;
    }
    
    .analogy-box {
        background-color: #1a0a2a !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #9C27B0 !important;
        margin: 0.5rem 0;
        color: #ffffff !important;
    }
    
    /* Buttons - keep red but readable */
    .stButton button {
        width: 100%;
        background-color: #FF4B4B !important;
        color: #ffffff !important;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #ff6b6b !important;
        color: #ffffff !important;
    }
    
    /* Text input - dark style */
    .stTextInput input {
        color: #ffffff !important;
        background-color: #1e1e2e !important;
        border: 1px solid #444 !important;
    }
    .stTextInput label {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1v3fvcr, .css-1q8dd3e {
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: #1a1a2e !important;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label {
        color: #ffffff !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #ffffff !important;
    }
    .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
    }
    
    /* Metrics */
    .stMetric label {
        color: #ffffff !important;
    }
    .stMetric .css-1xarl3l {
        color: #ffffff !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color: #ffffff !important;
        background-color: #1e1e2e !important;
    }
    .streamlit-expanderContent {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    /* Info, Warning, Success, Error boxes */
    .stAlert {
        color: #ffffff !important;
    }
    .stAlert p {
        color: #ffffff !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #1e1e2e !important;
        color: #ffffff !important;
    }
    
    /* Captions */
    .stCaption, .stCaption p {
        color: #aaaaaa !important;
    }
    
    /* Divider */
    hr {
        border-color: #444 !important;
    }
    
    /* Download button text */
    .stDownloadButton button {
        background-color: #FF4B4B !important;
        color: #ffffff !important;
    }
    .stDownloadButton button:hover {
        background-color: #ff6b6b !important;
        color: #ffffff !important;
    }
    
    /* Fix any remaining dark text */
    div, span, .stMarkdown div, .stMarkdown span {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main title and description
def display_header():
    """Display the main header"""
    st.markdown('<div class="main-header">🔧 AI Engineering Tutor</div>', unsafe_allow_html=True)
    st.markdown("""
    Your personal AI tutor for engineering concepts. 
    Get clear explanations, practice problems, and quizzes.
    """)
    st.markdown("---")

# Navigation sidebar
def display_sidebar():
    """Display the navigation sidebar"""
    with st.sidebar:
        st.title("🔧 AI Tutor")
        st.markdown("---")
        
        # Navigation - simplified
        page = st.radio(
            "Choose a Mode:",
            ["🏠 Home", "📚 Explain Concept"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Cost display
        st.subheader("💰 API Usage")
        total_cost = st.session_state.tutor_engine.get_total_cost()
        st.metric("Total Cost", f"${total_cost:.4f}")
        
        # Operations breakdown
        with st.expander("📊 Cost Details"):
            cost_data = st.session_state.tutor_engine.cost_tracker.get_operation_stats()
            if cost_data:
                for op, data in cost_data.items():
                    st.write(f"**{op}:** ${data['total_cost']:.4f} ({data['count']} calls)")
            else:
                st.write("No operations recorded yet")
        
        st.markdown("---")
        st.caption("Built for Engineering Students")
        st.caption(f"Session started: {datetime.now().strftime('%H:%M:%S')}")
        
        return page

# Home page
def show_home():
    """Display the home page"""
    st.header("🏠 Welcome to AI Engineering Tutor!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 What You Can Do
        
        **1. Explain Concepts**
        - Get clear explanations of engineering concepts
        - Includes definition, formula, applications
        - Real-world examples and common mistakes
        
        **2. Generate Practice Problems** (Coming Soon)
        - Choose topic and difficulty
        - Get step-by-step solutions
        
        **3. Take Quizzes** (Coming Soon)
        - Multiple-choice questions
        - Instant feedback
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Quick Start
        
        1. Select **"Explain Concept"** from the sidebar
        2. Type any engineering concept
        3. Get a comprehensive explanation
        4. Review and save your explanations
        
        ### 🎯 Example Topics
        - Ohm's Law
        - Thevenin's Theorem
        - Newton's Second Law
        - First Law of Thermodynamics
        - Fourier Transform
        """)
    
    st.markdown("---")
    
    # Show recent explanations
    if st.session_state.explanation_history:
        st.subheader("📖 Recent Explanations")
        for item in st.session_state.explanation_history[-3:]:
            with st.expander(f"📝 {item['concept']}"):
                st.write(item.get('definition', '')[:200] + "...")
    else:
        st.info("💡 No explanations yet. Start by explaining a concept!")

# Concept explanation page
def show_concept_explanation():
    """Display the concept explanation interface"""
    st.header("📚 Explain Engineering Concept")
    st.markdown("Get a comprehensive explanation of any engineering concept")
    
    # Initialize session state for concept input if not exists
    if 'concept_input' not in st.session_state:
        st.session_state.concept_input = ""
    
    # Input form
    with st.form("concept_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            concept = st.text_input(
                "Enter the concept you want to explain:",
                value=st.session_state.concept_input,
                placeholder="e.g., Ohm's Law, Thevenin's Theorem, Newton's Second Law",
                help="Be specific for best results"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("🔍 Explain Concept", use_container_width=True)
    
    # Example concepts - moved outside the form
    st.markdown("### 💡 Try These Examples:")
    examples = ["Ohm's Law", "Thevenin's Theorem", "Newton's Second Law", 
               "First Law of Thermodynamics", "Fourier Transform"]
    
    # Create example buttons in a grid
    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(f"📝 {example}", key=f"ex_{i}"):
                # Set the concept input and rerun
                st.session_state.concept_input = example
                st.rerun()
    
    # Handle submission
    if submit_button and concept:
        with st.spinner(f"Generating explanation for '{concept}'..."):
            try:
                # Get explanation
                explanation = st.session_state.concept_explainer.explain_concept(
                    concept=concept,
                    topic_context="General Engineering"
                )
                
                # Save to history
                st.session_state.explanation_history.append({
                    'concept': concept,
                    'timestamp': datetime.now().isoformat(),
                    'definition': explanation.get('definition', '')
                })
                
                # Display the explanation
                display_explanation(explanation)
                
                # Show cost
                total_cost = st.session_state.tutor_engine.get_total_cost()
                st.info(f"💰 Total cost so far: ${total_cost:.4f}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please check your API key and try again.")

def display_explanation(explanation: dict):
    """
    Display a structured explanation
    
    Args:
        explanation: Dictionary with explanation data
    """
    # Check for error
    if 'error' in explanation:
        st.error(f"Error: {explanation['error']}")
        return
    
    # Concept name
    concept_name = explanation.get('concept', 'Unknown Concept')
    st.markdown(f"## 📖 {concept_name}")
    
    # Difficulty level
    difficulty = explanation.get('difficulty_level', 'Intermediate')
    if difficulty == 'Basic':
        st.success(f"Level: {difficulty} 📘")
    elif difficulty == 'Intermediate':
        st.warning(f"Level: {difficulty} 📙")
    else:
        st.info(f"Level: {difficulty} 📕")
    
    st.markdown("---")
    
    # Definition
    st.subheader("📌 Definition")
    definition = explanation.get('definition', 'Definition not available')
    st.markdown(f'<div class="definition-box">{definition}</div>', unsafe_allow_html=True)
    
    # Key Formula
    st.subheader("📐 Key Formula")
    formula = explanation.get('key_formula', 'No formula available')
    st.markdown(f'<div class="formula-box">{formula}</div>', unsafe_allow_html=True)
    
    # Step-by-Step
    st.subheader("📋 Step-by-Step Application")
    steps = explanation.get('step_by_step', 'No step-by-step explanation available')
    st.markdown(steps)
    
    # Real-world Example
    st.subheader("🌍 Real-World Example")
    example = explanation.get('real_world_example', 'No example available')
    st.markdown(f'<div class="example-box">{example}</div>', unsafe_allow_html=True)
    
    # Analogy
    st.subheader("🔍 Analogy for Understanding")
    analogy = explanation.get('analogy', 'No analogy available')
    st.markdown(f'<div class="analogy-box">{analogy}</div>', unsafe_allow_html=True)
    
    # Common Mistakes
    st.subheader("⚠️ Common Mistakes to Avoid")
    mistakes = explanation.get('common_mistakes', ['No mistakes listed'])
    if isinstance(mistakes, list):
        for mistake in mistakes:
            st.markdown(f'<div class="mistake-box">• {mistake}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mistake-box">{mistakes}</div>', unsafe_allow_html=True)
    
    # Raw response toggle (for debugging)
    if 'raw_response' in explanation:
        with st.expander("🔧 Raw Response (for debugging)"):
            st.code(explanation['raw_response'], language='json')
    
    # Download button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📥 Download Explanation", use_container_width=True):
            # Create text file content
            content = f"""
            CONCEPT EXPLANATION
            ===================
            
            Concept: {concept_name}
            Difficulty: {difficulty}
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            DEFINITION:
            {definition}
            
            KEY FORMULA:
            {formula}
            
            STEP-BY-STEP APPLICATION:
            {steps}
            
            REAL-WORLD EXAMPLE:
            {example}
            
            ANALOGY:
            {analogy}
            
            COMMON MISTAKES:
            {chr(10).join(['- ' + m for m in (mistakes if isinstance(mistakes, list) else [mistakes])])}
            """
            
            st.download_button(
                label="📄 Download as Text File",
                data=content,
                file_name=f"{concept_name.replace(' ', '_')}_explanation.txt",
                mime="text/plain"
            )

# Main execution
def main():
    """Main application entry point"""
    # Display header
    display_header()
    
    # Get navigation choice
    page = display_sidebar()
    
    # Show appropriate page
    if page == "🏠 Home":
        show_home()
    elif page == "📚 Explain Concept":
        show_concept_explanation()

if __name__ == "__main__":
    main()