# 🤖 Intelligent Incident Response Agent

A comprehensive AI-powered cybersecurity incident response system with three intelligent agents working in coordination to detect, analyze, and remediate security threats automatically.

## 🎯 Overview

This system implements a complete **Agent-to-Agent (A2A)** communication pipeline following the **Model Context Protocol (MCP)** for intelligent incident response:

1. **🚨 Threat Monitor Agent** - Detects threats from security tools
2. **🧠 Context Analyzer Agent** - Enriches threats with AI-powered business context  
3. **⚙️ Remediation Orchestrator Agent** - Executes appropriate remediation actions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Threat Monitor │────│ Context Analyzer│────│   Orchestrator  │
│     Agent       │    │     Agent       │    │     Agent       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
    Raw Threats            AI Analysis             Remediation
                              +                      Actions
                        Business Context
```

**Communication Backbone:** Redis (with in-memory fallback)
**AI Engine:** Anthropic Claude + OpenAI Embeddings
**Knowledge Base:** LlamaIndex Vector Store
**UI:** Streamlit Dashboard

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone and navigate
git clone https://github.com/yguo005/ai_agent_demo.git
cd ai_agent_demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 3. Run the Demo

**Option A: Streamlit Web Interface (Recommended)**
```bash
streamlit run demo_app.py
```

**Option B: Command Line Pipeline**
```bash
# Single threat execution
python main.py --mode single --source horizon3

# Continuous mode
python main.py --mode continuous

# Demo mode (all threat sources)
python main.py --mode demo
```

## 📊 Demo Scenarios

The system includes three realistic threat scenarios:

### 🔥 Scenario 1: Critical RCE (Horizon3.ai)
- **Target**: Finance server (srv-finance-01)
- **Threat**: Remote Code Execution vulnerability
- **Action**: Automatic host isolation
- **Business Impact**: PII and financial data at risk

### 🦠 Scenario 2: Malware Detection (Bright Data)  
- **Target**: Web server (web-server-02)
- **Threat**: Suspicious executable
- **Action**: System patching
- **Business Impact**: Customer-facing service compromise

### ⚠️ Scenario 3: SSL Certificate Issue
- **Target**: Database server (db-server-01)
- **Threat**: Expired certificate
- **Action**: Enhanced monitoring
- **Business Impact**: Customer data access issues

## 🧠 AI Intelligence Features

### Context Enrichment
- **Asset Discovery**: Maps IPs to business-critical systems
- **Owner Identification**: Finds responsible teams and contacts  
- **Impact Assessment**: Evaluates business risk and compliance requirements
- **Action Recommendation**: Suggests appropriate remediation steps

### Smart Decision Making
- **Risk Scoring**: Considers business context, not just technical severity
- **Escalation Logic**: Follows company policies and SLAs
- **Compliance Awareness**: Factors in SOX, PCI DSS, GDPR requirements
- **Resource Optimization**: Balances security with business continuity

## 🔧 System Components

### Core Agents

| Agent | Purpose | Key Features |
|-------|---------|--------------|
| **Monitor** | Threat Detection | Multi-source ingestion, Real-time alerts, Metadata enrichment |
| **Analyzer** | Context Analysis | AI-powered analysis, Knowledge base queries, Risk assessment |
| **Orchestrator** | Remediation | Automated actions, API integration, Compliance checks |

### Supporting Infrastructure

- **`pacer.py`** - Redis communication backbone with fallback
- **`knowledge_base.md`** - Company asset and policy information
- **`simulated_data.py`** - Realistic threat scenarios
- **`main.py`** - Pipeline orchestration and modes
- **`demo_app.py`** - Interactive Streamlit interface

## 📈 Usage Modes

### 1. Interactive Demo (Web UI)
Perfect for presentations and demonstrations:
- Real-time pipeline visualization
- Step-by-step execution tracking
- Historical analysis and trends
- System status monitoring

### 2. Single Execution
Test individual threat scenarios:
```bash
python main.py --mode single --source horizon3
```

### 3. Continuous Mode
Production-like continuous monitoring:
```bash
python main.py --mode continuous
```

### 4. Batch Demo
Process all scenarios automatically:
```bash
python main.py --mode demo
```

## 🛡️ Remediation Actions

The system can execute various automated responses:

| Action | Trigger | Description | Business Impact |
|--------|---------|-------------|-----------------|
| **isolate_host** | Critical threats | Network isolation via firewall | Immediate protection, temporary downtime |
| **patch_system** | Vulnerabilities | Automated patching | Scheduled maintenance, minimal impact |
| **reset_credentials** | Credential compromise | Password/key rotation | User inconvenience, enhanced security |
| **monitor_closely** | Suspicious activity | Enhanced logging/alerting | No impact, increased visibility |
| **emergency_shutdown** | Imminent breach | Complete system shutdown | Maximum protection, business disruption |

## 🔌 API Integrations

The system simulates integration with common security tools:

- **Firewall Management** - Host isolation and traffic blocking
- **Patch Management** - Automated vulnerability remediation  
- **Identity Management** - Credential resets and MFA enforcement
- **SIEM Platform** - Enhanced monitoring and alerting
- **Infrastructure APIs** - System control and emergency actions

## 📋 Requirements

### Required Dependencies
```
anthropic>=0.25.0
llama-index>=0.10.0
redis>=5.0.0
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### Optional Services
- **Redis Server** - For production A2A communication (falls back to in-memory)
- **OpenAI API** - For embeddings (required for knowledge base)
- **Anthropic API** - For AI analysis (falls back to rule-based)

## 🔒 Security Considerations

- **API Keys**: Stored in environment variables, never committed
- **Network Security**: Redis connections should be encrypted in production
- **Access Control**: Implement proper authentication for web interface
- **Audit Logging**: All actions are logged with timestamps and metadata
- **Fail-Safe**: System defaults to safe actions when AI is unavailable

## 🎪 Demo Tips

### For Presentations
1. Start with the Streamlit interface (`streamlit run demo_app.py`)
2. Walk through the three-agent architecture
3. Demonstrate with the critical Horizon3 scenario first
4. Show the knowledge base integration and business context
5. Highlight the automated remediation actions

### For Technical Evaluation
1. Run individual agents to show modular design
2. Test with Redis disabled to show fallback capability
3. Demonstrate the pipeline with different threat sources
4. Show the knowledge base querying functionality
5. Review the comprehensive logging and observability

## 🤝 Contributing

This is a hackathon project demonstrating AI-powered incident response. The system is designed to be:

- **Modular**: Each agent can be developed and tested independently
- **Extensible**: Easy to add new threat sources and remediation actions
- **Observable**: Comprehensive logging and monitoring capabilities
- **Realistic**: Based on actual enterprise security workflows

## 📜 License

MIT License - See LICENSE file for details.

---

**Built for the AI Agent Hackathon** 🏆  
*Demonstrating the future of autonomous cybersecurity operations*
