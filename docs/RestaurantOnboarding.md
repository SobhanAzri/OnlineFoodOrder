# Process 2 — Restaurant Onboarding & Menu Management

## Purpose
Describes how a **Restaurant Owner** registers their restaurant, waits for
**Admin** approval (activation), and then keeps the menu and stock up to date.
Only approved (`is_active=True`) restaurants become visible to customers.

## Roles involved
- **Restaurant Owner** — submits the restaurant and manages its menu.
- **Admin** — reviews and approves / rejects the restaurant.
- **System** — stores the restaurant, enforces the `is_active` flag, hides
  unavailable items.

## Main steps
1. Owner submits restaurant data (name, address, location).
2. System creates the `Restaurant` with `is_active = False` (awaiting review).
3. Admin reviews the application.
4. If rejected → the restaurant stays inactive and the owner is notified.
5. If approved → `is_active = True`; customers can now see it.
6. Owner adds / edits `FoodItem`s and toggles their availability
   (`is_available`), which controls whether they appear on the public menu.

## Diagram

```mermaid
flowchart TD
    A([👤 Restaurant Owner]) --> B[Submit restaurant details<br/>name, address, location]
    B --> C[(System: create Restaurant<br/>is_active = False)]
    C --> D([👤 Admin])

    D --> E{Admin approves?}
    E -- No --> E1[Keep is_active = False]
    E1 --> E2[(System: notify owner<br/>'Application rejected')]
    E2 --> Y([Owner may resubmit])
    Y --> B

    E -- Yes --> F[(System: set is_active = True)]
    F --> G[(System: notify owner<br/>'Restaurant approved')]
    G --> H([👤 Restaurant Owner])

    H --> I[Manage menu]
    I --> J{Action?}
    J -- Add dish --> K[Add FoodItem<br/>name, price, image]
    J -- Edit dish --> L[Edit FoodItem details/price]
    J -- Toggle stock --> M{Item in stock?}
    M -- Yes --> M1[Set is_available = True]
    M -- No --> M2[Set is_available = False]
    M2 --> M3[/❌ Item hidden from<br/>customer menu/]

    K --> N[(System: save menu)]
    L --> N
    M1 --> N
    M3 --> N
    N --> I

    classDef actor fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef system fill:#fff3e0,stroke:#ef6c00,stroke-width:1px,stroke-dasharray: 4 2;
    classDef error fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 3;
    class A,D,H actor;
    class C,E2,F,G,N system;
    class E,E1,M error;
```

## Decision points & alternative paths
- **Admin approves?** — rejection keeps the restaurant hidden and notifies the
  owner; they can resubmit.
- **Item in stock?** — setting `is_available = False` hides the item from the
  customer menu (relies on `AvailableFoodManager`).

## Notes
- The `is_active` flag on `Restaurant` is the single source of truth for
  visibility; `ActiveRestaurantManager` guarantees customers never see a
  non-approved restaurant.
