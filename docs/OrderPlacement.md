# Process 1 — Place an Order

## Purpose
The core transaction of the platform: a **Customer** builds a cart from a
restaurant's available menu, checks out, and the **System** creates an `Order`
that the **Restaurant Owner** then processes through its lifecycle until it is
delivered (or canceled).

## Roles involved
- **Customer** — browses the menu, manages the cart, confirms the order.
- **Restaurant Owner** — accepts, prepares, dispatches and completes the order.
- **System** — validates availability, creates the order, calculates totals,
  notifies, and enforces the status transitions.

## Main steps
1. Customer opens an active restaurant's menu (only `is_active` restaurants and
   `is_available` food items are visible — enforced by the custom managers).
2. Customer adds items to the cart and sets quantities.
3. Customer proceeds to checkout.
4. System checks the cart is not empty and every item is still available.
5. System computes `total_price` + `delivery_cost` and creates the `Order`
   (status **Pending**).
6. Restaurant Owner sees the new order and accepts it (**Pending → Preparing**).
7. Order is dispatched (**Preparing → Sent**) and delivered
   (**Sent → Delivered**).
8. System writes a `NotificationLog` entry at key state changes.

## Diagram

```mermaid
flowchart TD
    A([👤 Customer]) --> B[Open active restaurant menu]
    B --> C{Menu has available items?}
    C -- No --> C1[/❌ Show 'No items available'/]
    C1 --> B
    C -- Yes --> D[Add food items to cart<br/>set quantities]
    D --> E[Go to checkout]
    E --> F{Cart empty?}
    F -- Yes --> F1[/❌ Show 'Your cart is empty'/]
    F1 --> D
    F -- No --> G{All items still available?}
    G -- No --> G1[/❌ Remove out-of-stock items<br/>and warn customer/]
    G1 --> D

    G -- Yes --> H[(System: compute total_price<br/>+ delivery_cost)]
    H --> I[(System: create Order<br/>status = Pending)]
    I --> J[(System: log notification<br/>'Order received')]
    J --> K([👤 Restaurant Owner])

    K --> L{Owner accepts order?}
    L -- No --> L1[Set status = Canceled]
    L1 --> L2[(System: notify customer<br/>'Order canceled')]
    L2 --> Z([Order closed])

    L -- Yes --> M[Set status = Preparing<br/>kitchen cooks food]
    M --> N[Set status = Sent<br/>dispatch to customer]
    N --> O[Set status = Delivered]
    O --> P[(System: log notification<br/>'Order delivered')]
    P --> Z

    classDef actor fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef system fill:#fff3e0,stroke:#ef6c00,stroke-width:1px,stroke-dasharray: 4 2;
    classDef error fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 3;
    class A,K actor;
    class H,I,J,P,L2 system;
    class C1,F1,G1,L1,C,F,G,L error;
```

## Decision points & alternative paths
- **Menu has available items?** — empty menu loops back.
- **Cart empty?** — blocks checkout.
- **All items still available?** — out-of-stock items are removed and the
  customer is warned (prevents ordering unavailable food).
- **Owner accepts order?** — rejection path cancels the order and notifies the
  customer.

## Notation
- `👤` rounded nodes = human **roles**.
- `[ ]` rectangles = **user activities**.
- `[( )]` dashed-orange nodes = **automatic system responses**.
- `{ }` diamonds = **decision points**.
- `/❌ .../` red dashed nodes = **error / rejection paths**.
