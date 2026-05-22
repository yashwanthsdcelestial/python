import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks'
import { PageLoader } from '@/components/shared/UI'
import { AppLayout } from '@/components/layout/AppLayout'

// Auth pages
import { LoginPage, RegisterPage } from '@/pages/auth/AuthPages'

// Admin pages
import { AdminDashboard } from '@/pages/admin/AdminDashboard'
import { AdminExamsPage } from '@/pages/admin/AdminExamsPage'
import { AdminUsersPage, AdminExamResultsPage } from '@/pages/admin/AdminUsersPage'

// Student pages
import { StudentDashboard } from '@/pages/student/StudentDashboard'
import { StudentBrowseExams } from '@/pages/student/StudentBrowseExams'
import { StudentMyExams } from '@/pages/student/StudentMyExams'
import { ExamTakingPage } from '@/pages/student/ExamTakingPage'
import { StudentResults } from '@/pages/student/StudentResults'
import { AttemptDetailPage } from '@/pages/student/AttemptDetailPage'

// ─── Auth init wrapper ────────────────────────────────────────────────────────
const AuthInit: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { fetchMe, isAuthenticated, isLoading } = useAuth()

  useEffect(() => {
    fetchMe()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (isLoading) return <PageLoader />
  return <>{children}</>
}

// ─── Root redirect ────────────────────────────────────────────────────────────
const RootRedirect: React.FC = () => {
  const { isAuthenticated, isAdmin, isLoading } = useAuth()
  if (isLoading) return <PageLoader />
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <Navigate to={isAdmin ? '/admin' : '/student'} replace />
}

// ─── Protected Route ──────────────────────────────────────────────────────────
const ProtectedRoute: React.FC<{ children: React.ReactNode; requireRole?: 'admin' | 'student' }> = ({ children, requireRole }) => {
  const { isAuthenticated, isAdmin, isStudent, isLoading } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) navigate('/login', { replace: true })
    if (!isLoading && isAuthenticated && requireRole === 'admin' && !isAdmin) navigate('/student', { replace: true })
    if (!isLoading && isAuthenticated && requireRole === 'student' && !isStudent) navigate('/admin', { replace: true })
  }, [isAuthenticated, isAdmin, isStudent, isLoading, requireRole, navigate])

  if (isLoading) return <PageLoader />
  if (!isAuthenticated) return null
  if (requireRole === 'admin' && !isAdmin) return null
  if (requireRole === 'student' && !isStudent) return null

  return <>{children}</>
}

// ─── App Router ───────────────────────────────────────────────────────────────
export const AppRouter: React.FC = () => (
  <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
    <AuthInit>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<RootRedirect />} />

        {/* Admin routes */}
        <Route path="/admin" element={
          <ProtectedRoute requireRole="admin"><AppLayout /></ProtectedRoute>
        }>
          <Route index element={<AdminDashboard />} />
          <Route path="exams" element={<AdminExamsPage />} />
          <Route path="exams/:examId" element={<AdminExamResultsPage />} />
          <Route path="users" element={<AdminUsersPage />} />
        </Route>

        {/* Student routes */}
        <Route path="/student" element={
          <ProtectedRoute requireRole="student"><AppLayout /></ProtectedRoute>
        }>
          <Route index element={<StudentDashboard />} />
          <Route path="exams" element={<StudentBrowseExams />} />
          <Route path="my-exams" element={<StudentMyExams />} />
          <Route path="exam/:examId" element={<ExamTakingPage />} />
          <Route path="results" element={<StudentResults />} />
          <Route path="result/:attemptId" element={<AttemptDetailPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthInit>
  </BrowserRouter>
)