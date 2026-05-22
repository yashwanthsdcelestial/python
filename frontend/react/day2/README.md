# React Day 2 Assignments

All 20 coding assignments implemented in a single React app.

## Setup & Run

```bash
npm install
npm start
```

Then open http://localhost:3000 in your browser.

## Navigation

Use the top navigation bar to switch between all 20 questions.

## Questions Covered

### Section A — Forms, Validation & State Lifting
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q1 | Multi-Field Registration Form | Controlled Components, Validation, Error State |
| Q2 | Temperature Converter | Lifting State Up, Sibling Sync |
| Q3 | Dynamic Survey Form Builder | Dynamic Rendering, Validation |

### Section B — Context API & useReducer
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q4 | Theme + Language Switcher | Context API, Multiple Contexts, localStorage |
| Q5 | Shopping Cart | useReducer, Context API, State Sharing |
| Q6 | Multi-Step Form | useReducer, Multi-Step Flow, Validation |

### Section C — Custom Hooks & useRef
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q7 | useFetch Hook | Custom Hooks, AbortController |
| Q8 | useLocalStorage Hook | Custom Hooks, localStorage Persistence |
| Q9 | useDebounce + Search | Custom Hooks, Debouncing, API Integration |
| Q10 | Stopwatch | useRef, setInterval, State Management |

### Section D — Routing, Auth & API Integration
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q11 | Multi-Page Blog | React Router, Dynamic Routes, useNavigate |
| Q12 | Protected Dashboard | Protected Routes, Context Auth, Nested Routes |
| Q13 | CRUD App with Axios | Axios, CRUD Operations, Loading & Error States |

### Section E — Performance & Error Handling
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q14 | Error Boundary + Lazy Loading | ErrorBoundary, React.lazy, Suspense |
| Q15 | Optimized Large List | React.memo, useCallback, useMemo |

### Section F — Redux Toolkit
| Q | Topic | Key Concepts |
|---|-------|-------------|
| Q16 | Redux Counter | createSlice, useSelector, useDispatch |
| Q17 | Redux Todo List | Multiple Reducers, Component Connection |
| Q18 | Redux Auth + Protected Routes | authSlice, ProtectedRoute, Persistence |
| Q19 | Async Users (createAsyncThunk) | Async Thunks, pending/fulfilled/rejected |
| Q20 | Multi-Slice Shopping Cart | Multiple Slices, Async Thunks, Selectors |

## Project Structure

```
src/
├── App.js                  # Main router
├── index.js                # Entry point (Redux Provider)
├── index.css               # Global styles
├── context/
│   ├── AuthContext.js      # Auth context (Q12)
│   ├── CartContext.js      # Cart context with useReducer (Q5)
│   ├── ThemeContext.js     # Theme context (Q4)
│   └── LanguageContext.js  # Language context (Q4)
├── hooks/
│   ├── useFetch.js         # Q7
│   ├── useLocalStorage.js  # Q8
│   └── useDebounce.js      # Q9
├── store/
│   ├── index.js            # Redux store setup
│   └── slices/
│       ├── counterSlice.js # Q16
│       ├── todoSlice.js    # Q17
│       ├── authSlice.js    # Q18
│       ├── usersSlice.js   # Q19
│       ├── productsSlice.js# Q20
│       └── cartSlice.js    # Q20
└── pages/
    ├── Q1.jsx  ... Q20.jsx # All 20 assignment pages
```
