"""
AI Engineering Tutor - Main Application
Streamlit UI for the engineering tutoring system.
"""

import html
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from tutor_engine import TutorEngine
from concept_explainer import ConceptExplainer


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Engineering Tutor",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "tutor_engine" not in st.session_state:
    st.session_state.tutor_engine = TutorEngine()

if "concept_explainer" not in st.session_state:
    st.session_state.concept_explainer = ConceptExplainer(
        st.session_state.tutor_engine
    )

if "explanation_history" not in st.session_state:
    st.session_state.explanation_history = []

if "concept_input" not in st.session_state:
    st.session_state.concept_input = ""


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MAIN APP
    -------------------------------------------------------- */

    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* --------------------------------------------------------
       MAIN TITLE
    -------------------------------------------------------- */

    .main-header {
        font-size: 2.6rem;
        font-weight: 750;
        margin-bottom: 0.3rem;
        color: #ff4b4b;
        letter-spacing: -0.5px;
    }

    .main-subtitle {
        font-size: 1.05rem;
        color: #b7bec9;
        margin-bottom: 1.5rem;
    }

    /* --------------------------------------------------------
       GENERAL TEXT
    -------------------------------------------------------- */

    h1, h2, h3, h4, h5, h6 {
        color: #f5f7fa;
    }

    p, li, label {
        color: #e6edf3;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f5f7fa;
    }

    /* --------------------------------------------------------
       TEXT INPUTS
    -------------------------------------------------------- */

    .stTextInput input {
        background-color: #1e2329;
        color: #ffffff;
        border: 1px solid #3d444d;
        border-radius: 8px;
    }

    .stTextInput input:focus {
        border-color: #ff4b4b;
        box-shadow: 0 0 0 1px #ff4b4b;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.15s ease-in-out;
    }

    .stFormSubmitButton > button {
        background-color: #ff4b4b;
        color: #ffffff;
        border: 1px solid #ff4b4b;
    }

    .stFormSubmitButton > button:hover {
        background-color: #ff6868;
        border-color: #ff6868;
        color: #ffffff;
    }

    .stButton > button {
        background-color: #21262d;
        color: #f0f3f6;
        border: 1px solid #3d444d;
    }

    .stButton > button:hover {
        background-color: #30363d;
        border-color: #ff4b4b;
        color: #ffffff;
    }

    /* --------------------------------------------------------
       EXPLANATION CARDS
    -------------------------------------------------------- */

    .definition-box,
    .formula-box,
    .example-box,
    .analogy-box,
    .mistake-box {
        padding: 1rem 1.15rem;
        border-radius: 10px;
        margin: 0.5rem 0 1.25rem 0;
        line-height: 1.65;
        color: #f5f7fa;
    }

    .definition-box {
        background-color: #16251a;
        border-left: 4px solid #4caf50;
    }

    .formula-box {
        background-color: #2a2115;
        border-left: 4px solid #ff9800;
        font-family: monospace;
        font-size: 1.05rem;
    }

    .example-box {
        background-color: #152330;
        border-left: 4px solid #2196f3;
    }

    .analogy-box {
        background-color: #25172e;
        border-left: 4px solid #9c27b0;
    }

    .mistake-box {
        background-color: #2b1717;
        border-left: 4px solid #f44336;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    /* --------------------------------------------------------
       FEATURE CARDS
    -------------------------------------------------------- */

    .feature-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.25rem;
        min-height: 220px;
        margin-bottom: 1rem;
    }

    .feature-card h3 {
        margin-top: 0;
    }

    /* --------------------------------------------------------
       METRICS
    -------------------------------------------------------- */

    [data-testid="stMetric"] {
        background-color: #1e2329;
        padding: 0.8rem;
        border: 1px solid #30363d;
        border-radius: 10px;
    }

    /* --------------------------------------------------------
       EXPANDERS
    -------------------------------------------------------- */

    [data-testid="stExpander"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }

    /* --------------------------------------------------------
       ALERTS
    -------------------------------------------------------- */

    [data-testid="stAlert"] {
        border-radius: 8px;
    }

    /* --------------------------------------------------------
       DOWNLOAD BUTTON
    -------------------------------------------------------- */

    .stDownloadButton > button {
        width: 100%;
        background-color: #238636;
        color: white;
        border: 1px solid #2ea043;
        border-radius: 8px;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        background-color: #2ea043;
        color: white;
        border-color: #3fb950;
    }

    /* --------------------------------------------------------
       DIVIDER
    -------------------------------------------------------- */

    hr {
        border-color: #30363d;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer-text {
        text-align: center;
        color: #8b949e;
        font-size: 0.85rem;
        margin-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe_html(value) -> str:
    """
    Escape model-generated content before inserting it into custom HTML.
    """
    if value is None:
        return ""

    text = str(value)
    escaped = html.escape(text)
    return escaped.replace("\n", "<br>")


def select_example(example: str):
    """
    Set an example concept in the text input.
    """
    st.session_state.concept_input = example


def build_download_content(
    concept_name,
    difficulty,
    definition,
    formula,
    steps,
    example,
    analogy,
    mistakes,
):
    """
    Build plain-text content for the explanation download.
    """

    if isinstance(mistakes, list):
        mistakes_text = "\n".join(f"- {mistake}" for mistake in mistakes)
    else:
        mistakes_text = f"- {mistakes}"

    return f"""AI ENGINEERING TUTOR
CONCEPT EXPLANATION
========================================

Concept: {concept_name}
Difficulty: {difficulty}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

DEFINITION
----------------------------------------
{definition}

KEY FORMULA
----------------------------------------
{formula}

STEP-BY-STEP APPLICATION
----------------------------------------
{steps}

REAL-WORLD EXAMPLE
----------------------------------------
{example}

ANALOGY
----------------------------------------
{analogy}

COMMON MISTAKES
----------------------------------------
{mistakes_text}

========================================
Generated with AI Engineering Tutor
"""


# ============================================================
# HEADER
# ============================================================

def display_header():
    """
    Display the main application header.
    """

    st.markdown(
        '<div class="main-header">🔧 AI Engineering Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-subtitle">
        An AI-powered tutor that transforms complex engineering concepts into
        clear explanations, formulas, step-by-step reasoning, real-world
        examples, analogies, and common mistakes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


# ============================================================
# SIDEBAR
# ============================================================

def display_sidebar():
    """
    Display navigation and API usage information.
    """

    with st.sidebar:

        st.title("🔧 AI Tutor")
        st.caption("Engineering learning assistant")

        st.markdown("---")

        page = st.radio(
            "Choose a Mode",
            [
                "🏠 Home",
                "📚 Explain Concept",
            ],
            key="navigation",
        )

        st.markdown("---")

        st.subheader("💰 API Usage")

        try:
            total_cost = st.session_state.tutor_engine.get_total_cost()
            st.metric("Total Cost", f"${total_cost:.4f}")
        except Exception:
            st.metric("Total Cost", "$0.0000")

        with st.expander("📊 Cost Details"):

            try:
                cost_data = (
                    st.session_state
                    .tutor_engine
                    .cost_tracker
                    .get_operation_stats()
                )

                if cost_data:
                    for operation, data in cost_data.items():

                        cost = data.get("total_cost", 0)
                        count = data.get("count", 0)

                        st.write(
                            f"**{operation}:** "
                            f"${cost:.4f} "
                            f"({count} calls)"
                        )

                else:
                    st.caption("No API operations recorded yet.")

            except Exception:
                st.caption("Cost details unavailable.")

        st.markdown("---")

        st.caption("Built for engineering students")
        st.caption(
            f"Session started: "
            f"{datetime.now().strftime('%H:%M:%S')}"
        )

        return page


# ============================================================
# HOME PAGE
# ============================================================

def show_home():
    """
    Display home page.
    """

    st.header("🏠 Welcome")

    st.write(
        """
        AI Engineering Tutor helps students break down difficult engineering
        topics into structured explanations designed for learning rather than
        simple one-line answers.
        """
    )

    st.markdown("### 🚀 What the Tutor Can Do")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <h3>📚 Explain Concepts</h3>
                <p>
                Explore engineering topics using definitions, formulas,
                step-by-step explanations, applications, analogies,
                and common mistakes.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <h3>🧠 Structured Learning</h3>
                <p>
                Explanations are organized into consistent sections so
                students can understand both the theory and how the concept
                is applied.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <h3>💡 Real-World Context</h3>
                <p>
                Connect abstract engineering principles to real systems,
                applications, and intuitive analogies.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.subheader("🚀 Quick Start")

        st.markdown(
            """
            1. Select **Explain Concept** from the sidebar.
            2. Enter an engineering concept.
            3. Generate the explanation.
            4. Review the formula, steps, examples, and common mistakes.
            5. Download the explanation for later review.
            """
        )

    with right:

        st.subheader("🎯 Example Topics")

        st.markdown(
            """
            - Ohm's Law
            - Thevenin's Theorem
            - Newton's Second Law
            - First Law of Thermodynamics
            - Fourier Transform
            """
        )

    st.markdown("---")

    if st.session_state.explanation_history:

        st.subheader("📖 Recent Explanations")

        recent_items = st.session_state.explanation_history[-3:]

        for item in reversed(recent_items):

            concept = item.get("concept", "Unknown Concept")
            definition = item.get("definition", "")

            with st.expander(f"📝 {concept}"):

                if definition:
                    preview = definition[:300]

                    if len(definition) > 300:
                        preview += "..."

                    st.write(preview)

                timestamp = item.get("timestamp")

                if timestamp:
                    st.caption(f"Generated: {timestamp}")

    else:

        st.info(
            "💡 You haven't generated an explanation yet. "
            "Open **Explain Concept** to get started."
        )


# ============================================================
# CONCEPT EXPLANATION PAGE
# ============================================================

def show_concept_explanation():
    """
    Display the concept explanation interface.
    """

    st.header("📚 Explain an Engineering Concept")

    st.write(
        """
        Enter an engineering topic and the AI tutor will create a structured
        learning explanation.
        """
    )

    # --------------------------------------------------------
    # EXAMPLE BUTTONS
    # --------------------------------------------------------

    st.markdown("### 💡 Try an Example")

    examples = [
        "Ohm's Law",
        "Thevenin's Theorem",
        "Newton's Second Law",
        "First Law of Thermodynamics",
        "Fourier Transform",
    ]

    cols = st.columns(5)

    for index, example in enumerate(examples):

        with cols[index]:

            st.button(
                example,
                key=f"example_{index}",
                on_click=select_example,
                args=(example,),
                use_container_width=True,
            )

    st.markdown("")

    # --------------------------------------------------------
    # INPUT FORM
    # --------------------------------------------------------

    with st.form("concept_form"):

        concept = st.text_input(
            "Engineering concept",
            key="concept_input",
            placeholder=(
                "e.g., Ohm's Law, Fourier Transform, "
                "Bernoulli's Principle"
            ),
            help="Enter a specific engineering concept for the best result.",
        )

        submit_button = st.form_submit_button(
            "🔍 Generate Explanation",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # SUBMISSION
    # --------------------------------------------------------

    if submit_button:

        concept = concept.strip()

        if not concept:

            st.warning(
                "Please enter an engineering concept before generating "
                "an explanation."
            )

            return

        with st.spinner(
            f"Generating an explanation for '{concept}'..."
        ):

            try:

                explanation = (
                    st.session_state
                    .concept_explainer
                    .explain_concept(
                        concept=concept,
                        topic_context="General Engineering",
                    )
                )

                if not isinstance(explanation, dict):
                    raise ValueError(
                        "The explanation service returned an "
                        "unexpected response."
                    )

                if "error" in explanation:

                    st.error(
                        explanation.get(
                            "error",
                            "The explanation could not be generated.",
                        )
                    )

                    return

                st.session_state.explanation_history.append(
                    {
                        "concept": concept,
                        "timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "definition": explanation.get(
                            "definition",
                            "",
                        ),
                    }
                )

                display_explanation(explanation)

                try:
                    total_cost = (
                        st.session_state
                        .tutor_engine
                        .get_total_cost()
                    )

                    st.caption(
                        f"💰 API usage this session: "
                        f"${total_cost:.4f}"
                    )

                except Exception:
                    pass

            except Exception as error:

                st.error(
                    "The explanation could not be generated."
                )

                st.info(
                    "Check that your API key is configured correctly "
                    "and that the AI service is available."
                )

                with st.expander("Technical details"):
                    st.code(str(error))


# ============================================================
# DISPLAY GENERATED EXPLANATION
# ============================================================

def display_explanation(explanation: dict):
    """
    Display a structured engineering explanation.
    """

    if "error" in explanation:

        st.error(
            explanation.get(
                "error",
                "An unknown error occurred.",
            )
        )

        return

    concept_name = explanation.get(
        "concept",
        "Engineering Concept",
    )

    difficulty = explanation.get(
        "difficulty_level",
        "Intermediate",
    )

    definition = explanation.get(
        "definition",
        "Definition not available.",
    )

    formula = explanation.get(
        "key_formula",
        "No key formula was provided.",
    )

    steps = explanation.get(
        "step_by_step",
        "No step-by-step explanation was provided.",
    )

    example = explanation.get(
        "real_world_example",
        "No real-world example was provided.",
    )

    analogy = explanation.get(
        "analogy",
        "No analogy was provided.",
    )

    mistakes = explanation.get(
        "common_mistakes",
        ["No common mistakes were provided."],
    )

    st.markdown("---")

    st.markdown(f"## 📖 {concept_name}")

    # --------------------------------------------------------
    # DIFFICULTY
    # --------------------------------------------------------

    difficulty_lower = str(difficulty).lower()

    if difficulty_lower == "basic":
        st.success(f"📘 Difficulty: {difficulty}")

    elif difficulty_lower == "intermediate":
        st.warning(f"📙 Difficulty: {difficulty}")

    else:
        st.info(f"📕 Difficulty: {difficulty}")

    # --------------------------------------------------------
    # DEFINITION
    # --------------------------------------------------------

    st.subheader("📌 Definition")

    st.markdown(
        f"""
        <div class="definition-box">
            {safe_html(definition)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FORMULA
    # --------------------------------------------------------

    st.subheader("📐 Key Formula")

    st.markdown(
        f"""
        <div class="formula-box">
            {safe_html(formula)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # STEP-BY-STEP
    # --------------------------------------------------------

    st.subheader("📋 Step-by-Step Application")

    if isinstance(steps, list):

        for number, step in enumerate(steps, start=1):
            st.markdown(f"**{number}.** {step}")

    else:
        st.markdown(str(steps))

    # --------------------------------------------------------
    # REAL-WORLD EXAMPLE
    # --------------------------------------------------------

    st.subheader("🌍 Real-World Example")

    st.markdown(
        f"""
        <div class="example-box">
            {safe_html(example)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # ANALOGY
    # --------------------------------------------------------

    st.subheader("🔍 Analogy")

    st.markdown(
        f"""
        <div class="analogy-box">
            {safe_html(analogy)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # COMMON MISTAKES
    # --------------------------------------------------------

    st.subheader("⚠️ Common Mistakes")

    if isinstance(mistakes, list):

        for mistake in mistakes:

            st.markdown(
                f"""
                <div class="mistake-box">
                    • {safe_html(mistake)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.markdown(
            f"""
            <div class="mistake-box">
                {safe_html(mistakes)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.markdown("---")

    download_content = build_download_content(
        concept_name=concept_name,
        difficulty=difficulty,
        definition=definition,
        formula=formula,
        steps=steps,
        example=example,
        analogy=analogy,
        mistakes=mistakes,
    )

    safe_filename = (
        str(concept_name)
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.download_button(
            label="📥 Download Explanation",
            data=download_content,
            file_name=f"{safe_filename}_explanation.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

def display_footer():
    """
    Display application footer.
    """

    st.markdown(
        """
        <div class="footer-text">
            AI Engineering Tutor • Built with Python, Streamlit, and AI
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """
    Main application entry point.
    """

    display_header()

    page = display_sidebar()

    if page == "🏠 Home":
        show_home()

    elif page == "📚 Explain Concept":
        show_concept_explanation()

    display_footer()


if __name__ == "__main__":
    main()