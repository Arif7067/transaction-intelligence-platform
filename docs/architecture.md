# Architecture & phase plan

| # | Phase | depends on | Key risk |
|---|---|---|---|
| 1 | Data ingestion & pipeline (Kafka, PySpark, Airflow) | - (foundation) | Over-engineering before there's a model to feed |
| 2 | Feature Engineering & Ml model (MLflow) | Phase 1 | Chasing accuracy over pipeline completeness |
| 3 | Model serving (FastAPI, Docker) | Phase 2 | Kubernetes rabbit hole - default to cloud Run/Fargate |
| 4 | LLM/RAG explanation layer | Phase 1, 3 | scope creep into a full agent framework |
| 5 | Monitoring & observability | Phase 1-4 | skipping it because it's invisible in a demo |
| 6 | CI/CD & infrastucture as code | Stable architecture | Automating before the manual path is proven |
| 7 | Packaging (diagram, README, demo video) | All prior phases | under-investing in the phase that gets attention |


## RAG pipeline steps (Phase 4 detail)

1. Build the knowledge corpus
2. Chunk the source data
3. Generate embeddings
4. Index in a vector database
5. Construct the query at inference time
6. Retrieve similar cases
7. Assemble the augmented prompt
8. Generate the explanation
9. Validate and format the output
10. Log and feed back

## Decision log
- YYYY-MM-DD: Chose PySpark over Ab Initio — office-licensed only, not usable in a public portfolio