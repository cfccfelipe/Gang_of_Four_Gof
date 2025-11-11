# 🏗️ Gang of Four (GoF) Design Patterns in Python

This repository is a **structured, case-study-driven collection** of implementations for the 23 essential Gang of Four (GoF) software Design Patterns, presented with clear Python examples. Its purpose is to serve as a **quick reference guide** and a **practical manual** for applying time-tested solutions to recurring architectural problems.

## 🎯 Why Design Patterns?

Design patterns are **battle-tested blueprints** for building resilient software. By adopting them, you're not reinventing solutions; you're leveraging shared industry knowledge, which ensures:

* **Maintainability & Readability:** They provide a **shared vocabulary** (`insight:: Design patterns provide a shared language`), making the code immediately recognizable and easier to comprehend.
* **Scalability:** They eliminate logic duplication and fragility caused by excessive conditional statements (`results:: Reduced duplication and complexity`).
* **Consistency:** They standardize recurring solutions, significantly accelerating developer **onboarding** (`lessons:: Patterns accelerate onboarding`).

> **Core Insight:** Are you solving this problem in a way others can recognize and reuse?

---

## 🛠️ Repository Structure & Pattern Toolkit

The repository is organized based on the **type of problem** each pattern solves, highlighting its practical **Case of Use** over theoretical definitions.

### I. Creational Patterns (Object Instantiation)

These patterns manage object creation, providing flexibility and control over the process without coupling the code to specific classes.

| Pattern | Purpose (The "What") | Architectural Use (The "When") |
| :--- | :--- | :--- |
| **[[Factory Pattern]]** | Centralizes complex object creation, letting subclasses decide instantiation. | **Very Frequent:** When object instantiation is complex, repeated, or requires runtime logic (e.g., creating different types of `Transaction` objects). |
| **[[Singleton Pattern]]** | Restricts a class to a single instance. | **Very Frequent:** For shared resources that must be unique globally (e.g., Logger, Configuration Manager). |
| **[[Builder Pattern]]** | Separates the construction of a complex object from its representation. | **Frequent:** When creating complex objects with many optional parameters (e.g., generating multi-format reports step-by-step). |
| **[[Prototype Pattern]]** | Creates new objects by cloning an existing instance. | **Specialized:** When object creation is costly, and cloning is more efficient (e.g., spawning enemies in a game engine). |

---

### II. Structural Patterns (Class and Object Composition)

These patterns deal with how classes and objects are composed to form larger, more flexible structures.

| Pattern | Purpose (The "What") | Architectural Use (The "When") |
| :--- | :--- | :--- |
| **[[Adapter Pattern]]** | Converts the interface of one class into another interface clients expect. | **Very Frequent:** Integrating legacy systems or third-party APIs with mismatched interfaces. |
| **[[Decorator Pattern]]** | Attaches additional responsibilities to an object dynamically. | **Very Frequent:** Adding features like logging, encryption, or retry logic without modifying core components (e.g., **Notifier**). |
| **[[Composite Pattern]]** | Treats individual objects and collections of objects uniformly. | **Very Frequent:** Modeling hierarchical structures like UI component trees or file systems. |
| **[[Proxy Pattern]]** | Provides a substitute or placeholder for another object to control access. | **Frequent:** Implementing lazy loading, access control, or caching for expensive objects (e.g., large document viewers). |
| **[[Facade Pattern]]** | Provides a unified, simplified interface to a complex subsystem. | **Frequent:** Exposing a simple API to orchestrate multiple internal components (e.g., **Media Converter**). |
| **[[Bridge Pattern]]** | Decouples an abstraction from its implementation so both can vary independently. | **Moderate:** When managing two orthogonal hierarchies, like Shapes and Platform Renderers. |
| **[[Flyweight Pattern]]** | Shares common state across many objects to minimize memory usage. | **Specialized:** Optimizing memory in systems with thousands of similar objects (e.g., Text Editor character rendering). |

---

### III. Behavioral Patterns (Object Interaction and Responsibility)

These patterns focus on effective communication, flow control, and assignment of responsibilities among objects.

| Pattern | Purpose (The "What") | Architectural Use (The "When") |
| :--- | :--- | :--- |
| **[[Strategy Pattern]]** | Encapsulates interchangeable algorithms within a context. | **Very Frequent:** Replacing conditional-heavy logic (`if/elif`) with dynamically switchable behaviors (e.g., multiple pricing strategies). |
| **[[Observer Pattern]]** | Defines a one-to-many dependency, enabling event-driven communication. | **Very Frequent:** When multiple components must react automatically to state changes (e.g., stock price updates). |
| **[[Command Pattern]]** | Encapsulates a request as an object. | **Frequent:** Implementing robust **Undo/Redo** functionality or queuing actions (e.g., Text Editor history). |
| **[[Template Method Pattern]]** | Defines the skeleton of an algorithm, deferring specific steps to subclasses. | **Frequent:** When workflows share structure but differ in specific steps (e.g., data processing pipelines). |
| **[[Iterator Pattern]]** | Provides sequential access to collection elements without exposing internal structure. | **Frequent:** Traversing custom or complex data structures (e.g., trees or custom lists). |
| **[[Visitor Pattern]]** | Separates algorithms (operations) from the objects on which they operate. | **Frequent:** When adding new operations without modifying the structure of existing element classes (e.g., rendering, exporting, and spell-checking elements). |
| **[[State Pattern]]** | Allows an object to alter its behavior when its internal state changes. | **Moderate:** When an object’s behavior must change dynamically based on status (e.g., Media Player). |
| **[[Chain of Responsibility Pattern]]** | Passes requests along a chain of handlers until one handles it. | **Moderate:** For flexible and decoupled request routing (e.g., Support Ticket triage). |
| **[[Mediator Pattern]]** | Centralizes communication between many interacting objects. | **Moderate:** When reducing complex, crisscrossed dependencies between components (e.g., Chat applications). |
| **[[Memento Pattern]]** | Captures and restores an object's internal state without violating encapsulation. | **Moderate:** Implementing rollback or history features (e.g., form state undo). |

---

## 🚀 Best Practices & Contributions

The value of this repository lies in its practical application and commitment to structured thinking.

### Principles for Application

* **Apply to Recurring Problems:** Use patterns as tools, not rigid rules. Avoid **over-engineering** by forcing patterns where a simple solution suffices (`pitfall:: Over-engineering`).
* **Safety First:** Use **refactoring** as the primary method to safely introduce patterns into existing code (`lessons:: Refactoring is often the gateway`).
* **Documentation is Key:** Ensure the applied pattern is documented for clarity in code reviews and **onboarding bundles** (`step_result:: Shared understanding and faster onboarding`).

### How to Contribute

We welcome contributions! Please adhere to the following guidelines:

1.  **Fork** the repository.
2.  Implement a new pattern or alternative approach within its corresponding section.
3.  Ensure the code is clean, utilizes modern Python features (like type hinting), and includes a clear **case of use** in the comments.
4.  Submit a Pull Request detailing the problem the example solves and the pattern's specific role.
