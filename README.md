### Weatherbot
Query rainfall data by weather API, sent Line messages if status is changed.

```mermaid
graph TD
    A[User enter station name] --> B{Is station name valid?}

    B -- Yes --> C[Fetch data from API]
    B -- No --> A

    C --> D{Fetch successful?}

    D -- Yes --> E[Reset error counter]
    E --> F[Parse API response]

    D -- No --> G[Retry and log error]
    G --> H{Retry with exponential backoff}

    H -- Yes --> F
    H -- No --> I[Log critical error]
    I --> J[Increment failure count]

    J --> K{Reached max retries?}
    K -- Yes --> L[Send LINE system alert]
    K -- No --> Z[End]

    F --> M[Load previous state]
    M --> N[Compute new state]

    N --> O{State changed?}

    O -- Yes --> P[Send LINE rain alert]
    O -- No --> Z

    P --> Q{LINE send successful?}

    Q -- Yes --> R[Persist new state]
    Q -- No --> S[Log critical error]

    R --> Z
    S --> Z
    L --> Z
    
```
This program parses weather API data and use Line message to notify user the weather state is changed significantly.


User enter station name:
    - search weather station, start parsing weather data.
    - if station didn't exist, ask user to input valid station name.
Fetch data from API:
    - 
