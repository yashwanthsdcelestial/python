// Q15. Class — Task Manager
// Topics: ES6 Classes, Private Fields, Getters, Static Methods

class TaskManager {
  #tasks = [];
  #nextId = 1;

  addTask(title, priority = "medium") {
    const task = {
      id: this.#nextId++,
      title,
      priority,
      status: "pending",
      createdAt: new Date().toISOString(),
    };
    this.#tasks.push(task);
    return task;
  }

  completeTask(id) {
    const task = this.#tasks.find((t) => t.id === id);
    if (!task) throw new Error(`Task with id ${id} not found`);
    task.status = "completed";
    return task;
  }

  removeTask(id) {
    const index = this.#tasks.findIndex((t) => t.id === id);
    if (index === -1) throw new Error(`Task with id ${id} not found`);
    this.#tasks.splice(index, 1);
  }

  getTasks(filterStatus) {
    if (!filterStatus) return [...this.#tasks];
    return this.#tasks.filter((t) => t.status === filterStatus);
  }

  get taskCount() {
    return this.#tasks.length;
  }

  // Static factory: creates a TaskManager and populates it from a JSON string
  static fromJSON(json) {
    const tm = new TaskManager();
    const data = JSON.parse(json);
    data.forEach(({ title, priority }) => tm.addTask(title, priority));
    return tm;
  }
}

// --- Tests ---
const tm = TaskManager.fromJSON('[{"title":"Setup env","priority":"high"}]');
tm.addTask("Write tests", "medium");
tm.addTask("Deploy app", "low");
tm.completeTask(1);

console.log(tm.taskCount);              // 3
console.log(tm.getTasks("pending"));    // [task 2, task 3]
console.log(tm.getTasks());             // all 3 tasks

try {
  tm.removeTask(999);
} catch (e) {
  console.error("Error:", e.message);  // Error: Task with id 999 not found
}
