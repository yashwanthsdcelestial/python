import api from './client'
import type {
  User, TokenResponse, Exam, ExamListResponse, EnrolledExam,
  AttemptStart, AttemptResult, AttemptDetail, AdminStats,
  ExamResult, PaginatedResponse,
} from '@/types'

// ─── Auth ─────────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data: { email: string; password: string; full_name: string; role: string }) =>
    api.post<User>('/auth/register', data).then(r => r.data),

  login: (data: { email: string; password: string }) =>
    api.post<TokenResponse>('/auth/login', data).then(r => r.data),

  refresh: (refresh_token: string) =>
    api.post<TokenResponse>('/auth/refresh', { refresh_token }).then(r => r.data),

  me: () => api.get<User>('/auth/me').then(r => r.data),
}

// ─── Exams ────────────────────────────────────────────────────────────────────
export const examApi = {
  list: (params?: { page?: number; page_size?: number; search?: string; sort_by?: string; sort_desc?: boolean }) =>
    api.get<ExamListResponse>('/exams', { params }).then(r => r.data),

  get: (id: number) => api.get<Exam>(`/exams/${id}`).then(r => r.data),

  create: (data: unknown) => api.post<Exam>('/exams', data).then(r => r.data),

  update: (id: number, data: unknown) => api.put<Exam>(`/exams/${id}`, data).then(r => r.data),

  delete: (id: number) => api.delete(`/exams/${id}`).then(r => r.data),
}

// ─── Enrollments ──────────────────────────────────────────────────────────────
export const enrollmentApi = {
  enroll: (examId: number) => api.post(`/enrollments/${examId}`).then(r => r.data),

  myExams: (params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<EnrolledExam>>('/enrollments', { params }).then(r => r.data),
}

// ─── Attempts ─────────────────────────────────────────────────────────────────
export const attemptApi = {
  start: (examId: number) => api.post<AttemptStart>(`/attempts/start/${examId}`).then(r => r.data),

  submit: (attemptId: number, answers: { question_id: number; selected_answer: string }[]) =>
    api.post<AttemptResult>(`/attempts/${attemptId}/submit`, { answers }).then(r => r.data),

  myResults: (params?: { page?: number; page_size?: number }) =>
    api.get<{ total: number; items: AttemptResult[] }>('/attempts/my-results', { params }).then(r => r.data),

  get: (attemptId: number) => api.get<AttemptDetail>(`/attempts/${attemptId}`).then(r => r.data),
}

// ─── Admin ────────────────────────────────────────────────────────────────────
export const adminApi = {
  stats: () => api.get<AdminStats>('/admin/stats').then(r => r.data),

  users: (params?: { page?: number; page_size?: number; role?: string }) =>
    api.get<PaginatedResponse<User>>('/admin/users', { params }).then(r => r.data),

  deactivateUser: (userId: number) =>
    api.patch(`/admin/users/${userId}/deactivate`).then(r => r.data),

  examResults: (examId: number, params?: { page?: number; page_size?: number }) =>
    api.get<{ exam_title: string; total: number; page: number; page_size: number; items: ExamResult[] }>(
      `/admin/exam-results/${examId}`, { params }
    ).then(r => r.data),

  studentExamSummary: () =>
    api.get<{ items: unknown[] }>('/admin/view/student-exam-summary').then(r => r.data),
}
