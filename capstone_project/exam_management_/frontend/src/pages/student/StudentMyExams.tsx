import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ClipboardList, Clock, Target, ChevronRight, BookOpen } from 'lucide-react'
import { enrollmentApi } from '@/api/services'
import { useFetch } from '@/hooks'
import { Button, EmptyState, PageLoader, Card } from '@/components/shared/UI'
import StarBorder from '@/components/shared/StarBorder'
import { format } from 'date-fns'

export const StudentMyExams: React.FC = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)

  const { data, loading } = useFetch(
    () => enrollmentApi.myExams({ page, page_size: 10 }),
    [page]
  )

  return (
    <div style={{ maxWidth: '900px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '28px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
          My Exams
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          {data?.total ?? 0} enrolled exams
        </p>
      </motion.div>

      {loading ? <PageLoader /> : (
        <>
          {data?.items.length === 0 ? (
            <EmptyState
              icon={<ClipboardList size={44} />}
              title="No enrolled exams"
              description="Browse available exams and enroll to get started"
              action={
                <StarBorder as="button" color="var(--gold)" speed="5s" thickness={2} onClick={() => navigate('/student/exams')} style={{ minWidth: 160 }}>
                  <BookOpen size={14} /> Browse Exams
                </StarBorder>
              }
            />
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {data?.items.map((exam, i) => (
                <motion.div
                  key={exam.enrollment_id}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Card hover onClick={() => navigate(`/student/exam/${exam.exam_id}`)}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
                          {exam.title}
                        </h3>
                        {exam.description && (
                          <p style={{ color: 'var(--text-muted)', fontSize: '0.83rem', marginBottom: '10px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {exam.description}
                          </p>
                        )}
                        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                            <Clock size={13} style={{ color: 'var(--gold)' }} /> {exam.duration_minutes} min
                          </span>
                          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                            <Target size={13} style={{ color: 'var(--success)' }} /> Pass: {exam.pass_percentage}%
                          </span>
                          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                            Enrolled {format(new Date(exam.registered_at), 'MMM dd, yyyy')}
                          </span>
                        </div>
                      </div>
                      <StarBorder as="button" color="var(--accent)" speed="5s" thickness={2} style={{ minWidth: 120 }}>
                        <ChevronRight size={14} /> Start Exam
                      </StarBorder>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}

          {data && data.total > 10 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '24px' }}>
              <Button variant="ghost" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</Button>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', alignSelf: 'center' }}>
                {page} / {Math.ceil(data.total / 10)}
              </span>
              <Button variant="ghost" size="sm" disabled={page >= Math.ceil(data.total / 10)} onClick={() => setPage(p => p + 1)}>Next →</Button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
