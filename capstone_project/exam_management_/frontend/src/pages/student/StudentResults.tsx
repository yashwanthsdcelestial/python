import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Award, Clock, CheckCircle, XCircle, AlertTriangle, ChevronRight } from 'lucide-react'
import { attemptApi } from '@/api/services'
import { useFetch } from '@/hooks'
import { Button, Badge, EmptyState, PageLoader, Card } from '@/components/shared/UI'
import { format } from 'date-fns'
import type { AttemptStatus } from '@/types'

const statusBadge = (status: AttemptStatus, passed: boolean | null) => {
  if (status === 'in_progress') return <Badge variant="warning"><AlertTriangle size={11} /> In Progress</Badge>
  if (status === 'timed_out') return <Badge variant="error"><Clock size={11} /> Timed Out</Badge>
  if (passed) return <Badge variant="success"><CheckCircle size={11} /> Passed</Badge>
  return <Badge variant="error"><XCircle size={11} /> Failed</Badge>
}

const fmtSeconds = (s: number | null) => {
  if (!s) return '—'
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}m ${sec}s`
}

export const StudentResults: React.FC = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)

  const { data, loading } = useFetch(
    () => attemptApi.myResults({ page, page_size: 10 }),
    [page]
  )

  const completed = data?.items.filter(a => a.status !== 'in_progress') ?? []
  const passed = completed.filter(a => a.passed).length
  const avgPct = completed.length
    ? Math.round(completed.reduce((s, a) => s + (a.percentage ?? 0), 0) / completed.length)
    : 0

  return (
    <div style={{ maxWidth: '900px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '28px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
          My Results
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{data?.total ?? 0} total attempts</p>
      </motion.div>

      {/* Summary row */}
      {completed.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '24px' }}>
          {[
            { label: 'Completed', value: completed.length, color: 'var(--accent)' },
            { label: 'Passed', value: passed, color: 'var(--success)' },
            { label: 'Avg Score', value: `${avgPct}%`, color: 'var(--gold)' },
          ].map(({ label, value, color }) => (
            <div key={label} style={{
              background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-lg)', padding: '16px', textAlign: 'center',
            }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.6rem', fontWeight: 500, color, marginBottom: '4px' }}>{value}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</div>
            </div>
          ))}
        </motion.div>
      )}

      {loading ? <PageLoader /> : (
        <>
          {data?.items.length === 0 ? (
            <EmptyState
              icon={<Award size={44} />}
              title="No results yet"
              description="Complete an exam to see your results here"
              action={<Button variant="gold" onClick={() => navigate('/student/exams')}>Browse Exams</Button>}
            />
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {data?.items.map((attempt, i) => (
                <motion.div
                  key={attempt.id}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.04 }}
                >
                  <Card hover onClick={() => navigate(`/student/result/${attempt.id}`)}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', flexWrap: 'wrap' }}>
                          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1rem', color: 'var(--text-primary)' }}>
                            {attempt.exam_title}
                          </h3>
                          {statusBadge(attempt.status, attempt.passed)}
                          {attempt.attempt_number > 1 && <Badge variant="default">Attempt #{attempt.attempt_number}</Badge>}
                        </div>
                        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                            {format(new Date(attempt.started_at), 'MMM dd, yyyy HH:mm')}
                          </span>
                          {attempt.time_taken_seconds != null && (
                            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                              <Clock size={12} /> {fmtSeconds(attempt.time_taken_seconds)}
                            </span>
                          )}
                        </div>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexShrink: 0 }}>
                        {attempt.percentage != null && (
                          <div style={{ textAlign: 'right' }}>
                            <div style={{
                              fontFamily: 'var(--font-mono)', fontSize: '1.4rem', fontWeight: 500,
                              color: attempt.passed ? 'var(--success)' : 'var(--error)',
                            }}>
                              {attempt.percentage.toFixed(1)}%
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                              {attempt.score ?? 0}/{attempt.total_marks} marks
                            </div>
                          </div>
                        )}
                        <ChevronRight size={18} style={{ color: 'var(--text-muted)' }} />
                      </div>
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
