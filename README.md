# Diabetes Lifestyle Tracker Agent

This repository contains a LangGraph + LLM agent that helps a user track lifestyle habits such as meals, water intake, sleep, and physical activity. It also provides general nutritional information about foods.

> **Note:** This agent does **not give medical advice**. It is strictly a habit-logging assistant.

---

## Folder Contents

- `agent.py` – main agent code with LLM, tools, and graph nodes 
- `langgraph.json` – LangGraph configuration file 
- `requirements.txt` – Python dependencies 
- `requirementss.txt` – langgraph dependencies 
---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/balkisoues/diabetes_agent.git
cd diabetes_agent

### 1. Create python virtual env 
python3 -m venv venv
source venv/bin/activate

