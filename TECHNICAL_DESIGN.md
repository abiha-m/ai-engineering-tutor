# Technical Design Document — AI Engineering Tutor

## 1. System Overview

AI Engineering Tutor is an AI-powered educational application designed to generate structured explanations of engineering concepts.

The current MVP is built with Python and Streamlit and integrates with the OpenAI API to transform a user-entered engineering concept into a structured learning response.

Each generated explanation can include:

- Definition
- Key formula
- Step-by-step application
- Real-world example
- Analogy
- Common mistakes
- Difficulty level

The system also includes API usage and cost tracking, session-based explanation history, error handling, and downloadable explanations.

---

## 2. Current Scope

### Implemented

The current version includes:

- AI-generated engineering concept explanations
- Structured AI response generation
- Engineering context injection
- JSON response parsing
- Streamlit user interface
- Example concept selection
- Session-based explanation history
- API usage and cost tracking
- Downloadable explanations
- Basic Concept Explainer testing
- Environment-based API credential management

### Planned

The following features are potential future extensions and are **not part of the current implementation**:

- Practice problem generation
- Student solution checking
- Quiz generation
- Topic review workflows
- PDF upload
- Retrieval-Augmented Generation (RAG)
- Persistent student progress
- User authentication
- Cloud deployment

---

# 3. System Architecture

## 3.1 High-Level Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │      app.py         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Tutor Engine     │
                    │  tutor_engine.py    │
                    └───────┬─────┬───────┘
                            │     │
                  AI request│     │usage data
                            │     │
                            ▼     ▼
              ┌────────────────┐  ┌─────────────────┐
              │Concept Explainer│  │  Cost Tracker   │
              │concept_         │  │cost_tracker.py  │
              │explainer.py     │  └─────────────────┘
              └───────┬─────────┘
                      │
                      ▼
              ┌─────────────────┐
              │   OpenAI API    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │Structured Model │
              │    Response     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │Response Parsing │
              │  + Validation   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Streamlit View  │
              └─────────────────┘
```

---

# 4. Request Flow

A typical concept-explanation request follows this sequence:

1. The user enters an engineering concept in the Streamlit interface.
2. `app.py` sends the concept to the `ConceptExplainer`.
3. `ConceptExplainer` requests relevant engineering context from the `TutorEngine`.
4. `ConceptExplainer` constructs a structured system and user prompt.
5. The request is passed through the `TutorEngine`.
6. `TutorEngine` communicates with the OpenAI API.
7. API usage information is recorded by the `CostTracker`.
8. The model response is returned to `ConceptExplainer`.
9. The response is cleaned and parsed into structured JSON.
10. `app.py` displays each educational component separately.
11. A summary of the explanation is stored in Streamlit session state.
12. The user can optionally download the explanation as a text file.

---

# 5. Component Design

## 5.1 Streamlit Application — `app.py`

### Responsibility

`app.py` provides the presentation layer and coordinates user interaction with the tutoring system.

### Current Responsibilities

- Configure the Streamlit application
- Initialize session state
- Initialize `TutorEngine`
- Initialize `ConceptExplainer`
- Display navigation
- Accept engineering concept input
- Provide example concepts
- Trigger explanation generation
- Display structured explanation sections
- Display API cost information
- Maintain session explanation history
- Handle user-facing errors
- Generate downloadable explanation files

### Main Functions

| Function | Responsibility |
|---|---|
| `main()` | Main application entry point |
| `display_header()` | Displays application title and description |
| `display_sidebar()` | Displays navigation and API usage information |
| `show_home()` | Displays project overview and recent explanations |
| `show_concept_explanation()` | Handles concept input and generation |
| `display_explanation()` | Renders structured explanation output |
| `build_download_content()` | Creates downloadable text representation |
| `safe_html()` | Escapes generated text before custom HTML rendering |

### Session State

Streamlit session state is used to maintain application data between reruns.

Current state includes:

```python
{
    "tutor_engine": TutorEngine,
    "concept_explainer": ConceptExplainer,
    "explanation_history": list,
    "concept_input": str
}
```

This allows the application to maintain history and reuse initialized components during the active session.

---

# 6. Tutor Engine — `tutor_engine.py`

## Responsibility

The Tutor Engine acts as the shared AI-service layer of the application.

It separates API communication from feature-specific prompt logic.

### Responsibilities

- Initialize the OpenAI client
- Manage AI model requests
- Accept system and user prompts
- Provide engineering context
- Configure generation parameters
- Integrate with the Cost Tracker
- Return generated responses
- Expose API usage information

### Design Rationale

Separating AI communication from the Concept Explainer makes the system easier to extend.

Future modules could reuse the same engine:

```text
                    TutorEngine
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
ConceptExplainer   ProblemGenerator   QuizEngine
   CURRENT             FUTURE          FUTURE
