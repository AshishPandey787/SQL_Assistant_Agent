## This is the flowchart for the agent flow


        User (PDF Input)
                |
                v
        Agent reads PDF → Extracts Columns & Filters
                |
                v
        User Validation
        ├── Yes → SQL Generation (Knowledge Source)
        │           |
        │           v
        │       User Feedback (Query 2)
        │           |
        │           v
        │       Regenerate SQL → Repeat until satisfied
        │
        └── No → User Correction (Query 1)
                        |
                        v
                Agent Refines Extraction → Back to Validation
                

