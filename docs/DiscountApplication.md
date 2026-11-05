# Process 3 — Apply a Discount Code at Checkout

## Purpose
Lets a **Customer** redeem a restaurant's discount code. The **System**
validates the code against activity, the time window, and the restaurant, then
recalculates the order total — or rejects the attempt with a clear reason.

## Roles involved
- **Customer** — enters a discount code at checkout.
- **System** — validates using `ActiveDiscountManager.get_valid_discounts()`
  and recalculates the total.

## Main steps
1. Customer enters a code at checkout.
2. System looks up the code and checks:
   - does it exist?
   - does it belong to the order's restaurant?
   - is it active and within `valid_from`–`valid_to`?
   - is `discount_percent` between 0 and 100?
3. If valid → apply the percentage, recompute `total_price`, attach the
   `Discount` to the `Order`.
4. If invalid → keep the previous total and show the specific reason.

## Diagram

```mermaid
flowchart TD
    A([👤 Customer]) --> B[Enter discount code at checkout]
    B --> C{Code exists?}
    C -- No --> R1[/❌ 'Invalid code'/]
    C -- Yes --> D{Belongs to this<br/>restaurant?}
    D -- No --> R2[/❌ 'Code not valid<br/>for this restaurant'/]
    D -- Yes --> E{is_active AND<br/>valid_from <= now <= valid_to?}
    E -- No --> R3[/❌ 'Code expired or inactive'/]
    E -- Yes --> F{discount_percent<br/>valid 0-100?}
    F -- No --> R4[/❌ 'Malformed discount'/]

    F -- Yes --> G[(System: recompute total_price<br/>base x percent / 100)]
    G --> H[(System: link Discount to Order)]
    H --> I[/✔ Apply 'Code applied'/]
    I --> Z([Proceed to payment/checkout])

    R1 --> Z2[Keep current total]
    R2 --> Z2
    R3 --> Z2
    R4 --> Z2
    Z2 --> Z

    classDef actor fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef system fill:#fff3e0,stroke:#ef6c00,stroke-width:1px,stroke-dasharray: 4 2;
    classDef error fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 3;
    classDef ok fill:#e8f5e9,stroke:#2e7d32;
    class A actor;
    class G,H system;
    class C,D,E,F,R1,R2,R3,R4,Z2 error;
    class I ok;
```

## Decision points & alternative paths
- **Code exists?** — unknown codes are rejected immediately.
- **Belongs to this restaurant?** — a restaurant's code cannot be used
  elsewhere.
- **Active + within window?** — this mirrors
  `ActiveDiscountManager.get_valid_discounts()`, so a code that is disabled or
  expired is refused.
- **discount_percent valid?** — guards against malformed data.

Every failure branch returns the customer to checkout with the *unmodified*
total, so an invalid code never corrupts the order price.
