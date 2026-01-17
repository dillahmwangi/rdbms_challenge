import { useEffect, useState } from "react";
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser,
  // fetchJoin,
} from "./api";

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [age, setAge] = useState("");

  // JOIN state
  // const [joinResult, setJoinResult] = useState([]);
  // const [leftTable, setLeftTable] = useState("users");
  // const [rightTable, setRightTable] = useState("orders");
  // const [leftColumn, setLeftColumn] = useState("id");
  // const [rightColumn, setRightColumn] = useState("user_id");

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    const data = await fetchUsers();
    setUsers(data);
  }

  async function handleCreate(e) {
    e.preventDefault();

    await createUser({
      name: name.trim(),
      age: Number(age),
    });

    setName("");
    setAge("");
    loadUsers();
  }

  async function handleUpdate(user) {
    const newName = prompt("Enter new name:", user.name);
    const newAge = prompt("Enter new age:", user.age);

    if (!newName || newAge === null) return;

    const parsedAge = Number(newAge);
    if (Number.isNaN(parsedAge)) return;

    await updateUser(user.id, {
      name: newName.trim(),
      age: parsedAge,
    });

    loadUsers();
  }

  // async function loadJoin() {
  //   const result = await fetchJoin({
  //     left_table: leftTable,
  //     right_table: rightTable,
  //     left_column: leftColumn,
  //     right_column: rightColumn,
  //   });

  //   setJoinResult(result);
  // }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>Pesapal RDBMS Demo</h1>
        <p style={styles.subtitle}>
          Custom-built relational database engine with CRUD, constraints, and joins
        </p>
      </header>

      {/* CREATE USER */}
      <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Create User</h2>

        <form onSubmit={handleCreate} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Name</label>
            <input
              style={styles.input}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Age</label>
            <input
              style={styles.input}
              type="number"
              min="0"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
            />
          </div>

          <button style={styles.primaryButton}>Create User</button>
        </form>
      </section>

      {/* USERS TABLE */}
      <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Users</h2>

        {users.length === 0 ? (
          <div style={styles.emptyState}>No users found.</div>
        ) : (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.thId}>ID</th>
                <th style={styles.thName}>Name</th>
                <th style={styles.thAge}>Age</th>
                <th style={styles.thActions}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u, index) => (
                <tr key={u.id} style={index % 2 === 0 ? styles.rowAlt : null}>
                  <td style={styles.tdId}>
                    {String(u.id).padStart(3, "0")}
                  </td>
                  <td style={styles.tdName}>
                    <strong>{u.name}</strong>
                  </td>
                  <td style={styles.tdAge}>{u.age}</td>
                  <td style={styles.tdActions}>
                    <div style={styles.actionGroup}>
                      <button
                        style={styles.iconButton}
                        onClick={() => handleUpdate(u)}
                      >
                        ✏️
                      </button>
                      <button
                        style={styles.iconButtonDanger}
                        onClick={() => deleteUser(u.id).then(loadUsers)}
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* DYNAMIC JOIN */}
      {/* <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Dynamic INNER JOIN</h2>

        <div style={styles.form}>
          <input
            style={styles.input}
            value={leftTable}
            onChange={(e) => setLeftTable(e.target.value)}
            placeholder="Left table"
          />
          <input
            style={styles.input}
            value={leftColumn}
            onChange={(e) => setLeftColumn(e.target.value)}
            placeholder="Left column"
          />
          <input
            style={styles.input}
            value={rightTable}
            onChange={(e) => setRightTable(e.target.value)}
            placeholder="Right table"
          />
          <input
            style={styles.input}
            value={rightColumn}
            onChange={(e) => setRightColumn(e.target.value)}
            placeholder="Right column"
          />
        </div>

        <button style={styles.primaryButton} onClick={loadJoin}>
          Execute JOIN
        </button>
      </section> */}
{/* 
      {joinResult.length > 0 && (
        <section style={styles.card}>
          <h2 style={styles.sectionTitle}>JOIN Result</h2>

          <table style={styles.table}>
            <thead>
              <tr>
                {Object.keys(joinResult[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {joinResult.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val, j) => (
                    <td key={j}>{String(val)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )} */}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: 950,
    margin: "40px auto",
    padding: "0 20px",
    fontFamily: "Inter, Arial, sans-serif",
  },
  header: { marginBottom: 40 },
  title: { fontSize: 28 },
  subtitle: { color: "#6b7280" },

  card: {
    background: "#ffffff",
    padding: 24,
    borderRadius: 12,
    marginBottom: 32,
    boxShadow: "0 6px 16px rgba(0,0,0,0.06)",
  },
  sectionTitle: { marginBottom: 16 },

  form: { display: "flex", gap: 12, flexWrap: "wrap" },
  formGroup: { display: "flex", flexDirection: "column", gap: 6 },

  input: {
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
  },

  primaryButton: {
    marginTop: 12,
    padding: "10px 18px",
    background: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
  },

  table: { width: "100%", borderCollapse: "collapse" },

  thId: { width: 80 },
  thAge: { width: 80 },
  thActions: { width: 120, textAlign: "right" },

  tdId: { textAlign: "center", fontWeight: 600 },
  tdName: { paddingLeft: 10, textAlign: "center" },
  tdAge: { textAlign: "center" },
  tdActions: { textAlign: "right" },

  actionGroup: { display: "flex", justifyContent: "flex-end", gap: 8 },

  iconButton: {
    border: "none",
    background: "#e5e7eb",
    padding: "6px 10px",
    borderRadius: 8,
    cursor: "pointer",
  },
  iconButtonDanger: {
    border: "none",
    background: "#fecaca",
    padding: "6px 10px",
    borderRadius: 8,
    cursor: "pointer",
  },

  rowAlt: { background: "#f9fafb" },
  emptyState: { padding: 20, textAlign: "center", color: "#6b7280" },
};

export default App;
