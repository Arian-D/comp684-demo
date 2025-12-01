# Frontend Design (React SPA)

This document describes the frontend design for the full demo website, built as a React single-page application on top of the FastAPI backend.

---

## 1. Goals

- Provide a **clear, simple UI** for demonstrating the inventory and checkout system.
- Integrate cleanly with the existing FastAPI API.
- Keep the codebase small and approachable for teaching and demos.

---

## 2. Tech Stack

Recommended stack:

- **Framework**: React + TypeScript
- **Bundler**: Vite
  - `npm create vite@latest frontend -- --template react-ts`
- **Styling**: TailwindCSS or CSS Modules (choice of implementer)
- **HTTP Client**: Fetch API or Axios
- **State Management**: React hooks + Context; no Redux needed for this size

---

## 3. Project Structure (Frontend)

Create a `frontend/` folder at the repo root:

```text
comp684-demo/
  frontend/
    src/
      api/
        client.ts
      context/
        UserContext.tsx
      pages/
        LandingPage.tsx
        ProductListPage.tsx
        ProductDetailsPage.tsx
        CartPage.tsx
        CheckoutPage.tsx
        OrderConfirmationPage.tsx
        OrderHistoryPage.tsx  # optional
      components/
        Header.tsx
        ProductCard.tsx
        CartItemRow.tsx
        OrderSummary.tsx
      App.tsx
      main.tsx
    index.html
    package.json
    ...
```

---

## 4. Routing & Pages

Use `react-router-dom` for navigation.

### 4.1 Routes

- `/` – Landing / Demo Login
- `/products` – Product catalog
- `/products/:id` – Product detail
- `/cart` – User’s cart
- `/checkout` – Checkout flow
- `/order-confirmation/:orderId` – Post-checkout confirmation
- `/orders` – Order history (optional)

### 4.2 Page Design Details

#### 4.2.1 Landing Page (`/`)

**Purpose:** Start a demo session with a “demo user.”

**UI:**

- App title and short description.
- A “Continue as Demo User” button.
- Possibly an email input to create/use a custom demo user.

**Behavior:**

- On click, call `POST /demo/login` with a hardcoded or entered email.
- Save returned `user` (at minimum `user.id`) in `UserContext`.
- Redirect to `/products`.

---

#### 4.2.2 Product List Page (`/products`)

**Purpose:** Browse all products in the catalog.

**UI:**

- Grid of `ProductCard` components.
- Each card shows:
  - Product image or placeholder.
  - Name.
  - Price.
  - Stock status (In stock / Low stock / Out of stock).
  - “Add to cart” button.
  - “View details” link or button.

**Data:**

- `GET /products/` on mount.

**Interactions:**

- “Add to cart” → `POST /users/{user_id}/cart`
- “View details” → go to `/products/:id`

---

#### 4.2.3 Product Details (`/products/:id`)

**Purpose:** Show full information for a single product.

**UI:**

- Large product image (or placeholder).
- Name, category, description.
- Price, stock.
- Quantity selector + “Add to cart” button.

**Data:**

- `GET /products/{product_id}`.

**Interactions:**

- “Add to cart” uses the same cart API as the catalog page.

---

#### 4.2.4 Cart Page (`/cart`)

**Purpose:** Manage items in the cart.

**UI:**

- Table or list of `CartItemRow` components:
  - Product name (clickable link to details).
  - Unit price.
  - Quantity (editable or +/- buttons).
  - Line total.
  - Remove button.
- Cart summary (subtotal).
- “Proceed to checkout” button.

**Data:**

- `GET /users/{user_id}/cart`.

**Interactions:**

- Remove item: `DELETE /users/{user_id}/cart/{item_id}`.
- Update quantity:
  - Either via repeated `POST /users/{user_id}/cart` with updated quantity; or
  - `PATCH /users/{user_id}/cart/{item_id}` if implemented.
- Proceed to `/checkout`.

---

#### 4.2.5 Checkout Page (`/checkout`)

**Purpose:** Confirm current cart and perform checkout.

**UI:**

- Read-only list of cart items and totals.
- “Place order” button.

**Data:**

- Option 1: Re-fetch cart via `GET /users/{user_id}/cart` to ensure it is up to date.
- Option 2: Use cached cart data in context (still okay for a demo).

