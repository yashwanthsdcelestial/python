import React, { useState } from "react";
import Q1ProfileCards from "./components/Q1/Q1ProfileCards";
import Q2Buttons from "./components/Q2/Q2Buttons";
import Q3ProductGrid from "./components/Q3/Q3ProductGrid";
import Q4Counter from "./components/Q4/Q4Counter";
import Q5ToggleTheme from "./components/Q5/Q5ToggleTheme";
import Q6LoginLogout from "./components/Q6/Q6LoginLogout";
import Q7TodoList from "./components/Q7/Q7TodoList";
import Q8StudentList from "./components/Q8/Q8StudentList";
import Q9Clock from "./components/Q9/Q9Clock";
import Q10UsersFetcher from "./components/Q10/Q10UsersFetcher";
import Q11TitleTracker from "./components/Q11/Q11TitleTracker";
import Q12FilteredProducts from "./components/Q12/Q12FilteredProducts";
import Q13PrimeCalc from "./components/Q13/Q13PrimeCalc";
import Q14TodoCallback from "./components/Q14/Q14TodoCallback";
import Q15CounterCallback from "./components/Q15/Q15CounterCallback";
import "./App.css";

const QUESTIONS = [
  { id: 1, label: "Q1 — Profile Cards", component: <Q1ProfileCards /> },
  { id: 2, label: "Q2 — Reusable Button", component: <Q2Buttons /> },
  { id: 3, label: "Q3 — Product Grid", component: <Q3ProductGrid /> },
  { id: 4, label: "Q4 — Counter", component: <Q4Counter /> },
  { id: 5, label: "Q5 — Toggle Theme", component: <Q5ToggleTheme /> },
  { id: 6, label: "Q6 — Login/Logout", component: <Q6LoginLogout /> },
  { id: 7, label: "Q7 — To-Do List", component: <Q7TodoList /> },
  { id: 8, label: "Q8 — Student List", component: <Q8StudentList /> },
  { id: 9, label: "Q9 — Live Clock", component: <Q9Clock /> },
  { id: 10, label: "Q10 — Users Fetcher", component: <Q10UsersFetcher /> },
  { id: 11, label: "Q11 — Title Tracker", component: <Q11TitleTracker /> },
  { id: 12, label: "Q12 — useMemo Filter", component: <Q12FilteredProducts /> },
  { id: 13, label: "Q13 — Prime useMemo", component: <Q13PrimeCalc /> },
  { id: 14, label: "Q14 — useCallback Todo", component: <Q14TodoCallback /> },
  { id: 15, label: "Q15 — useCallback Counter", component: <Q15CounterCallback /> },
];

function App() {
  const [active, setActive] = useState(1);
  const current = QUESTIONS.find(q => q.id === active);

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <span className="sidebar-title">⚛ React Day 1</span>
          <span className="sidebar-subtitle">15 Assignments</span>
        </div>
        <nav>
          {QUESTIONS.map(q => (
            <button
              key={q.id}
              className={`nav-item ${active === q.id ? "active" : ""}`}
              onClick={() => setActive(q.id)}
            >
              <span className="nav-num">{String(q.id).padStart(2, "0")}</span>
              <span className="nav-label">{q.label.split("—")[1]?.trim()}</span>
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="question-card">
          {current.component}
        </div>
      </main>
    </div>
  );
}

export default App;
