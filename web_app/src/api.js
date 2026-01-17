const API_BASE = "http://127.0.0.1:5000";

export async function fetchUsers() {
  const res = await fetch(`${API_BASE}/users`);
  return res.json();
}

export async function createUser(user) {
  await fetch(`${API_BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: user.name,
      age: user.age,
    }),
  });
}


export async function updateUser(id, data) {
  await fetch(`${API_BASE}/users/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: data.name,
      age: data.age,
    }),
  });
}

export async function fetchJoin(data) {
  const res = await fetch("http://127.0.0.1:5000/join", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return res.json();
}



export async function deleteUser(id) {
  await fetch(`${API_BASE}/users/${id}`, {
    method: "DELETE",
  });
}
