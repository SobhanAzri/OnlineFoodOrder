# Process 5 — Discover Nearby Restaurants (Distance-Based)

## Purpose
The distance-based bonus feature: a **Customer** shares their location and the
**System** ranks active restaurants by their great-circle distance (Haversine),
so the closest restaurants appear first. Handles the case where coordinates are
missing.

## Roles involved
- **Customer** — provides a location (or uses their saved profile location).
- **System** — computes distances with `core.utils.haversine_distance()`,
  filters active restaurants, and sorts the result.

## Main steps
1. Customer requests nearby restaurants (manual location or saved profile).
2. System checks that usable coordinates are available.
3. System loads only **active** restaurants that have coordinates
   (`ActiveRestaurantManager`).
4. System computes the distance from the customer to each restaurant.
5. System sorts by ascending distance and returns the list.
6. If no coordinates are available, the system falls back to an unfiltered list
   and prompts the customer to set a location.

## Diagram

```mermaid
flowchart TD
    A([👤 Customer]) --> B[Request nearby restaurants]
    B --> C{Use saved profile<br/>location or enter new?}
    C -- Enter new --> C1[Provide latitude/longitude]
    C -- Saved --> C2[Load profile coordinates]
    C1 --> D
    C2 --> D

    D{Customer coordinates<br/>available?}
    D -- No --> D1[/⚠ Can't compute distance/]
    D1 --> D2[(System: show all active<br/>restaurants unsorted)]
    D2 --> D3[Prompt customer to set a location]
    D3 --> Z([Show results])

    D -- Yes --> E[(System: load active restaurants<br/>with coordinates)]
    E --> F{Restaurants<br/>with location found?}
    F -- No --> F1[/❌ 'No nearby restaurants'/]
    F1 --> Z

    F -- Yes --> G[(System: compute haversine<br/>distance to each)]
    G --> H[(System: sort by distance ASC)]
    H --> I[/✔ Return ranked list<br/>nearest first/]
    I --> Z

    classDef actor fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef system fill:#fff3e0,stroke:#ef6c00,stroke-width:1px,stroke-dasharray: 4 2;
    classDef error fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 3;
    classDef warn fill:#fff8e1,stroke:#f9a825,stroke-dasharray: 5 3;
    classDef ok fill:#e8f5e9,stroke:#2e7d32;
    class A actor;
    class E,G,H,D2 system;
    class F,F1,D error;
    class D1,D3 warn;
    class I ok;
```

## Decision points & alternative paths
- **Customer coordinates available?** — if not, distance cannot be computed; the
  system degrades gracefully to an unfiltered active list and prompts for a
  location. `haversine_distance()` returns `None` when any coordinate is
  missing, which drives this branch.
- **Any restaurants with coordinates?** — if none, a clear “no nearby
  restaurants” message is shown.

## Notes
- Distances are computed in application code (`core.utils.haversine_distance`)
  rather than the database, keeping Phase 1 free of a PostGIS dependency while
  still supporting correct, city-scale ranking.