```

Only the Concept Explainer is currently implemented.

---

# 7. Concept Explainer — `concept_explainer.py`

## Responsibility

The Concept Explainer converts an engineering concept into a structured tutoring request and processes the resulting model response.

### Primary Workflow

```text
Engineering Concept
        │
        ▼
Engineering Context
        │
        ▼
Structured Prompt
        │
        ▼
Tutor Engine
        │
        ▼
AI Response
        │
        ▼
Response Cleaning
        │
        ▼
JSON Parsing
        │
        ▼
Structured Explanation
```

### Main Operations

#### `explain_concept()`

Accepts:

```python
concept: str
topic_context: str
```

and generates a structured explanation.

#### `explain_multiple()`

Provides support for requesting explanations for multiple concepts.

#### Cost Methods

The component can access cost information through the Tutor Engine.

---

# 8. Structured Explanation Model

The application expects a concept explanation with approximately the following structure:

```python
{
    "concept": str,
    "definition": str,
    "key_formula": str,
    "step_by_step": str,
    "real_world_example": str,
    "common_mistakes": list[str],
    "analogy": str,
    "difficulty_level": str
}
```

### Field Definitions

| Field | Description |
|---|---|
| `concept` | Name of the engineering concept |
| `definition` | Explanation of the concept |
| `key_formula` | Important formula or mathematical relationship |
| `step_by_step` | Explanation of how the concept is applied |
| `real_world_example` | Practical application or example |
| `common_mistakes` | Common misconceptions or errors |
| `analogy` | Intuitive analogy for understanding |
| `difficulty_level` | Basic, Intermediate, or Advanced |

---

# 9. Prompt Engineering Strategy

## 9.1 Goal

The prompt is designed to produce educational content that can be reliably displayed by the application.

A general request such as:

```text
Explain Ohm's Law.
```

may produce useful information, but its structure can vary significantly.

The application instead defines:

- The model's role
- The educational objective
- The desired explanation style
- Required response fields
- Expected JSON structure

---

## 9.2 System Prompt Strategy

The system prompt establishes the model as an engineering tutor and emphasizes:

- Clear explanations
- Simple-to-complex reasoning
- Real-world examples
- Analogies
- Explanation of why concepts work
- Structured output

---

## 9.3 User Prompt Strategy

The user prompt supplies:

```text
Concept
+
Engineering Context
+
Required Explanation Components
+
Expected Output Structure
```

The requested output includes:

1. Definition
2. Key formula
3. Step-by-step application
4. Real-world example
5. Common mistakes
6. Analogy
7. Difficulty level

---

# 10. Response Processing

AI-generated output is treated as untrusted external input.

The application does not assume that every response will perfectly follow the requested format.

## Processing Pipeline

```text
Raw Model Response
        │
        ▼
Remove Markdown Code Fences
        │
        ▼
Attempt JSON Parsing
        │
        ├──── Success ────► Structured Dictionary
        │
        └──── Failure ────► Error/Fallback Handling
```

This is necessary because models may occasionally return JSON surrounded by Markdown formatting or otherwise deviate from the requested format.

---

# 11. Cost Tracking — `cost_tracker.py`

## Responsibility

The Cost Tracker provides visibility into AI API usage.

### Responsibilities

- Track usage by operation
- Track token usage
- Estimate request costs
- Store aggregate usage information
- Provide operation-level statistics

### Conceptual Data Structure

```python
{
    "total_cost": float,
    "total_tokens": int,
    "total_requests": int,

    "operations": {
        "explain_concept": {
            "count": int,
            "total_cost": float,
            "total_tokens": int,
            "input_tokens": int,
            "output_tokens": int
        }
    }
}
```

### Why Cost Tracking Matters

AI APIs introduce a variable resource cost.

Tracking usage makes it possible to reason about:

- Cost per operation
- Token consumption
- Application usage
- Future scalability
- Opportunities for prompt optimization

---

# 12. User Interface Design

The Streamlit interface currently contains two primary views.

## Home

The Home page provides:

- Project introduction
- Feature overview
- Quick-start instructions
- Example engineering topics
- Recent explanation history

## Explain Concept

The explanation page provides:

- Concept input
- Example concept buttons
- Generate Explanation action
- Loading indicator
- Structured explanation display
- Difficulty indicator
- API usage information
- Explanation download

### Explanation Presentation

Generated information is separated into visual sections:

```text
📖 Concept

