import React from 'react';
import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import Q1 from './pages/Q1';
import Q2 from './pages/Q2';
import Q3 from './pages/Q3';
import Q4 from './pages/Q4';
import Q5 from './pages/Q5';
import Q6 from './pages/Q6';
import Q7 from './pages/Q7';
import Q8 from './pages/Q8';
import Q9 from './pages/Q9';
import Q10 from './pages/Q10';
import Q11 from './pages/Q11';
import Q12 from './pages/Q12';
import Q13 from './pages/Q13';
import Q14 from './pages/Q14';
import Q15 from './pages/Q15';
import Q16 from './pages/Q16';
import Q17 from './pages/Q17';
import Q18 from './pages/Q18';
import Q19 from './pages/Q19';
import Q20 from './pages/Q20';

const QUESTIONS = [
  { path: 'q1',  label: 'Q1 Registration Form' },
  { path: 'q2',  label: 'Q2 Temp Converter' },
  { path: 'q3',  label: 'Q3 Survey Builder' },
  { path: 'q4',  label: 'Q4 Theme+Lang' },
  { path: 'q5',  label: 'Q5 Shopping Cart' },
  { path: 'q6',  label: 'Q6 Multi-Step Form' },
  { path: 'q7',  label: 'Q7 useFetch Hook' },
  { path: 'q8',  label: 'Q8 useLocalStorage' },
  { path: 'q9',  label: 'Q9 useDebounce' },
  { path: 'q10', label: 'Q10 Stopwatch' },
  { path: 'q11', label: 'Q11 Blog Router' },
  { path: 'q12', label: 'Q12 Protected Routes' },
  { path: 'q13', label: 'Q13 CRUD Axios' },
  { path: 'q14', label: 'Q14 Error Boundary' },
  { path: 'q15', label: 'Q15 Perf List' },
  { path: 'q16', label: 'Q16 Redux Counter' },
  { path: 'q17', label: 'Q17 Redux Todos' },
  { path: 'q18', label: 'Q18 Redux Auth' },
  { path: 'q19', label: 'Q19 AsyncThunk' },
  { path: 'q20', label: 'Q20 Redux Cart' },
];

function Nav() {
  return (
    <nav className="app-nav">
      <span style={{ color: '#fff', fontWeight: 700, fontSize: 13, marginRight: 8 }}>React Day 2</span>
      {QUESTIONS.map(q => (
        <NavLink key={q.path} to={q.path}
          className={({ isActive }) => isActive ? 'active' : ''}>
          {q.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route index element={<Navigate to="q1" replace />} />
        <Route path="q1" element={<Q1 />} />
        <Route path="q2" element={<Q2 />} />
        <Route path="q3" element={<Q3 />} />
        <Route path="q4" element={<Q4 />} />
        <Route path="q5" element={<Q5 />} />
        <Route path="q6" element={<Q6 />} />
        <Route path="q7" element={<Q7 />} />
        <Route path="q8" element={<Q8 />} />
        <Route path="q9" element={<Q9 />} />
        <Route path="q10" element={<Q10 />} />
        <Route path="q11/*" element={<Q11 />} />
        <Route path="q12/*" element={<Q12 />} />
        <Route path="q13" element={<Q13 />} />
        <Route path="q14" element={<Q14 />} />
        <Route path="q15" element={<Q15 />} />
        <Route path="q16" element={<Q16 />} />
        <Route path="q17" element={<Q17 />} />
        <Route path="q18/*" element={<Q18 />} />
        <Route path="q19" element={<Q19 />} />
        <Route path="q20" element={<Q20 />} />
      </Routes>
    </BrowserRouter>
  );
}
