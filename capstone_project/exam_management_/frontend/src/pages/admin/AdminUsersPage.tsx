import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Users, Shield, GraduationCap, UserX, Trophy, Clock, CheckCircle, XCircle } from 'lucide-react'
import { adminApi } from '@/api/services'
import { useFetch } from '@/hooks'
import { Button, Badge, EmptyState, PageLoader, Card } from '@/components/shared/UI'
import { format } from 'date-fns'
import toast from 'react-hot-toast'

// ─── Admin Users Page ─────────────────────────────────────────────────────────
export const AdminUsersPage: React.FC = () => {
  const [page, setPage] = useState(1)
  const [roleFilter, setRoleFilter] = useState<string>('')
  const { data, loading, refetch } = useFetch(
    () => adminApi.users({ page, page_size: 20, role: roleFilter || undefined }),
    [page, roleFilter]
  )

  const handleDeactivate = async (id: number) => {
    if (!confirm('Deactivate this user?')) return
    try {
      await adminApi.deactivateUser(id)
      toast.success('User deactivated')
      refetch()
    } catch { toast.error('Failed') }
  }

  return (
    <div style={{ maxWidth: '1000px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '28px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>Users</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{data?.total ?? 0} registered users</p>
      </motion.div>

      {/* Role filter */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        {['', 'admin', 'student'].map(r => (
          <button key={r} onClick={() => { setRoleFilter(r); setPage(1) }}
            style={{
              padding: '6px 16px', borderRadius: '100px', fontSize: '0.8rem', cursor: 'pointer',
              border: `1px solid ${roleFilter === r ? 'var(--gold)' : 'var(--border-default)'}`,
              background: roleFilter === r ? 'var(--gold-dim)' : 'transparent',
              color: roleFilter === r ? 'var(--gold)' : 'var(--text-secondary)',
              transition: 'all 0.15s', fontFamily: 'var(--font-body)',
            }}>
            {r === '' ? 'All' : r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      {loading ? <PageLoader /> : (
        <>
          {data?.items.length === 0 ? (
            <EmptyState icon={<Users size={40} />} title="No users found" />
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {data?.items.map((user, i) => (
                <motion.div key={user.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.03 }}>
                  <Card>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                        <div style={{
                          width: 40, height: 40, borderRadius: '50%', flexShrink: 0,
                          background: user.role === 'admin'
                            ? 'linear-gradient(135deg, var(--gold), var(--gold-light))'
                            : 'linear-gradient(135deg, var(--accent), #818cf8)',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontSize: '1rem', fontWeight: 600, color: 'var(--bg-void)',
                        }}>
                          {user.full_name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <div style={{ fontWeight: 500, color: 'var(--text-primary)', marginBottom: '2px' }}>{user.full_name}</div>
                          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{user.email}</div>
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                        <Badge variant={user.role === 'admin' ? 'gold' : 'blue'}>
                          {user.role === 'admin' ? <Shield size={11} /> : <GraduationCap size={11} />}
                          {user.role}
                        </Badge>
                        {!user.is_active && <Badge variant="error">Inactive</Badge>}
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                          {format(new Date(user.created_at), 'MMM dd, yyyy')}
                        </span>
                        {user.is_active && (
                          <Button variant="danger" size="sm" icon={<UserX size={13} />} onClick={() => handleDeactivate(user.id)}>
                            Deactivate
                          </Button>
                        )}
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}

          {data && data.total > 20 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '24px' }}>
              <Button variant="ghost" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</Button>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', alignSelf: 'center' }}>{page} / {Math.ceil(data.total / 20)}</span>
              <Button variant="ghost" size="sm" disabled={page >= Math.ceil(data.total / 20)} onClick={() => setPage(p => p + 1)}>Next</Button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

// ─── Admin Exam Results Page ───────────────────────────────────────────────────
export const AdminExamResultsPage: React.FC = () => {
  const { examId } = useParams<{ examId: string }>()
  const [page, setPage] = useState(1)
  const { data, loading } = useFetch(
    () => adminApi.examResults(Number(examId), { page, page_size: 20 }),
    [examId, page]
  )

  const fmtTime = (secs: number | null) => {
    if (!secs) return '—'
    const m = Math.floor(secs / 60), s = secs % 60
    return `${m}m ${s}s`
  }

  return (
    <div style={{ maxWidth: '1000px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '28px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
          {data?.exam_title ?? 'Exam Results'}
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{data?.total ?? 0} attempts recorded</p>
      </motion.div>

      {loading ? <PageLoader /> : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {data?.items.length === 0 ? (
            <EmptyState icon={<Trophy size={40} />} title="No attempts yet" />
          ) : data?.items.map((result, i) => (
            <motion.div key={result.attempt_id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
              <Card>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: 36, height: 36, borderRadius: '50%',
                      background: result.passed ? 'var(--success-dim)' : 'var(--error-dim)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                    }}>
                      {result.passed ? <CheckCircle size={18} color="var(--success)" /> : <XCircle size={18} color="var(--error)" />}
                    </div>
                    <div>
                      <div style={{ fontWeight: 500, color: 'var(--text-primary)', marginBottom: '2px' }}>{result.student_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{result.student_email}</div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.1rem', color: result.passed ? 'var(--success)' : 'var(--error)', fontWeight: 500 }}>
                        {result.percentage?.toFixed(1) ?? '—'}%
                      </div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                        {result.score ?? 0}/{result.total_marks}
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                      <Clock size={13} /> {fmtTime(result.time_taken_seconds)}
                    </div>
                    <Badge variant={result.passed ? 'success' : 'error'}>
                      {result.passed ? 'Passed' : 'Failed'}
                    </Badge>
                    <Badge variant="default">Attempt #{result.attempt_number}</Badge>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
