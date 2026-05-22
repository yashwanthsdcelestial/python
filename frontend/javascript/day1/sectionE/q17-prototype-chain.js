// Q17. Prototype Chain Explorer
// Topics: Constructor Functions, prototype, Object.create, instanceof

// ── Base: Vehicle ──
function Vehicle(make, model, year) {
  this.make = make;
  this.model = model;
  this.year = year;
}

Vehicle.prototype.drive = function () {
  console.log(`${this.make} ${this.model} (${this.year}) is driving`);
};

// ── Derived: Car ──
function Car(make, model, year) {
  // Borrow Vehicle's constructor to set own properties
  Vehicle.call(this, make, model, year);
}

// Set up prototype chain: Car.prototype → Vehicle.prototype → Object.prototype
Car.prototype = Object.create(Vehicle.prototype);

// Restore constructor reference (Object.create breaks it)
Car.prototype.constructor = Car;

// Car-specific method
Car.prototype.honk = function () {
  console.log(`${this.make} ${this.model} (${this.year}) honks: Beep beep!`);
};

// --- Tests ---
const car = new Car("Toyota", "Camry", 2024);

car.drive(); // Toyota Camry (2024) is driving
car.honk();  // Toyota Camry (2024) honks: Beep beep!

console.log(car instanceof Car);     // true
console.log(car instanceof Vehicle); // true

// Verify prototype chain: car → Car.prototype → Vehicle.prototype
console.log(Object.getPrototypeOf(Object.getPrototypeOf(car)) === Vehicle.prototype); // true

// Constructor is correctly restored
console.log(car.constructor === Car); // true
