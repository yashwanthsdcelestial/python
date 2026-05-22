// q18-ecommerce-types.ts
// Run: npx ts-node q18-ecommerce-types.ts

// ══════════════════════════════════════════════════════════════
//  Enums
// ══════════════════════════════════════════════════════════════

enum OrderStatus {
  Pending    = 'PENDING',
  Processing = 'PROCESSING',
  Shipped    = 'SHIPPED',
  Delivered  = 'DELIVERED',
  Cancelled  = 'CANCELLED',
}

enum ProductCategory {
  Electronics = 'Electronics',
  Clothing    = 'Clothing',
  Food        = 'Food',
  Books       = 'Books',
  Other       = 'Other',
}

// ══════════════════════════════════════════════════════════════
//  Core Interfaces
// ══════════════════════════════════════════════════════════════

interface Product {
  id:       string;
  name:     string;
  price:    number;      // in USD
  category: ProductCategory;
  stock:    number;
  imageUrl?: string;
  description?: string;
}

interface CartItem {
  product:  Product;
  quantity: number;
  addedAt:  string;     // ISO date
}

interface Address {
  street:  string;
  city:    string;
  zip:     string;
  country: string;
}

interface Order {
  id:              string;
  items:           CartItem[];
  total:           number;
  status:          OrderStatus;
  shippingAddress: Address;
  createdAt:       string;
  updatedAt:       string;
}

// ══════════════════════════════════════════════════════════════
//  Utility Types (API variations)
// ══════════════════════════════════════════════════════════════

// For creating a product (no id — server assigns it)
type CreateProduct = Omit<Product, 'id'>;

// For updating a product (all fields optional except id)
type UpdateProduct = Partial<Omit<Product, 'id'>> & { id: string };

// Lightweight summary for listing pages
type ProductSummary = Pick<Product, 'id' | 'name' | 'price' | 'category'>;

// ══════════════════════════════════════════════════════════════
//  Type Guards
// ══════════════════════════════════════════════════════════════

function isProduct(value: unknown): value is Product {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    'price' in value &&
    typeof (value as Product).price === 'number'
  );
}

function isOrder(value: unknown): value is Order {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'items' in value &&
    'status' in value &&
    Array.isArray((value as Order).items)
  );
}

// ══════════════════════════════════════════════════════════════
//  ID generator utility
// ══════════════════════════════════════════════════════════════

