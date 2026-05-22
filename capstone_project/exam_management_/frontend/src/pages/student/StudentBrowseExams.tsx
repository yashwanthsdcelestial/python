import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, BookOpen, Clock, Target, Users, ChevronRight, CheckCircle } from 'lucide-react'
import { examApi, enrollmentApi } from '@/api/services'
import { useFetch, useDebounce } from '@/hooks'
import { Button, Badge, EmptyState, PageLoader, Input } from '@/components/shared/UI'
import StarBorder from '@/components/shared/StarBorder'
import toast from 'react-hot-toast'

export const StudentBrowseExams: React.FC = () => {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [enrolling, setEnrolling] = useState<number | null>(null)
  const debouncedSearch = useDebounce(search)

  const { data, loading, refetch } = useFetch(
    () => examApi.list({ page, page_size: 9, search: debouncedSearch || undefined }),
    [page, debouncedSearch]
  )

  const handleEnroll = async (examId: number) => {
    setEnrolling(examId)
    try {
      await enrollmentApi.enroll(examId)
      toast.success('Enrolled successfully!')
      refetch()
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Enrollment failed'
      toast.error(msg)
    } finally {
      setEnrolling(null)
    }
  }

  return (
    <div style={{ maxWidth: '1100px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '28px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
          Browse Exams
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          {data?.total ?? 0} exams available
        </p>
      </motion.div>

      {/* Search */}
      <div style={{ marginBottom: '24px' }}>
        <Input
          placeholder="Search exams by title or description..."
          icon={<Search size={16} />}
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(1) }}
          style={{ maxWidth: '420px' }}
        />
      </div>

      {loading ? <PageLoader /> : (
        <>
          {data?.items.length === 0 ? (
            <EmptyState
              icon={<BookOpen size={44} />}
              title="No exams found"
              description="Try adjusting your search query"
            />
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
              {data?.items.map((exam, i) => (
                <motion.div
                  key={exam.id}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.06 }}
                  whileHover={{ y: -3 }}
                  style={{
                    background: 'var(--bg-card)',
                    border: `1px solid ${exam.is_enrolled ? 'rgba(79,142,247,0.25)' : 'var(--border-subtle)'}`,
                    borderRadius: 'var(--radius-lg)',
                    padding: '22px',
                    boxShadow: 'var(--shadow-card)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '14px',
                    position: 'relative',
                    overflow: 'hidden',
                  }}
                >
                  {/* Top accent line */}
                  <div style={{
                    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
                    background: exam.is_enrolled
                      ? 'linear-gradient(90deg, var(--accent), transparent)'
                      : 'linear-gradient(90deg, var(--gold), transparent)',
                    opacity: 0.7,
                  }} />

                  {/* Header */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                      <h3 style={{
                        fontFamily: 'var(--font-display)', fontSize: '1.1rem',
                        color: 'var(--text-primary)', lineHeight: 1.3, flex: 1, paddingRight: '8px',
                      }}>
                        {exam.title}
                      </h3>
                      {exam.is_enrolled && (
                        <span style={{ color: 'var(--accent)', flexShrink: 0 }}>
                          <CheckCircle size={18} />
                        </span>
                      )}
                    </div>
                    {exam.description && (
                      <p style={{
                        color: 'var(--text-muted)', fontSize: '0.83rem', lineHeight: 1.5,
                        display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden',
                      }}>
                        {exam.description}
                      </p>
                    )}
                  </div>

                  {/* Meta info */}
                  <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                      <Clock size={13} style={{ color: 'var(--gold)' }} />
                      {exam.duration_minutes} min
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                      <BookOpen size={13} style={{ color: 'var(--accent)' }} />
                      {exam.question_count} questions
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                      <Target size={13} style={{ color: 'var(--success)' }} />
                      Pass: {exam.pass_percentage}%
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                      <Users size={13} style={{ color: '#a78bfa' }} />
                      {exam.max_attempts} attempt{exam.max_attempts > 1 ? 's' : ''}
                    </span>
                  </div>

                  {/* Total marks badge */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '0.8rem',
                      color: 'var(--text-muted)',
                    }}>
                      {exam.total_marks} marks total
                    </span>
                    <Badge variant="default">{exam.total_marks} pts</Badge>
                  </div>

                  {/* Action */}
                  {exam.is_enrolled ? (
                    <Button
                      variant="primary"
                      size="sm"
                      style={{ width: '100%' }}
                      icon={<ChevronRight size={14} />}
                      onClick={() => navigate(`/student/exam/${exam.id}`)}
                    >
                      Go to Exam
                    </Button>
                  ) : (
                    <StarBorder
                      as="button"
                      color="var(--gold)"
                      speed="5s"
                      thickness={2}
                      disabled={enrolling === exam.id}
                      onClick={() => handleEnroll(exam.id)}
                    >
                      {enrolling === exam.id ? 'Enrolling...' : 'Enroll Now'}
                    </StarBorder>
                  )}
                </motion.div>
              ))}
            </div>
          )}

          {/* Pagination */}
          {data && data.total > 9 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '28px' }}>
              <Button variant="ghost" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</Button>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', alignSelf: 'center' }}>
                Page {page} of {Math.ceil(data.total / 9)}
              </span>
              <Button variant="ghost" size="sm" disabled={page >= Math.ceil(data.total / 9)} onClick={() => setPage(p => p + 1)}>Next →</Button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
