// Q16. Inheritance — Shape Calculator
// Topics: extends, super, Polymorphism, instanceof

class Shape {
  constructor(name) {
    this.name = name;
  }
  area() { throw new Error("Not implemented"); }
  perimeter() { throw new Error("Not implemented"); }
}

class Circle extends Shape {
  constructor(radius) {
    if (radius <= 0) throw new Error("Radius must be positive.");
    super("Circle");
    this.radius = radius;
  }
  area() { return Math.PI * this.radius ** 2; }
  perimeter() { return 2 * Math.PI * this.radius; }
}

class Rectangle extends Shape {
  constructor(width, height) {
    if (width <= 0 || height <= 0) throw new Error("Dimensions must be positive.");
    super("Rectangle");
    this.width = width;
    this.height = height;
  }
  area() { return this.width * this.height; }
  perimeter() { return 2 * (this.width + this.height); }
}

class Triangle extends Shape {
  constructor(a, b, c) {
    if (a <= 0 || b <= 0 || c <= 0) throw new Error("Sides must be positive.");
    if (a + b <= c || a + c <= b || b + c <= a) throw new Error("Invalid triangle sides.");
    super("Triangle");
    this.a = a; this.b = b; this.c = c;
  }
  area() {
    // Heron's formula
    const s = (this.a + this.b + this.c) / 2;
    return Math.sqrt(s * (s - this.a) * (s - this.b) * (s - this.c));
  }
  perimeter() { return this.a + this.b + this.c; }
}

function printShapeReport(shapes) {
  console.log("Shape Report:");
  console.log("--------------------------");
  shapes.forEach((s) => {
    console.log(
      `${s.name.padEnd(9)} | Area: ${s.area().toFixed(2).padStart(6)} | Perimeter: ${s.perimeter().toFixed(2)}`
    );
  });
  console.log("--------------------------");
  const totalArea = shapes.reduce((sum, s) => sum + s.area(), 0);
  console.log(`Total Area: ${totalArea.toFixed(2)}`);
}

// --- Tests ---
const shapes = [new Circle(10), new Rectangle(5, 8), new Triangle(3, 4, 5)];
printShapeReport(shapes);
// Shape Report:
// --------------------------
// Circle    | Area: 314.16 | Perimeter: 62.83
// Rectangle | Area:  40.00 | Perimeter: 26.00
// Triangle  | Area:   6.00 | Perimeter: 12.00
// --------------------------
// Total Area: 360.16

console.log(shapes[0] instanceof Circle);  // true
console.log(shapes[0] instanceof Shape);   // true