📘 Difficulty

📌 Definition

📐 Key Formula

📋 Step-by-Step Application

🌍 Real-World Example

🔍 Analogy

⚠️ Common Mistakes

📥 Download Explanation
```

---

# 13. Error Handling

The application includes error handling at multiple layers.

## API Errors

API-related exceptions are caught so the application can display a user-friendly message rather than terminate unexpectedly.

## Response Errors

The system checks for error responses before attempting to display an explanation.

## JSON Parsing Errors

Model output is cleaned before JSON parsing.

Malformed responses are handled rather than assuming all model output is valid JSON.

## Empty User Input

The interface prevents an empty concept from being submitted for generation.

## UI-Level Handling

Unexpected exceptions during generation result in a user-facing error message.

---

# 14. Security Considerations

## API Credentials

The OpenAI API key is stored in an environment variable loaded from `.env`.

```text
OPENAI_API_KEY=...
```

The `.env` file is excluded from Git version control.

## Git Ignore Rules

Local development artifacts are excluded, including:

```text
.env
venv/
__pycache__/
```

## Generated Content

Model-generated text inserted into custom HTML components should be escaped before rendering.

This reduces the risk associated with directly injecting generated content into HTML.

## Data Persistence

The application currently does not maintain persistent user accounts or a permanent student learning database.

Explanation history is maintained for the active Streamlit session.

---

# 15. Testing Strategy

The current repository includes testing for the Concept Explainer.

Example engineering concepts include:

- Ohm's Law
- Thevenin's Theorem
- Newton's Second Law
- First Law of Thermodynamics
- Fourier Transform

Tests verify that generated explanations contain expected fields such as:

```text
definition
key_formula
step_by_step
real_world_example
common_mistakes
analogy
```

## Current Testing Limitation

Some testing relies on live API requests.

This creates several limitations:

- Tests may incur API cost
- Results can vary between runs
- Tests depend on network/API availability
- AI output is nondeterministic

## Recommended Future Testing

A stronger testing strategy would use mocked AI responses.

```text
Application
     │
     ▼
Mock Tutor Engine
     │
     ▼
Known AI Response
     │
     ▼
Deterministic Test
```

This would allow application logic to be tested independently from the external model.

---

# 16. Current Repository Structure

```text
ai-engineering-tutor/
│
├── app.py
│   └── Streamlit user interface
│
├── tutor_engine.py
│   └── AI request orchestration
│
├── concept_explainer.py
│   └── Prompt construction and response parsing
│
├── cost_tracker.py
│   └── API usage and cost tracking
│
├── test_concept_explainer.py
│   └── Concept Explainer testing
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project overview and setup
│
├── TECHNICAL_DESIGN.md
│   └── System architecture and design
│
├── reflections.md
│   └── Development reflection and lessons learned
│
└── .gitignore
    └── Git exclusions
