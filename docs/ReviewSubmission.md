# Process 4 — Submit a Review After Delivery

## Purpose
A **Customer** rates (1–5) and optionally comments on a food item once their
order has actually been delivered. The **System** enforces that only delivered
orders are eligible and that each customer reviews a given food item only once.

## Roles involved
- **Customer** — selects a food item from a delivered order, gives a rating and
  comment.
- **System** — verifies eligibility, validates the rating range, enforces the
  uniqueness constraint, and stores the `Review`.

## Main steps
1. Customer opens a delivered order and picks a food item to review.
2. System confirms the item belongs to a **Delivered** order of this customer.
3. Customer supplies a rating (1–5) and optional comment.
4. System validates the rating is within 1–5.
5. System checks the customer has not already reviewed this item.
6. System saves the `Review`.

## Diagram

```mermaid
flowchart TD
    A([👤 Customer]) --> B[Open a delivered order]
    B --> C{Order status<br/>= Delivered?}
    C -- No --> R1[/❌ 'You can review<br/>only after delivery'/]

    C -- Yes --> D[Select a food item from the order]
    D --> E[Enter rating 1-5<br/>and optional comment]
    E --> F{Rating between<br/>1 and 5?}
    F -- No --> R2[/❌ 'Rating must be 1-5'/]
    R2 --> E

    F -- Yes --> G{Already reviewed<br/>this item?}
    G -- Yes --> R3[/❌ 'You already reviewed<br/>this item'/]

    G -- No --> H[(System: create Review<br/>unique per customer+item)]
    H --> I[(System: store rating & comment)]
    I --> J[/✔ 'Review submitted'/]
    J --> Z([End])

    R1 --> Z
    R3 --> Z

    classDef actor fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef system fill:#fff3e0,stroke:#ef6c00,stroke-width:1px,stroke-dasharray: 4 2;
    classDef error fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 3;
    classDef ok fill:#e8f5e9,stroke:#2e7d32;
    class A actor;
    class H,I system;
    class C,F,G,R1,R2,R3 error;
    class J ok;
```

## Decision points & alternative paths
- **Order status = Delivered?** — reviews are only allowed on completed orders
  (prevents rating food the customer never received).
- **Rating 1–5?** — validated by `MinValueValidator` / `MaxValueValidator`;
  invalid input loops back for correction.
- **Already reviewed this item?** — `unique_review_per_customer_food_item`
  constraint blocks duplicates.

## Notes
- The uniqueness rule is enforced both in the app flow and at the database level
  via `Meta.constraints`, so the guarantee holds even under concurrent requests.
