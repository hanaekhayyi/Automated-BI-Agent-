<div align="center">

# 🧠 Automated Business Intelligence Agent

**An end-to-end Data & AI Engineering solution for automated sales analytics, data quality monitoring, and AI-assisted business reporting.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Async%20API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-EA4B71?logo=n8n&logoColor=white)](https://n8n.io/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](#-license)

</div>

---

## 📌 Overview

**Automated Business Intelligence Agent** is a production-style BI pipeline built to turn raw transactional sales data into **reliable KPIs, interactive dashboards, and automated management reports** — with Generative AI used strictly as an interpretation layer, never as a calculation engine.

The project was developed in an **enterprise-oriented internship context** to address a recurring BI challenge: how to transform large volumes of noisy transactional data into trustworthy, decision-ready insights with minimal manual intervention.

It processes **541,909 transactional records** while enforcing a strict separation of concerns between data processing, business calculation, visualization, orchestration, and AI interpretation — a design principle that runs through the entire system.

> 📎 *This is the first production milestone of a broader roadmap that will introduce a Model Context Protocol (MCP) server to expose controlled business tools to an autonomous BI agent. See [Roadmap](#-roadmap).*

---

## 📑 Table of Contents

- [Business Objectives](#-business-objectives)
- [Architecture](#%EF%B8%8F-architecture)
- [Design Principle](#-design-principle)
- [Technology Stack](#%EF%B8%8F-technology-stack)
- [Data Quality Layer](#-data-quality-layer)
- [PostgreSQL Analytics Layer](#%EF%B8%8F-postgresql-analytics-layer)
- [Business KPIs](#-business-kpis)
- [Power BI Dashboard](#-power-bi-dashboard)
- [AI-Assisted Business Analysis](#-ai-assisted-business-analysis)
- [Automated n8n Workflow](#%EF%B8%8F-automated-n8n-workflow)
- [Dockerized Environment](#-dockerized-environment)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Security](#-security)
- [Roadmap](#-roadmap)
- [Skills Demonstrated](#-skills-demonstrated)
- [Author](#-author)

---

## 🎯 Business Objectives

The solution was designed to:

- centralize and structure transactional sales data;
- automate data quality controls on ingestion;
- calculate reliable, reusable, and auditable business KPIs;
- analyze sales performance by time, country, and product;
- provide interactive management dashboards;
- automate recurring BI reporting on a schedule;
- generate concise, grounded AI business insights;
- reduce manual intervention across the entire reporting lifecycle.

---

## 🏗️ Architecture

```text
                    Transactional Sales Data
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
      Python / Pandas                    PostgreSQL
       Data Quality                     Analytics Layer
              │                               │
              ▼                    ┌──────────┴──────────┐
           FastAPI                 │                     │
              │                    ▼                     ▼
              └───────────────►   n8n                Power BI
                               Orchestration          Dashboard
                                    │
                                    ▼
                              OpenRouter / LLM
                                    │
                                    ▼
                              HTML BI Report
                                    │
                                    ▼
                                  Gmail
```

### Design Principle

| Component | Responsibility |
|---|---|
| **Python / SQL** | Calculate and validate facts (deterministic) |
| **PostgreSQL** | Single source of truth for business metrics |
| **Power BI** | Visualize facts |
| **n8n** | Orchestrate the end-to-end workflow |
| **LLM** | Interpret facts — never compute them |
| **Gmail** | Distribute insights to stakeholders |

The LLM is intentionally **not responsible for calculating KPIs**. All business metrics are computed using deterministic SQL and Python before being handed to the AI layer, which operates strictly on pre-validated numbers it cannot alter.

---

## 🛠️ Technology Stack

| Layer | Technology | Role |
|---|---|---|
| Data Processing | Python, Pandas | Data quality profiling and cleaning |
| API | FastAPI, Uvicorn | Exposes Python analytics as HTTP endpoints |
| Database | PostgreSQL 16 | Storage and analytical processing |
| Analytics | SQL (views) | KPI definitions and business logic |
| Orchestration | n8n | Workflow automation and scheduling |
| Generative AI | OpenRouter / LLM | Business insight generation (interpretation only) |
| Visualization | Power BI | Interactive BI dashboard |
| Reporting | Gmail | Automated HTML report delivery |
| Infrastructure | Docker Compose | Service orchestration and reproducibility |
| Version Control | Git / GitHub | Source code management |

---

## 🔍 Data Quality Layer

A dedicated Python/Pandas component automatically profiles the transactional dataset **before** any analytical interpretation takes place, so that data issues are surfaced rather than silently propagated into KPIs.

| Data Quality Check | Result |
|---|---:|
| Transaction lines | 541,909 |
| Source attributes | 8 |
| Non-positive quantities | 10,624 |
| Non-positive unit prices | 2,517 |
| Missing customer identifiers | 135,080 |
| Missing descriptions | 1,454 |

> Non-positive quantities or prices are **not automatically treated as errors**, since they can represent returns, cancellations, or legitimate accounting adjustments. The system flags them for context rather than discarding them silently.

This component is exposed through a FastAPI endpoint, allowing n8n to trigger the analysis and retrieve structured results on demand:

```http
GET /data-quality
```

---

## 🗄️ PostgreSQL Analytics Layer

PostgreSQL is the **central analytical layer** of the solution — the single source of truth consumed by both Power BI and the automated reporting workflow, ensuring KPI consistency across every surface.

Core analytical views:

```text
valid_sales
product_sales
kpi_summary
monthly_sales
country_sales
product_performance
```

A commercial sales rule isolates valid sales transactions from cancellations, accounting adjustments, and zero-price movements:

```sql
invoice_no ~ '^[0-9]'
AND unit_price > 0
AND quantity > 0
```

Raw records are always preserved for full traceability — cleaning happens at the view level, never by mutating source data.

---

## 📊 Business KPIs

| KPI | Result |
|---|---:|
| Total Revenue | $10,655,622.48 |
| Total Orders | 19,959 |
| Average Order Value | $533.88 |
| Unique Identified Customers | 4,338 |

The analytical layer additionally produces:

- monthly revenue evolution;
- order-volume analysis;
- average order value trends;
- sales performance by country;
- product performance by revenue;
- product performance by quantity.

> **Data limitation:** the final month is incomplete — available transactions end on December 9, 2011. This limitation is explicitly surfaced both in the dashboard and in the AI-generated analysis, to prevent misleading period-over-period conclusions.

---

## 📈 Power BI Dashboard

Power BI consumes the PostgreSQL analytical views directly, providing an interactive decision-support dashboard built on top of a single, consistent KPI definition layer.

**Included visuals:**
- Total Revenue
- Total Orders
- Average Order Value
- Unique Customers
- Monthly Revenue Evolution
- Top 10 Countries by Revenue
- Top 10 Products by Revenue

Centralizing business logic in PostgreSQL guarantees that Power BI and the automated reporting workflow always report identical figures.

---

## 🤖 AI-Assisted Business Analysis

n8n merges three trusted analytical contexts before invoking the LLM:

```text
PostgreSQL KPI Summary ──────┐
                             │
PostgreSQL Monthly Sales ────┼──► LLM Analysis
                             │
Python Data Quality ─────────┘
```

The LLM operates under explicit guardrails. It must:

- use **only** the supplied analytical data;
- preserve calculated KPI values exactly as provided;
- never invent missing information;
- avoid unsupported causal explanations;
- clearly distinguish data quality issues from business performance;
- respect and flag incomplete reporting periods.

This design treats Generative AI as an **interpretation layer**, not a source of truth — a deliberate choice to keep the system auditable and trustworthy for business stakeholders.

---

## ⚙️ Automated n8n Workflow

The workflow runs manually or on an automated schedule — every **Monday at 08:00 (Africa/Casablanca)**.

```text
Trigger
  │
  ├──► PostgreSQL → KPI Summary ──────────┐
  │                                       │
  ├──► PostgreSQL → Monthly Sales ────────┼──► Merge Context
  │                                       │         │
  └──► FastAPI → Pandas Data Quality ─────┘         ▼
                                                LLM Analysis
                                                     │
                                                     ▼
                                                HTML Report
                                                     │
                                                     ▼
                                                   Gmail
```

**Final report contents:**
- Business Summary
- Monthly Evolution
- Key Trends
- Data Quality Summary
- Analytical Caveats

---

## 🐳 Dockerized Environment

The application runs as three core Docker services:

```text
n8n              → workflow orchestration
postgres         → analytical data store
python-quality   → FastAPI + Pandas data quality service
```

Docker Compose manages networking, persistent storage, ports, environment configuration, and restart policies — making the architecture fully reproducible across machines.

---

## 📁 Project Structure

```text
automated-bi-agent/
│
├── data/                      # Transactional sales data (gitignored)
├── reports/                   # Generated data quality & BI reports (gitignored)
├── scripts/
│   ├── api.py                 # FastAPI application
│   └── data_quality.py        # Pandas data quality module
│
├── .env.example                # Environment variable template
├── .gitignore
├── Dockerfile.python
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Sensitive credentials, raw datasets, generated reports, and local configuration files are excluded from version control.

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- A free [OpenRouter](https://openrouter.ai/) API key
- Gmail OAuth credentials (for automated report delivery)

### 1. Configure environment variables

```bash
cp .env.example .env
```

```env
POSTGRES_DB=bi_database
POSTGRES_USER=bi_user
POSTGRES_PASSWORD=change_me
OPENROUTER_API_KEY=your_api_key_here
```

### 2. Add the transactional dataset

```text
data/OnlineRetail.csv
```

### 3. Start the services

```bash
docker compose up -d
```

### 4. Access the services

| Service | URL |
|---|---|
| Python API health check | http://localhost:8000/health |
| Data quality report | http://localhost:8000/data-quality |
| n8n | http://localhost:5678 |

---

## 🔐 Security

Sensitive information is strictly separated from source code via environment variables. The repository **never** includes:

- database passwords;
- OpenRouter API keys;
- Gmail OAuth credentials;
- raw transactional datasets.

---

## 🔮 Roadmap

The next development phase introduces an **MCP-enabled Business Intelligence Agent**, allowing an AI agent to query business data through a controlled tool interface rather than direct database access.

Planned MCP-exposed tools:

```text
get_kpi_summary()
get_revenue()
get_sales_by_region()
get_sales_by_product()
get_top_products()
compare_periods()
```

**Goal:** let the LLM autonomously decide which tool(s) to call based on a natural-language business question — while keeping every data access point explicit, controlled, and auditable.

Further stages under consideration: a multi-agent setup (Data Quality / KPI / Analysis / Report agents), to be introduced only if it provides measurable value over the single-agent design.

---

## 💼 Skills Demonstrated

| Domain | Skills |
|---|---|
| **Data Engineering** | Python, Pandas, PostgreSQL, SQL, Data Quality |
| **Business Intelligence** | Power BI, KPI Design, Sales Analytics |
| **AI Engineering** | LLM Integration, Prompt Guardrails, FastAPI |
| **Automation** | n8n, Scheduled Workflows, Automated Reporting |
| **DevOps** | Docker, Docker Compose, Environment Management |
| **Software Engineering** | REST API Design, Git, GitHub |

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Hanae KHAYYI**
Data & AI Engineer

*Automated Business Intelligence Agent — Data Engineering, Business Intelligence & AI Automation Project*