**Interactions:**

- On “Place order”:
  - Call `POST /users/{user_id}/checkout`.
  - On success, navigate to `/order-confirmation/:orderId`.

---

#### 4.2.6 Order Confirmation (`/order-confirmation/:orderId`)

**Purpose:** Show the user that the order succeeded.

**UI:**

- “Order successful!” message.
- Order summary:
  - Order ID.
  - Date/time.
  - Items and quantities.
  - Total.
- Links/buttons:
  - “Back to products”
  - “View order history” (`/orders`)

**Data:**

- Either:
  - Use response from checkout.
  - Or fetch: `GET /users/{user_id}/orders/{order_id}`.

---

#### 4.2.7 Order History (`/orders`) – Optional

**Purpose:** Show past orders for the current user.

**UI:**

- List or table of orders:
  - ID.
  - Date.
  - Total.
  - Status.

**Data:**

- `GET /users/{user_id}/orders`.

**Interactions:**

- Clicking an order can navigate to `/orders/:orderId` for details (which can reuse the confirmation layout).

---

## 5. Core Components

### 5.1 Header

`<Header />` common on all logged-in pages:

- Left: App name (e.g. “Inventory Demo”).
- Right: Navigation links:
  - Products
  - Cart (with item count)
  - Orders (if implemented)
  - Possibly user email or “Demo User”

### 5.2 ProductCard

Props:

- `product` with `id`, `name`, `price_cents`, `stock`, `image_url`, etc.
- `onAddToCart(productId)` handler.

Shows:

- Image.
- Name.
- Price.
- Stock label.
- “Add to cart” button.

### 5.3 CartItemRow

Props:

- `item` with embedded `product` and `quantity`.
- Handlers for:
  - `onIncreaseQuantity()`
  - `onDecreaseQuantity()`
  - `onRemove()`

---

## 6. API Client Layer

Create a simple client in `frontend/src/api/client.ts`:

```ts
// frontend/src/api/client.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  return handleResponse<T>(res);
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return handleResponse<T>(res);
}

export async function apiDelete(path: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}${path}`, { method: "DELETE" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
}
```

### 6.1 Example Hook: Fetch Products

```ts
// frontend/src/api/useProducts.ts
import { useEffect, useState } from "react";
import { apiGet } from "./client";

export interface Product {
  id: number;
  name: string;
  sku: string;
  description: string;
  price_cents: number;
  stock: number;
  image_url?: string;
  category?: string;
}

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<Product[]>("/products/")
      .then(setProducts)
      .catch((err: unknown) => {
        if (err instanceof Error) setError(err.message);
        else setError("Unknown error");
      })
      .finally(() => setLoading(false));
  }, []);

  return { products, loading, error };
}
```

---

## 7. User Context

Use context to store the currently “logged in” demo user.

```tsx
// frontend/src/context/UserContext.tsx
import { createContext, useContext, useState, ReactNode } from "react";

interface User {
  id: number;
  email: string;
  full_name?: string;
}

interface UserContextValue {
  user: User | null;
  setUser: (user: User | null) => void;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUser must be used within a UserProvider");
  return ctx;
}
```

Wrap `<App />` with `<UserProvider>` in `main.tsx`.

---

## 8. Environment Configuration

Create `.env.local` inside `frontend/`:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Vite will expose this as `import.meta.env.VITE_API_BASE_URL`.

---

## 9. Local Frontend Development

Commands (from `frontend/`):

```bash
# 1. Create the app (one-time)
npm create vite@latest . -- --template react-ts

# 2. Install dependencies
npm install

# 3. (Optional) Install TailwindCSS
# Follow Tailwind + Vite setup instructions

# 4. Run the dev server
npm run dev
```

The frontend will typically run on `http://localhost:5173`.

Make sure the backend is running too (see [`backend-expansion.md`](./backend-expansion.md)), and that `VITE_API_BASE_URL` points to it.

---

## 10. Future Enhancements

- Add proper authentication (JWT, OAuth) instead of demo login.
- Add admin views for managing products and inventory.
- Create more polished UI components and responsive layouts.
- Add tests for key components and hooks (e.g. Jest + React Testing Library).
