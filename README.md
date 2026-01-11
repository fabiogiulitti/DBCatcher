# DBCatcher

DBCatcher is a **lightweight and accessibility‑focused database client**, designed to manage multiple database connections through a simple and extensible architecture.

The main goal of the project is to provide a usable alternative to existing database clients, with **strong attention to accessibility** (screen readers, keyboard navigation) and to experimentation with different data engines.

Currently supported databases are:
- **PostgreSQL**
- **MongoDB**
- **Apache Hive via Apache Kyuubi** (basic support)

---

## ✨ Key Features

- Multiple database connections
- Accessible UI (screen‑reader friendly)
- Modular architecture, easy to extend with new engines
- Basic Hive SQL support through **Apache Kyuubi** (SQL gateway)
- Playground environment with dockerized DBMS for development and testing

---

## 🧩 Hive / Kyuubi Support (Basic)

DBCatcher provides **basic support for Apache Hive** by connecting through **Apache Kyuubi**.

Kyuubi acts as a SQL gateway on top of Spark / Hive, exposing a JDBC endpoint that DBCatcher can use to:

- Establish a connection
- Execute basic SQL queries
- Browse schemas and tables (where supported by the engine)

> ⚠️ The current Kyuubi/Hive integration is intentionally minimal and considered **experimental**.

---

## 📦 Requirements

- Python ≥ 3.8
- Poetry
- Docker & Docker Compose (for the playground, development only)

> No local DBMS installation is required to **try or develop** DBCatcher, thanks to the provided playground.

---

## 🚀 Installation

### From source (development)

```bash
git clone https://github.com/fabiogiulitti/DBCatcher.git
cd DBCatcher
poetry install
```

Poetry is used for dependency management and virtual environment handling.

---

## ▶️ Running the Application

```bash
poetry run python -m main.main
```

### Using a custom configuration file

DBCatcher supports a custom configuration file via the `-c` parameter:

```bash
poetry run python -m main.main -c path/to/config.yaml
```

---

## 🧪 Playground (Development Only)

For development and testing purposes, DBCatcher includes a **dockerized playground** with the supported DBMS.

The playground allows you to:

- Run PostgreSQL, MongoDB and Hive/Kyuubi without local installation
- Quickly test new features
- Reproduce issues in a controlled environment

### Start the playground from project root directory

```bash
docker compose -f playground/<dbtype>/compose.yml up -d
```

Once started, you can launch DBCatcher using the dedicated playground configuration file:

```bash
poetry run python -m main.main -c playground/config/config.yaml
```

> ⚠️ **Important**: The playground is **not included in release artifacts** and is intended **only for development**.

---

## 🔌 Example Connections

**PostgreSQL**

```text
postgresql://user:password@localhost:5432/dbname
```

**MongoDB**

```text
mongodb://user:password@localhost:27017/dbname
```

**Hive via Kyuubi**

```text
jdbc:hive2://localhost:10009/default
```

---

## 🧑‍💻 Contributing

Contributions are welcome and encouraged! 🎉

You can contribute by:

- Fixing bugs
- Improving accessibility
- Adding new database backends
- Enhancing Hive/Kyuubi support
- Writing tests and documentation

### Contribution workflow

1. Fork the repository
2. Create a feature or fix branch
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes
   ```bash
   git commit -m "Add support for ..."
   ```
4. Push the branch and open a Pull Request

### Guidelines

- Keep commits small and focused
- Follow the existing code style
- Prefer readability over premature optimization
- For major changes, open an Issue first to discuss the approach

---

## 📄 License

DBCatcher is released under the **GPL‑3.0 License**.

---

## ❤️ Acknowledgements

Thanks to everyone who uses, tests, or contributes to DBCatcher.
If you find the project useful, consider giving it a ⭐ on GitHub!

