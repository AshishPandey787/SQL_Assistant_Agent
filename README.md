flowchart TD
    A[User provides PDF input] --> B[Agent reads PDF and extracts columns & filters]
    B --> C[Agent shares extracted details with user]
    C --> D{Are columns & filters correct?}
    D -- Yes --> E[Generate SQL code using knowledge source]
    D -- No --> F[User provides corrections (Query 1)]
    F --> B

    E --> G[Share SQL code with user]
    G --> H[User feedback (Query 2)]
    H --> I[Regenerate SQL using knowledge source]
    I --> G