function generateId(prefix: string = 'id'): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`;
}

// ══════════════════════════════════════════════════════════════
//  Cart Class
// ══════════════════════════════════════════════════════════════

class Cart {
  private items: Map<string, CartItem> = new Map();

  /** Add a product to the cart (or increase quantity) */
  addItem(product: Product, quantity: number = 1): void {
    if (quantity <= 0) throw new Error('Quantity must be positive');
    if (product.stock < quantity) {
      throw new Error(`Insufficient stock for "${product.name}" (available: ${product.stock})`);
    }

    const existing = this.items.get(product.id);
    if (existing) {
      const newQty = existing.quantity + quantity;
      if (newQty > product.stock) {
        throw new Error(`Cannot add ${quantity} more — only ${product.stock - existing.quantity} left`);
      }
      this.items.set(product.id, { ...existing, quantity: newQty });
    } else {
      this.items.set(product.id, {
        product,
        quantity,
        addedAt: new Date().toISOString(),
      });
    }
  }

  /** Remove a product entirely from the cart */
  removeItem(productId: string): void {
    if (!this.items.has(productId)) {
      throw new Error(`Product ${productId} not in cart`);
    }
    this.items.delete(productId);
  }

  /** Update quantity of an item */
  updateQuantity(productId: string, quantity: number): void {
    const item = this.items.get(productId);
    if (!item) throw new Error(`Product ${productId} not in cart`);
    if (quantity <= 0) { this.removeItem(productId); return; }
    if (quantity > item.product.stock) {
      throw new Error(`Only ${item.product.stock} in stock`);
    }
    this.items.set(productId, { ...item, quantity });
  }

  /** Total price (rounded to 2 decimal places) */
  getTotal(): number {
    let total = 0;
    this.items.forEach(item => { total += item.product.price * item.quantity; });
    return Math.round(total * 100) / 100;
  }

  /** Total number of individual items */
  getItemCount(): number {
    let count = 0;
    this.items.forEach(item => { count += item.quantity; });
    return count;
  }

  /** Number of distinct products */
  getProductCount(): number {
    return this.items.size;
  }

  /** Get all cart items as array */
  getItems(): CartItem[] {
    return Array.from(this.items.values());
  }

  /** Is the cart empty? */
  isEmpty(): boolean {
    return this.items.size === 0;
  }

  /** Clear all items */
  clear(): void {
    this.items.clear();
  }

  /** Checkout — validates cart and returns Order */
  checkout(shippingAddress: Address): Order {
    if (this.isEmpty()) throw new Error('Cannot checkout with an empty cart');

    // Validate all stock levels are still met
    this.items.forEach(item => {
      if (item.quantity > item.product.stock) {
        throw new Error(`"${item.product.name}" is no longer available in requested quantity`);
      }
    });

    const now   = new Date().toISOString();
    const order: Order = {
      id:              generateId('ord'),
      items:           this.getItems(),
      total:           this.getTotal(),
      status:          OrderStatus.Pending,
      shippingAddress,
      createdAt:       now,
      updatedAt:       now,
    };

    this.clear();
    return order;
  }
}

// ══════════════════════════════════════════════════════════════
//  Demo
// ══════════════════════════════════════════════════════════════

const laptop: Product = {
  id:       'p1',
  name:     'MacBook Pro',
  price:    1999.99,
  category: ProductCategory.Electronics,
  stock:    10,
};

const headphones: Product = {
  id:       'p2',
  name:     'AirPods Pro',
  price:    249.00,
  category: ProductCategory.Electronics,
  stock:    25,
};

const tshirt: Product = {
  id:       'p3',
  name:     'TypeScript T-Shirt',
  price:    29.99,
  category: ProductCategory.Clothing,
  stock:    100,
};

const cart = new Cart();
cart.addItem(laptop, 1);
cart.addItem(headphones, 2);
cart.addItem(tshirt, 3);

console.log('=== Cart ===');
console.log('Item count:   ', cart.getItemCount());    // 6
console.log('Product count:', cart.getProductCount()); // 3
console.log('Total:       $', cart.getTotal());        // 2588.96

// Update quantity
cart.updateQuantity('p3', 1);
console.log('\nAfter update (tshirt qty → 1):');
console.log('Total:       $', cart.getTotal());        // 2279.97

// Checkout
const order = cart.checkout({
  street:  '123 Main Street',
  city:    'San Francisco',
  zip:     '94105',
  country: 'US',
});

console.log('\n=== Order ===');
console.log('Order ID:  ', order.id);
console.log('Status:    ', order.status);               // PENDING
console.log('Total:    $', order.total);
console.log('Items:     ', order.items.length);
console.log('Cart empty:', cart.isEmpty());             // true

// Type guard usage
console.log('\n=== Type Guards ===');
console.log('isProduct(laptop):', isProduct(laptop));   // true
console.log('isProduct({}):', isProduct({}));           // false
console.log('isOrder(order):', isOrder(order));         // true

// Utility type usage
const newProduct: CreateProduct = {
  name:     'iPad',
  price:    799,
  category: ProductCategory.Electronics,
  stock:    50,
};

const summary: ProductSummary = {
  id:       laptop.id,
  name:     laptop.name,
  price:    laptop.price,
  category: laptop.category,
};

console.log('\n=== Utility Types ===');
console.log('CreateProduct:', JSON.stringify(newProduct));
console.log('ProductSummary:', JSON.stringify(summary));

// Error handling
try {
  cart.addItem(laptop, 9999);
} catch (e: unknown) {
  if (e instanceof Error) console.log('\nExpected error:', e.message);
}

// Stock-out scenario
const outOfStock: Product = { ...laptop, stock: 1 };
const cart2 = new Cart();
cart2.addItem(outOfStock, 1);
try {
  cart2.addItem(outOfStock, 1);
} catch (e: unknown) {
  if (e instanceof Error) console.log('Stock error:', e.message);
}

console.log('\n✓ All e-commerce type examples ran successfully');