```

Local files such as `.env`, `venv/`, `__pycache__/`, and usage data are intentionally excluded from version control.

---

# 17. Technology Stack

| Technology | Role |
|---|---|
| Python | Primary programming language |
| Streamlit | Web application interface |
| OpenAI API | AI-generated explanations |
| python-dotenv | Environment variable management |
| JSON | Structured response representation |
| tiktoken | Token counting/usage estimation |
| Git | Version control |
| GitHub | Source repository |

---

# 18. Design Decisions

## Modular Architecture

The project separates:

```text
UI
AI orchestration
Feature logic
Cost tracking
```

This reduces coupling and provides a foundation for additional features.

## Structured AI Output

JSON was selected instead of free-form output because the UI needs predictable fields.

## Session State

Streamlit session state is used because the framework reruns the application when users interact with widgets.

## Cost Visibility

Cost tracking was included early because API usage is a system-level consideration in AI applications.

## MVP Scope

The current application intentionally focuses on one core workflow:

> Generate a structured explanation of an engineering concept.

Additional educational features are treated as future work rather than partially represented as completed functionality.

---

# 19. Current Limitations

## Model Accuracy

AI-generated engineering explanations may contain incorrect or incomplete information.

The application should not be treated as an authoritative engineering reference.

## Schema Enforcement

The system requests structured JSON but does not currently use a strict schema-validation library.

## Testing

Automated testing is currently limited and some tests rely on external API calls.

## Persistence

Explanation history is session-based and is not stored permanently.

## Authentication

The system does not currently support user accounts.

## Personalization

The current implementation does not maintain a long-term student learning profile.

## Grounding

Responses currently rely primarily on the AI model rather than a verified engineering knowledge base.

---

# 20. Future Architecture

The modular architecture allows additional tutoring capabilities to be introduced later.

A possible future architecture is:

```text
                         Tutor Engine
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
 Concept Explainer     Problem Generator      Quiz Engine
     CURRENT                FUTURE               FUTURE
          │
          │
          └──────────────────────────┐
                                     │
                                     ▼
                              Knowledge Base
                               RAG / Documents
                                  FUTURE
```

Potential future components include:

### Problem Generator

Generate engineering practice problems at different difficulty levels.

### Solution Checker

Evaluate student reasoning and provide structured feedback.

### Quiz Engine

Generate quizzes with explanations for correct and incorrect answers.

### RAG Knowledge Base

Allow students to upload course material and generate responses grounded in their own notes.

### Student Progress System

Track:

- Studied topics
- Performance
- Difficult concepts
- Recommended review areas

---

# 21. Future Improvements

### Reliability

- Add strict response schema validation
- Improve malformed-response recovery
- Add retry handling where appropriate
- Expand automated tests

### AI Engineering

- Evaluate different model configurations
- Add grounded RAG responses
- Measure explanation consistency
- Evaluate factual accuracy

### Testing

- Mock external AI requests
- Add unit tests for Tutor Engine
- Add Cost Tracker tests
- Add UI workflow testing

### User Experience

- Improve mobile responsiveness
- Add conversation-based follow-up questions
- Add learning progress visualization
- Improve formula rendering

### Deployment

- Prepare cloud deployment configuration
- Configure secrets management
- Add monitoring
- Add rate limiting

---

# 22. Key Engineering Lessons

This project demonstrated several important principles of AI application development.

### 1. LLM output must be treated as external input

Even well-designed prompts do not guarantee perfectly structured responses.

### 2. Prompt design can function as an API contract

Structured prompts make downstream software integration easier.

### 3. AI functionality should be separated from UI logic

A dedicated Tutor Engine makes future feature development easier.

### 4. Cost is part of system design

AI requests consume resources and should be monitored.

### 5. State management matters

Interactive AI applications often need to maintain information across user actions.

### 6. AI applications require traditional software engineering

Prompt engineering alone is not enough.

Reliability also depends on:

- Architecture
- Testing
- Error handling
- Security
- Validation
- State management
- Documentation
- User experience

---

# 23. Project Status

**Status: MVP**

### Implemented

- [x] Concept explanation
- [x] Structured AI output
- [x] Prompt engineering
- [x] Engineering context
- [x] Streamlit interface
- [x] Session history
- [x] API usage/cost tracking
- [x] Explanation downloads
- [x] Basic Concept Explainer testing
- [x] Environment-based API credentials

### Planned

- [ ] Practice problem generation
- [ ] Solution checking
- [ ] Quiz generation
- [ ] PDF/RAG integration
- [ ] Persistent learning history
- [ ] User authentication
- [ ] Expanded automated testing
- [ ] Production deployment

---

# 24. Author

**Abiha Majid**

Engineering Student  
Northern Virginia Community College

Interests: Artificial Intelligence, Engineering, Intelligent Systems, and Applied AI Development

---

# 25. Related Project

## AI Research Assistant

A separate Retrieval-Augmented Generation (RAG) project focused on querying and understanding document content.

Repository:

https://github.com/abiha-m/ai-research-assistant

---

# 26. Documentation

Additional project documentation:

- [`README.md`](README.md) — project overview and setup
- [`reflections.md`](reflections.md) — development reflection and lessons learned

---

# 27. Version

**Current Version:** MVP / 1.0

The current release focuses on the engineering concept explanation workflow. Future versions may extend the architecture with additional educational and retrieval-based capabilities.