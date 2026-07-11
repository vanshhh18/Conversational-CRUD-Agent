# OpsCopilot

**LLM-Powered Business Operations Agent with Human-in-the-Loop Approval**

OpsCopilot is a conversational AI agent that lets business operators manage day-to-day operations — memberships, bookings, users, revenue — through natural language, while keeping every write operation gated behind explicit human approval.

Built on a LangGraph ReAct agent backed by LLaMA 3.3-70B (via Groq), the system separates **read operations** (safe, instant) from **write operations** (require approval before execution), ensuring an LLM never directly mutates production data without a human confirming the action.

---

## Features

- **Natural language interface** — ask questions or issue commands in plain English; no need to know the underlying schema or write queries.
- **Read tools** — instantly pull dashboard summaries, today's revenue, active users, trial users, expiring memberships, and tomorrow's bookings.
- **Write tools with approval gating** — extend memberships/trials, update phone numbers, and cancel bookings are staged as *pending actions* and only applied after explicit approval.
- **Approve / Reject workflow** — every write action generates a pending request with an ID; nothing is committed to the database until approved.
- **Input validation** — rejects invalid requests (negative durations, malformed identifiers, nonexistent users) before they reach the database layer.
- **Streamlit chat UI** — simple front-end for interacting with the agent in real time.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | LLaMA 3.3-70B via Groq |
| Agent framework | LangGraph (ReAct agent), LangChain |
| Backend API | FastAPI |
| ORM / DB | SQLAlchemy + SQLite |
| Validation | Pydantic |
| Frontend | Streamlit |
| Memory / checkpointing | LangGraph checkpointer |

---

## Architecture

```
User (Streamlit UI)
      │
      ▼
FastAPI Backend
      │
      ▼
LangGraph ReAct Agent (LLaMA 3.3-70B)
      │
      ├── Read Tools ─────────────► Direct DB query, response returned immediately
      │
      └── Write Tools ────────────► Creates a "pending action"
                                          │
                                          ▼
                                   approve_action / reject_action
                                          │
                                          ▼
                                   Executed on DB only if approved
```

---

## Tools

**Read Tools**
- `get_dashboard_summary`
- `get_today_revenue`
- `list_trial_users`
- `get_active_users`
- `get_expiring_memberships`
- `get_tomorrow_bookings`

**Write Request Tools** *(require approval)*
- `extend_membership`
- `extend_trial`
- `update_phone`
- `cancel_booking`

**Approval Tools**
- `approve_action`
- `reject_action`

---

## Project Structure

```
.
├── agent.py          # Agent initialization (LangGraph + Groq LLM)
├── tools.py           # Tool definitions (read/write/approval)
├── prompt.py          # System prompt for the agent
├── memory.py           # LangGraph checkpointer/memory setup
├── config.py            # API keys and configuration
├── test_agent_metrics.py  # Evaluation script (accuracy, latency, edge-case handling)
└── README.md
```

---

## Evaluation

The agent was tested against a suite of natural language queries covering all 12 tools, plus a set of adversarial edge cases (invalid IDs, negative values, approval-bypass attempts, malformed input).

| Metric | Result |
|---|---|
| Intent-to-tool accuracy | 100% (12/12 test queries) |
| Average response latency | ~1.5s |
| Edge-case safe-handling rate | 80% (4/5) |

> A phone-number format validation gap was identified during edge-case testing and is being addressed — see [Known Issues](#known-issues).

---

## Known Issues

- `update_phone` does not currently reject malformed phone number formats (e.g. non-numeric input) before creating a pending action. Fix in progress: add Pydantic-level format validation on the phone number field.

---

## Getting Started

```bash
# Clone the repo
git clone <your-repo-url>
cd opscopilot

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key to config.py or .env

# Run the Streamlit app
streamlit run app.py
```

---

## Future Improvements

- Expand tool coverage (e.g. payment reconciliation, coach scheduling)
- Add role-based access control for approvals
- Persist pending actions and audit logs to a dedicated table
- Add automated regression testing via `test_agent_metrics.py` in CI
