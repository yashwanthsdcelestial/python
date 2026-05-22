// ─── Auth ────────────────────────────────────────────────────────────────────
export type Role = 'admin' | 'student'

export interface User {
  id: number
  email: string
  full_name: string
  role: Role
  is_active: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

// ─── Exam ────────────────────────────────────────────────────────────────────
export type ExamStatus = 'draft' | 'published' | 'archived'

export interface Question {
  id: number
  text: string
  options: string[]
  marks: number
  correct_answer?: string // only for admin
}

export interface Exam {
  id: number
  title: string
  description: string | null
  duration_minutes: number
  total_marks: number
  pass_percentage: number
  status: ExamStatus
  max_attempts: number
  start_time: string | null
  end_time: string | null
  created_by: number
  created_at: string
  question_count: number
  is_enrolled: boolean
  questions?: Question[]
}

export interface ExamListResponse {
  total: number
  page: number
  page_size: number
  items: Exam[]
}

// ─── Enrollment ───────────────────────────────────────────────────────────────
export interface EnrolledExam {
  enrollment_id: number
  exam_id: number
  title: string
  description: string | null
  duration_minutes: number
  total_marks: number
  pass_percentage: number
  status: ExamStatus
  registered_at: string
}

// ─── Attempt ─────────────────────────────────────────────────────────────────
export type AttemptStatus = 'in_progress' | 'submitted' | 'timed_out'

export interface AttemptStart {
  id: number
  exam_id: number
  started_at: string
  duration_minutes: number
  questions: Question[]
}

export interface AttemptResult {
  id: number
  exam_id: number
  exam_title: string
  status: AttemptStatus
  score: number | null
  total_marks: number
  percentage: number | null
  passed: boolean | null
  started_at: string
  submitted_at: string | null
  time_taken_seconds: number | null
  attempt_number: number
}

export interface AttemptDetail extends AttemptResult {
  answers: {
    question_id: number
    selected_answer: string
    is_correct: boolean
    marks_awarded: number
  }[]
}

// ─── Admin ────────────────────────────────────────────────────────────────────
export interface AdminStats {
  total_users: number
  total_students: number
  total_exams: number
  published_exams: number
  total_attempts: number
  passed_attempts: number
}

export interface ExamResult {
  attempt_id: number
  student_id: number
  student_name: string
  student_email: string
  score: number | null
  total_marks: number
  percentage: number | null
  passed: boolean | null
  status: AttemptStatus
  started_at: string
  submitted_at: string | null
  attempt_number: number
}

// ─── Pagination ───────────────────────────────────────────────────────────────
export interface PaginatedResponse<T> {
  total: number
  page: number
  page_size: number
  items: T[]
}
