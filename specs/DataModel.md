# Data Model

## Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ INCIDENTS : "reports"
    
    USERS {
        uuid id PK
        string email UK
    }

    INCIDENTS {
        uuid id PK
        string title
        text description
        enum category "CLEANING, NOISE, MAINTENANCE, SECURITY"
        timestamp created_at
        timestamp updated_at
        uuid owner_id FK
    }
```
