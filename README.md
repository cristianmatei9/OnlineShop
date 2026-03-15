# Flask Online Store Web Application

A full-stack online store application built with **Flask** and **SQLite**. This project demonstrates a clean separation of concerns using a **Service-Repository pattern**, focusing on secure user authentication and **efficient state management for the shopping cart.**

---

### 🌟 Key Features
* **User Authentication:** Secure Sign-up and Login functionality.
* **Shopping Cart System:** Add/remove products and update quantities in real-time.
* **Persistent Storage:** Full CRUD operations managed via **SQLAlchemy**.
* **Data Integrity:** Robust server-side input validation (via `validators.py`).
* **Clean Architecture:** Separated business logic (Services) from data access (Repositories).
* **Responsive UI:** Mobile-friendly design using custom CSS.

---

### 🛠️ Tech Stack
* **Backend:** Python / Flask
* **Database:** SQLite (SQLAlchemy ORM)
* **Migrations:** Flask-Migrate
* **Frontend:** HTML5, CSS3
* **Architecture:** Layered Pattern (`Models` → `Repositories` → `Services` → `Routes`)

---

### 📂 Project Structure

* **`app.py`**: Application entry point and configuration.
* **`models.py`**: Database schemas (User, Product, Order).
* **`repository.py`**: Direct database interactions and queries.
* **`service.py`**: Core business logic and use cases.
* **`validators.py`**: Custom logic for data sanitization and validation.
* **`templates/`**: Dynamic HTML.
* **`static/`**: Assets including CSS and UI components.
