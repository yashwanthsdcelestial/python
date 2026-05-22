import React from "react";

const students = [
  { rollNo: 1, name: "Alice", marks: 88 },
  { rollNo: 2, name: "Bob", marks: 72 },
  { rollNo: 3, name: "Carol", marks: 30 },
  { rollNo: 4, name: "David", marks: 55 },
  { rollNo: 5, name: "Eva", marks: 95 },
  { rollNo: 6, name: "Frank", marks: 28 },
  { rollNo: 7, name: "Grace", marks: 60 },
];

function getRowStyle(marks) {
  if (marks > 75) return { background: "#dcfce7", color: "#166534", fontWeight: 600 };
  if (marks < 35) return { background: "#fee2e2", color: "#991b1b", fontWeight: 600 };
  return { background: "#f8fafc", color: "#334155" };
}

function Q8StudentList() {
  return (
    <div>
      <h2>Q8 — Student List Renderer</h2>
      <table style={{ borderCollapse: "collapse", minWidth: "360px" }}>
        <thead>
          <tr style={{ background: "#e2e8f0" }}>
            <th style={{ padding: "10px 16px", textAlign: "left" }}>Roll No</th>
            <th style={{ padding: "10px 16px", textAlign: "left" }}>Name</th>
            <th style={{ padding: "10px 16px", textAlign: "left" }}>Marks</th>
          </tr>
        </thead>
        <tbody>
          {students.map(s => (
            <tr key={s.rollNo} style={getRowStyle(s.marks)}>
              <td style={{ padding: "8px 16px", border: "1px solid #e2e8f0" }}>{s.rollNo}</td>
              <td style={{ padding: "8px 16px", border: "1px solid #e2e8f0" }}>{s.name}</td>
              <td style={{ padding: "8px 16px", border: "1px solid #e2e8f0" }}>{s.marks}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p style={{ fontSize: "0.8rem", color: "#666", marginTop: "8px" }}>
        🟢 Above 75 &nbsp;|&nbsp; 🔴 Below 35
      </p>
    </div>
  );
}

export default Q8StudentList;
