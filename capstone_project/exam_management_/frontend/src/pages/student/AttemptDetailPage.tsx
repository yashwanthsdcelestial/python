import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ChevronLeft, CheckCircle, XCircle, Clock, Award } from 'lucide-react'
import { attemptApi, examApi } from '@/api/services'
import { useFetch } from '@/hooks'
import { Button, Badge, PageLoader, Card } from '@/components/shared/UI'
import { format } from 'date-fns'

export const AttemptDetailPage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>()
  const navigate = useNavigate()

  const { data: attempt, loading } = useFetch(
    () => attemptApi.get(Number(attemptId)),
    [attemptId]
  )
  const { data: exam } = useFetch(
    () => attempt ? examApi.get(attempt.exam_id) : Promise.reject(),
    [attempt?.exam_id]
  )

  if (loading) return <PageLoader />
  if (!attempt) return null

  const answerMap = Object.fromEntries(attempt.answers.map(a => [a.question_id, a]))
  const pct = attempt.percentage ?? 0

  return (
    <div style={{ maxWidth: '800px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <Button variant="ghost" size="sm" icon={<ChevronLeft size={16} />} onClick={() => navigate(-1)}
          style={{ marginBottom: '20px' }}>
          Back
        </Button>

        {/* Header card */}
        <Card style={{ marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
            <div>
              <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.6rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
                {attempt.exam_title}
              </h1>
              <div style={{ display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
                <Badge variant={attempt.passed ? 'success' : 'error'}>
                  {attempt.passed ? <CheckCircle size={11} /> : <XCircle size={11} />}
                  {attempt.passed ? 'Passed' : 'Failed'}
                </Badge>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {attempt.submitted_at ? format(new Date(attempt.submitted_at), 'MMM dd, yyyy HH:mm') : '—'}
                </span>
                {attempt.time_taken_seconds != null && (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    <Clock size={12} />
                    {Math.floor(attempt.time_taken_seconds / 60)}m {attempt.time_taken_seconds % 60}s
                  </span>
                )}
              </div>
            </div>

            <div style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '2.4rem', fontWeight: 500, color: attempt.passed ? 'var(--success)' : 'var(--error)', lineHeight: 1 }}>
                {pct.toFixed(1)}%
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {attempt.score ?? 0} / {attempt.total_marks} marks
              </div>
            </div>
          </div>

          {/* Score progress */}
          <div style={{ marginTop: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Score</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                Need {exam?.pass_percentage}% to pass
              </span>
            </div>
            <div style={{ height: '6px', background: 'var(--bg-elevated)', borderRadius: '3px', overflow: 'hidden' }}>
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
                style={{
                  height: '100%',
                  background: attempt.passed
                    ? 'linear-gradient(90deg, var(--success), #6ee7b7)'
                    : 'linear-gradient(90deg, var(--error), #fca5a5)',
                  borderRadius: '3px',
                }}
              />
            </div>
            {/* Pass threshold marker */}
            <div style={{ position: 'relative', height: '16px', marginTop: '-4px' }}>
              <div style={{
                position: 'absolute', left: `${exam?.pass_percentage ?? 60}%`,
                width: '2px', height: '12px', background: 'var(--gold)', opacity: 0.7,
                transform: 'translateX(-50%)',
              }} />
            </div>
          </div>
        </Card>

        {/* Q&A breakdown */}
        <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Award size={16} style={{ color: 'var(--gold)' }} />
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Answer Review</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {exam?.questions?.map((q, qi) => {
            const ans = answerMap[q.id]
            const isCorrect = ans?.is_correct
            const selected = ans?.selected_answer

            return (
              <motion.div
                key={q.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: qi * 0.04 }}
              >
                <Card style={{
                  borderColor: isCorrect ? 'rgba(52,211,153,0.2)' : 'rgba(248,113,113,0.2)',
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>Q{qi + 1}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                        {ans?.marks_awarded ?? 0}/{q.marks} marks
                      </span>
                      {isCorrect
                        ? <CheckCircle size={16} color="var(--success)" />
                        : <XCircle size={16} color="var(--error)" />}
                    </div>
                  </div>

                  <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem', marginBottom: '14px', lineHeight: 1.5 }}>
                    {q.text}
                  </p>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {q.options.map((opt, oi) => {
                      const isSelected = selected === opt
                      const isCorrectOpt = q.correct_answer === opt

                      let bg = 'var(--bg-elevated)'
                      let border = 'var(--border-subtle)'
                      let color = 'var(--text-secondary)'

                      if (isCorrectOpt) { bg = 'var(--success-dim)'; border = 'rgba(52,211,153,0.3)'; color = 'var(--success)' }
                      if (isSelected && !isCorrect) { bg = 'var(--error-dim)'; border = 'rgba(248,113,113,0.3)'; color = 'var(--error)' }

                      return (
                        <div key={oi} style={{
                          display: 'flex', alignItems: 'center', gap: '10px',
                          padding: '9px 13px', borderRadius: 'var(--radius-md)',
                          background: bg, border: `1px solid ${border}`, color,
                          fontSize: '0.875rem',
                        }}>
                          <span style={{
                            width: 22, height: 22, borderRadius: '50%', flexShrink: 0,
                            border: `1.5px solid ${border}`,
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '0.7rem', fontWeight: 600,
                          }}>
                            {String.fromCharCode(65 + oi)}
                          </span>
                          <span style={{ flex: 1 }}>{opt}</span>
                          {isSelected && <span style={{ fontSize: '0.75rem', fontWeight: 500 }}>Your answer</span>}
                          {isCorrectOpt && <CheckCircle size={14} />}
                        </div>
                      )
                    })}
                  </div>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}
