import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { BookOpen, Award, TrendingUp, Clock, ChevronRight } from 'lucide-react'
import { useAuth, useFetch } from '@/hooks'
import { attemptApi, enrollmentApi } from '@/api/services'
import { StatCard, Card, Badge, PageLoader, Button } from '@/components/shared/UI'
import { format } from 'date-fns'

export const StudentDashboard: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const { data: results, loading: loadingResults } = useFetch(() => attemptApi.myResults({ page: 1, page_size: 5 }))
  const { data: enrolled, loading: loadingEnrolled } = useFetch(() => enrollmentApi.myExams({ page: 1, page_size: 4 }))

  const completedAttempts = results?.items.filter(a => a.status !== 'in_progress') ?? []
  const passedCount = completedAttempts.filter(a => a.passed).length
  const avgScore = completedAttempts.length
    ? Math.round(completedAttempts.reduce((s, a) => s + (a.percentage ?? 0), 0) / completedAttempts.length)
    : 0

  if (loadingResults && loadingEnrolled) return <PageLoader />

  return (
    <div style={{ maxWidth: '1000px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '32px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
          Hello, <span style={{ color: 'var(--gold)' }}>{user?.full_name?.split(' ')[0]}</span>
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Your learning dashboard</p>
      </motion.div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '14px', marginBottom: '28px' }}>
        <StatCard label="Enrolled Exams" value={enrolled?.total ?? 0} icon={<BookOpen size={20} />} color="var(--accent)" delay={0} />
        <StatCard label="Completed" value={completedAttempts.length} icon={<TrendingUp size={20} />} color="var(--gold)" delay={0.05} />
        <StatCard label="Passed" value={passedCount} icon={<Award size={20} />} color="var(--success)" delay={0.1} />
        <StatCard label="Avg Score" value={`${avgScore}%`} icon={<TrendingUp size={20} />} color="#a78bfa" delay={0.15} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Enrolled exams */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)' }}>My Exams</h2>
              <Button variant="ghost" size="sm" onClick={() => navigate('/student/my-exams')}>
                View all <ChevronRight size={14} />
              </Button>
            </div>
            {enrolled?.items.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                No exams enrolled yet.<br />
                <Button variant="ghost" size="sm" style={{ marginTop: '8px' }} onClick={() => navigate('/student/exams')}>Browse exams →</Button>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {enrolled?.items.slice(0, 4).map(exam => (
                  <div key={exam.exam_id} style={{
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    padding: '10px 12px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)',
                  }}>
                    <div style={{ overflow: 'hidden', flex: 1 }}>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-primary)', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{exam.title}</div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '2px' }}>
                        <Clock size={11} /> {exam.duration_minutes}m
                      </div>
                    </div>
                    <Button variant="primary" size="sm" onClick={() => navigate(`/student/exam/${exam.exam_id}`)}>
                      Start
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </motion.div>

        {/* Recent results */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Recent Results</h2>
              <Button variant="ghost" size="sm" onClick={() => navigate('/student/results')}>
                View all <ChevronRight size={14} />
              </Button>
            </div>
            {completedAttempts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)', fontSize: '0.875rem' }}>No results yet</div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {completedAttempts.slice(0, 4).map(attempt => (
                  <div key={attempt.id} style={{
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    padding: '10px 12px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)',
                  }}>
                    <div style={{ overflow: 'hidden', flex: 1 }}>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-primary)', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{attempt.exam_title}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        {format(new Date(attempt.started_at), 'MMM dd')}
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: attempt.passed ? 'var(--success)' : 'var(--error)', fontWeight: 500 }}>
                        {attempt.percentage?.toFixed(0)}%
                      </span>
                      <Badge variant={attempt.passed ? 'success' : 'error'}>{attempt.passed ? 'Pass' : 'Fail'}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
