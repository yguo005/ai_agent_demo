# 🤖 Intelligent Incident Response Agent

This project is a demonstration of an advanced, AI-powered cybersecurity pipeline built for the AI Agent Hackathon. It features a coordinated system of three intelligent agents that work together to automatically detect, analyze, and remediate security threats in real-time.

## Core Concept

The system is built on a three-agent pipeline, where each agent has a specialized role:

1.  **🚨 The Monitor**: Ingests raw security alerts from various sources.
2.  **🧠 The Analyzer**: Enriches the raw data with business context using a knowledge base and evaluates the true risk using a large language model.
3.  **⚙️ The Orchestrator**: Takes the AI-driven recommendation and executes an automated remediation action, such as isolating a host or patching a system.

This multi-agent approach transforms a simple security alert into an intelligent, automated response that considers business impact and operational context.

---

## 🏆 Sponsor Technology Integration

This project proudly integrates technologies from **5 key sponsors**, showcasing a modern, AI-native approach to security automation.

| Sponsor         | Category      | How It's Used in this Project                                                                                                                                                             |
| :-------------- | :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Horizon3.ai** | 📊 Power Data | **Simulated Threat Ingestion**: The demo simulates receiving critical vulnerability alerts from Horizon3.ai, acting as a primary trigger for the incident response pipeline. (`simulated_data.py`) |
| **Redis**       | 📊 Power Data | **High-Speed Messaging (Pacer)**: Redis serves as the communication backbone for the agents. The `pacer.py` module uses Redis Pub/Sub to pass threats from one agent to the next.       |
| **LlamaIndex**  | 🧠 Add Smarts | **Knowledge Base & Context**: LlamaIndex is used to build and query a knowledge base (`knowledge_base.md`) of the company's assets, enabling the AI to understand the business context of a threat. |
| **HoneyHive**   | 🧠 Add Smarts | **AI Observability (MCP)**: HoneyHive is integrated to trace and log the AI's decision-making process. It wraps the OpenAI calls, providing crucial observability and fulfilling the MCP requirement. |
| **OpenAI**      | 🧠 Add Smarts | **Core Intelligence**: OpenAI's GPT-4 is the large language model that performs the risk analysis, severity justification, and recommends the final remediation action.                         |

---

## 🏗️ System Architecture

The agents communicate in a seamless pipeline, passing data through the Redis Pacer.

```
 Threat Sources
(Horizon3, Bright Data)
       │
       ▼
┌──────────────────┐
│ 🚨 Agent 1:      │
│     Monitor      │
└──────────────────┘
       │
       │ (Publishes Raw Threat via Redis)
       ▼
┌──────────────────┐   ┌────────────────────┐
│ 🧠 Agent 2:      │──▶│   Knowledge Base   │
│     Analyzer     │   │   (LlamaIndex)     │
└──────────────────┘   └────────────────────┘
       │
       │ (Publishes Enriched Analysis via Redis)
       ▼
┌──────────────────┐   ┌────────────────────┐
│ ⚙️ Agent 3:      │──▶│  Remediation APIs  │
│    Orchestrator  │   │ (Qodo / Speakeasy) │
└──────────────────┘   └────────────────────┘
       │
       ▼
  Action Taken
```

---

## 🚀 How to Run the Demo

### 1. Setup

```bash
# Install all required packages
pip install -r requirements.txt

# Copy the environment file
cp .env.example .env

# Add your API keys to the .env file
# (At minimum, OPENAI_API_KEY is required)
```

### 2. Run the Streamlit UI

The best way to experience the demo is through the interactive Streamlit interface.

```bash
python3 -m streamlit run demo_app.py
```

From the UI, you can:
*   Inject different threat scenarios from the sidebar.
*   Watch the pipeline execute in real-time across the three columns.
*   View the status of each integrated sponsor technology.
*   See a history of completed pipeline runs.

Demo: https://youtu.be/wbw2SM_R9r8
