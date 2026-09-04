# AI Engineering Tutor — Project Reflection

## Project Overview

AI Engineering Tutor is an AI-powered learning application designed to help engineering students understand technical concepts through structured explanations.

The current MVP allows a user to enter an engineering concept and receive an AI-generated explanation containing a definition, key formula, step-by-step application, real-world example, analogy, common mistakes, and difficulty level.

The project was built with Python, Streamlit, and the OpenAI API.

---

## Why I Built This Project

Engineering students often encounter concepts that are difficult to understand from a definition or formula alone.

I wanted to explore whether an AI system could provide explanations in a more structured learning format rather than simply returning a general answer.

The goal was to create a tutor that breaks a concept into several useful components:

- What does the concept mean?
- What is the important formula?
- How is it applied?
- Where is it used in the real world?
- What is an intuitive way to understand it?
- What mistakes do students commonly make?

This became the foundation of the AI Engineering Tutor.

---

## What I Built

The current version includes four main components.

### 1. Tutor Engine

The Tutor Engine handles communication with the AI API.

It is responsible for:

- Initializing the AI client
- Sending system and user prompts
- Providing engineering context
- Managing model responses
- Integrating API usage tracking

Separating the AI logic from the user interface made the application easier to organize and extend.

### 2. Concept Explainer

The Concept Explainer is responsible for converting a user's topic into a structured tutoring request.

Instead of asking the model a simple question such as:

> Explain Ohm's Law.

I designed the prompt to request specific educational components.

The expected response contains:

- Definition
- Key formula
- Step-by-step application
- Real-world example
- Common mistakes
- Analogy
- Difficulty level

The response is returned in JSON format so that each component can be displayed separately in the application.

### 3. Streamlit Interface

I built an interactive Streamlit interface where users can:

- Enter an engineering concept
- Select example topics
- Generate an explanation
- View each part of the explanation in a structured interface
- Review recent explanations during the session
- Download an explanation as a text file

The interface helped turn the underlying AI functionality into an application that someone could actually interact with.

### 4. API Cost Tracking

I also implemented API usage and cost tracking.

The application records usage by operation and displays the total estimated API cost in the Streamlit sidebar.

I included this because cost is an important consideration when designing applications that rely on external AI services.

---

# Key Technical Challenges

## Challenge 1: Getting Consistent AI Responses

One of the first challenges was response consistency.

Even when an AI model is given similar prompts, the exact structure of its response can vary. That becomes a problem when an application needs to extract individual fields and display them in different parts of the interface.

### My Approach

I created a detailed prompt that explicitly requests a structured JSON response.

Instead of accepting arbitrary text, the application expects fields such as:

```json
{
  "concept": "...",
  "definition": "...",
  "key_formula": "...",
  "step_by_step": "...",
  "real_world_example": "...",
  "common_mistakes": [],
  "analogy": "...",
  "difficulty_level": "..."
}
