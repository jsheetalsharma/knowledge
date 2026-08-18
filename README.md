# Backend Interview Prep Portal

A private, generic interview-preparation study portal focused on senior/lead backend engineering.

## Included

- Easy explanations of Java, concurrency, JVM, Spring Boot
- Kafka fundamentals and failure scenarios
- Stream processing / Flink concepts
- AWS + Kubernetes
- Distributed systems and resiliency
- System design
- LLD and code review
- Testing, CI/CD and production operations
- Security and AI-assisted engineering
- Leadership and behavioral preparation
- Rapid-fire questions
- Limited-time revision plan
- Topic completion tracking

## Privacy

This project intentionally contains no personal details, employer details, interview-company details, names, URLs, or identifying information.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy

This is designed to work with Streamlit Community Cloud or any environment that can run Streamlit.

Entry point:

```text
app.py
```

## Suggested future additions

- Flashcards
- Timed mock interview
- Quiz scoring
- Spaced repetition
- Personal notes stored locally
- More system-design walkthroughs
- Java/Kafka/Flink coding exercises
