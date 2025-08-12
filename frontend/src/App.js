import React, { useState } from "react";

const URL = "http://localhost:8000/readPDF";

export default function App() {
  const [file, setFile] = useState(null);
  const [res, setRes] = useState(null);
  const [err, setErr] = useState("");

  async function handleUpload(uploadEvent) {
    uploadEvent.preventDefault();
    setErr("");
    setRes(null);

    if (!file) {
      setErr("Please, Upload a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      setRes(data);
    } catch (error) {
      setErr(error.message || "something went wrong");
    }
  }

  return (
    <div>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>

      {err && <p style={{ color: "red" }}>Error: {err}</p>}

      {res && (
        <div>
          <h2>{res.fileName}</h2>
          <pre>{res.pageCount}</pre>

          {res.pages &&
            res.pages.map((p) => (
              <div key={p.pageNumber}>
                <h3>Page {p.pageNumber + 1}</h3>

                {/* Original */}
                <h4>Original Text</h4>
                <pre style={{ whiteSpace: "pre-wrap" }}>{p.text}</pre>

                {/* Cleaned */}
                <h4>Clean Lines</h4>
                <pre style={{ whiteSpace: "pre-wrap" }}>
                  {(p.cleanLines || []).join("\n")}
                </pre>

                {/* Removed */}
                <h4 style={{ color: "red" }}>Removed Lines</h4>
                <pre style={{ whiteSpace: "pre-wrap", color: "red" }}>
                  {(p.removedLines || []).join("\n")}
                </pre>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
