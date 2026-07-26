# TRIBUNAL — Detailed Installation & Deployment Guide

This guide provides end-to-end instructions for deploying **TRIBUNAL** from scratch.

> *"I downloaded the ZIP. Now what?"* — Follow this guide for step-by-step setup.

---

## 1. System Requirements

Before installing TRIBUNAL, ensure your system meets the following specifications:

| Requirement | Minimum | Recommended |
| :--- | :--- | :--- |
| **OS** | Windows 10/11, macOS 12+, Linux | Windows 11 / macOS 14 / Ubuntu 22.04 |
| **Python** | 3.10 | 3.11 or 3.12 |
| **Node.js** | 18.x | 20.x or 22.x LTS |
| **RAM** | 8 GB | 16 GB+ |
| **Storage** | 2 GB free space | 10 GB (if running local Ollama LLM) |

---

## 2. Local LLM Setup (Optional: Ollama & Qwen)

TRIBUNAL includes a built-in mock LLM caller for instant out-of-the-box operation. However, to evaluate full generative query planning with local LLMs:

### Step 2.1: Install Ollama
- **Windows / macOS**: Download and run the installer from [ollama.com](https://ollama.com/).
- **Linux**: Run:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### Step 2.2: Pull Qwen 2.5 Coder Model
Launch a terminal window and run:

```bash
ollama pull qwen2.5-coder:7b
```

Verify Ollama service is active at `http://localhost:11434`.

---

## 3. Backend Setup (FastAPI & Engine)

### Step 3.1: Create Virtual Environment

Navigate to the project root directory:

```bash
cd TRIBUNAL_RELEASE
```

Create a dedicated Python virtual environment:

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3.2: Install Python Dependencies

Install the pinned dependencies from `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3.3: Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Default configuration contents:
```ini
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO
STORAGE_BASE_DIR=./storage
LLM_PROVIDER=mock
OLLAMA_ENDPOINT=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5-coder:7b
```

*Note: Change `LLM_PROVIDER=ollama` if you have pulled the Qwen model in Step 2.*

---

## 4. Frontend Setup (React/Vite Dashboard)

Navigate to the dashboard directory and install packages:

```bash
cd dashboard
npm install
cd ..
```

---

## 5. Running the Application

### Step 5.1: Launch Backend API Server

In Terminal 1:

```bash
# Ensure virtualenv is activated
uvicorn api.app:app --reload --port 8000
```

- **API Base URL**: `http://localhost:8000`
- **Interactive OpenAPI / Swagger Docs**: `http://localhost:8000/docs`

### Step 5.2: Launch Frontend Dashboard

In Terminal 2:

```bash
cd dashboard
npm run dev
```

- **Dashboard Access URL**: `http://localhost:5173`

---

## 6. System Verification

Verify system integrity by executing the automated test suite and dashboard build check:

### Verify Backend Test Suite (142 Tests)
```bash
pytest tribunal/tests/unit tribunal/tests/integration
```
*Expected Output*: `142 passed in xx.xxs`

### Verify Frontend Bundle Build
```bash
cd dashboard
npm run build
```
*Expected Output*: `built in 1.xxs`

---

## 7. Troubleshooting & FAQ

### Issue 1: `npm : File cannot be loaded because running scripts is disabled`
- **Cause**: PowerShell execution policy restricted script execution.
- **Solution**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or run command via `cmd /c "npm run dev"`.

### Issue 2: `Failed to connect to Ollama at http://localhost:11434`
- **Cause**: Ollama background service is not running.
- **Solution**: Set `LLM_PROVIDER=mock` in `.env` or start Ollama by opening the Ollama application / running `ollama serve`.

### Issue 3: Port 8000 or 5173 is already in use
- **Solution**: Kill the occupying process or specify custom ports:
  ```bash
  uvicorn api.app:app --port 8080
  ```
