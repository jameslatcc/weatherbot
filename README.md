### Weatherbot
Query rainfall data by weather API, sent Line messages if status is changed.

```mermaid
graph TD
    A[Task Scheduler<br>Every 10 min] --> B{Fetch API}
    B -- Success --> O[Reset Error Counter]
    O --> C[Parse Rainfall]
    B -- Fail --> D[Retry/Log errors]
    D --> E{Retry with exponential backoff}
    E -- Success --> C
    E -- Fail --> G[Log Critical Error]
    G --> M[Count 5 times]
    M --> N[Send Line Message System Alert]
    N --> Z
    C --> F[Load Previous State]
    F --> H[Compute New State]
    H -- State Changed --> I[Send Line Message Rain Alert]
    H -- State No Change --> Z[END]
    I --> J{Line Fail?}
    J -- NO --> L[Persist New State]
    J -- YES --> K[Log Critical Error]
    L --> Z
    K --> Z
```