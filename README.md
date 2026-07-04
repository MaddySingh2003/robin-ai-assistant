# 🤖 ROBIN – AI Desktop Assistant

> A next-generation, local-first AI assistant capable of voice interaction, memory, tool execution, project generation, and autonomous task planning.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

# Overview

ROBIN is a modular AI desktop assistant built with Python that combines speech recognition, large language models, memory management, tool execution, and agent-based workflows into a single system.

Unlike traditional chatbots, ROBIN is designed to perform real tasks through specialized agents, remember conversations, generate projects, execute commands, and interact naturally using voice.

The project emphasizes clean architecture, modularity, and extensibility, making it suitable for experimenting with modern AI assistant concepts.

---

# Features

## Voice Interaction

* Wake word detection
* Speech-to-text using Whisper
* Natural text-to-speech using Piper
* English and Hinglish support
* Automatic language detection

---

## AI Conversation

* Local LLM integration using Ollama
* Streaming AI responses
* Context-aware conversations
* Dynamic prompt generation

---

## Memory System

* Long-term memory
* Conversation memory
* ChromaDB vector memory
* Automatic fact storage
* Memory recall

---

## Agent-Based Architecture

* Coding Agent
* Command Agent
* Project Agent
* Memory Agent

Future agents include:

* Browser Agent
* Research Agent
* GitHub Agent
* System Agent

---

## Tool Execution

ROBIN can perform tasks such as:

* Create folders
* Generate project structures
* Create files
* Execute commands
* Generate code snippets
* Automate repetitive workflows

---

## Project Generator

Generate complete software project templates including:

* Python
* FastAPI
* Flask
* React
* Node.js
* AI Projects
* Machine Learning Projects

---

## Intelligent Routing

ROBIN automatically classifies user requests and routes them to the appropriate module.

Examples include:

* Conversation
* Coding
* Memory
* Project generation
* System commands

---

# Project Structure

```text
ROBIN/
│
├── agents/
│   ├── coding_agent.py
│   ├── command_agent.py
│   ├── memory_agent.py
│   └── project_agent.py
│
├── assistant/
│   ├── planner.py
│   ├── executor.py
│   ├── intent_classifier.py
│   └── entities.py
│
├── core/
│   ├── brain.py
│   ├── listener.py
│   ├── speaker.py
│   ├── wake_word.py
│   ├── memory.py
│   ├── memory_manager.py
│   └── chroma_memory.py
│
├── tools/
│   ├── browser_tools.py
│   ├── file_tools.py
│   ├── command.py
│   ├── project_generator.py
│   └── registry.py
│
├── piper/
│
├── main.py
├── config.py
└── memory.json
```

---

# Technology Stack

### Programming Language

* Python 3.11+

### AI

* Ollama
* Whisper
* ChromaDB
* Sentence Transformers

### Voice

* Piper
* SoundDevice
* PyAudio
* SpeechRecognition

### Machine Learning

* PyTorch
* NumPy
* SciPy

### Utilities

* Pygame
* Rich
* FastAPI
* Requests

---

# Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/ROBIN.git
```

Move into the project.

```bash
cd ROBIN
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the assistant.

```bash
python main.py
```

---

# Example Commands

```text
Hello Robin

Create a Python project

Create a FastAPI API

Write a Python function

Remember my favorite language is Python

What is my favorite language?

Create a React project

Generate code for binary search

Explain recursion in Hinglish
```

---

# Architecture

```text
User Voice
      │
      ▼
Wake Word Detection
      │
      ▼
Speech Recognition
      │
      ▼
Intent Classification
      │
      ▼
Planner
      │
      ▼
Executor
      │
      ▼
Agents
      │
      ▼
Tools / Memory / LLM
      │
      ▼
Response Generation
      │
      ▼
Text-to-Speech
```

---

# Roadmap

* Multi-agent orchestration
* Browser automation
* GitHub integration
* Web search agent
* Vision model support
* Local document RAG
* PDF understanding
* Autonomous task planning
* Desktop GUI
* Plugin system
* Multi-model routing
* Workflow automation
* Calendar integration
* Email integration
* Cross-platform support

---

# Why ROBIN?

ROBIN demonstrates practical AI engineering concepts beyond simple chatbot development.

Key engineering highlights include:

* Modular architecture
* Local AI execution
* Voice interaction
* Memory management
* Agent-based design
* Extensible tool framework
* Project automation
* Retrieval-ready architecture

---

# Future Vision

The long-term goal of ROBIN is to evolve into a fully autonomous desktop AI assistant capable of planning, reasoning, executing complex workflows, interacting with external tools, and assisting developers with end-to-end software engineering tasks.

---

# Contributing

Contributions, feature requests, and bug reports are welcome.

Feel free to fork the repository and submit pull requests.

---

# License

This project is licensed under the MIT License.

---

# Author

**Milan Suryavanshi**

Artificial Intelligence & Data Science Student
AI • Machine Learning • Python • Full Stack Development

If you found this project useful, consider giving it a ⭐ on GitHub.
