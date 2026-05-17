"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async () => {
    const res = await fetch("https://shl-recommender-production-b613.up.railway.app/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>SHL Recommender</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
        style={{ padding: 10, width: "300px" }}
      />

      <button onClick={handleSubmit} style={{ marginLeft: 10 }}>
        Submit
      </button>

      <pre style={{ marginTop: 20 }}>
        {result && JSON.stringify(result, null, 2)}
      </pre>
    </div>
  );
}