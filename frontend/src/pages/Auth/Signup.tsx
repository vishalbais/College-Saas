import React, { useState } from "react";
import axios from "axios";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const res = await axios.post("/api/v1/auth/signup", { email, password, role: "CollegeAdmin" });
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/";
    } catch (err: any) {
      alert("Signup failed: " + (err?.response?.data?.detail || err.message));
    }
  }
  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-xl mb-4">Signup</h2>
      <form onSubmit={submit} className="space-y-4">
        <input value={email} onChange={e => setEmail(e.target.value)} className="w-full p-2 border" placeholder="Email" />
        <input value={password} onChange={e => setPassword(e.target.value)} type="password" className="w-full p-2 border" placeholder="Password" />
        <button className="bg-green-600 text-white px-4 py-2 rounded">Sign up</button>
      </form>
    </div>
  );
}
