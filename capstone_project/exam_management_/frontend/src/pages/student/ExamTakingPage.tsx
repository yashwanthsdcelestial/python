import React, { useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, ChevronLeft, ChevronRight, Send, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'
import { examApi, attemptApi } from '@/api/services'
import { useFetch, useCountdown } from '@/hooks'
import { Button, PageLoader, Badge } from '@/components/shared/UI'
import StarBorder from '@/components/shared/StarBorder'
import type { AttemptStart, AttemptResult } from '@/types'
import toast from 'react-hot-toast'

// ─── Result Screen ────────────────────────────────────────────────────────────
const ResultScreen: React.FC<{ result: AttemptResult; onBack: () => void }> = ({ result, onBack }) => {
  const pct = result.percentage ?? 0

  return (
    <div style={{ maxWidth: '560px', margin: '0 auto', textAlign: 'center', padding: '48px 24px' }}>
      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }}>
        <div style={{
          width: 100, height: 100, borderRadius: '50%', margin: '0 auto 24px',
          background: result.passed ? 'var(--success-dim)' : 'var(--error-dim)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          border: `2px solid ${result.passed ? 'var(--success)' : 'var(--error)'}`,
          boxShadow: result.passed ? '0 0 40px rgba(52,211,153,0.25)' : '0 0 40px rgba(248,113,113,0.2)',
        }}>
          {result.passed
            ? <CheckCircle size={48} color="var(--success)" />
            : <XCircle size={48} color="var(--error)" />}
        </div>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2.2rem', color: result.passed ? 'var(--success)' : 'var(--error)', marginBottom: '8px' }}>
          {result.passed ? 'Congratulations!' : 'Keep Trying'}
        </h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>
          {result.passed ? 'You passed the exam.' : "You didn't meet the passing threshold."}
        </p>

        {/* Score gauge */}
        <div style={{
          background: 'var(--bg-card)', border: '1px solid var(--border-default)',
          borderRadius: 'var(--radius-xl)', padding: '28px', marginBottom: '24px',
        }}>
          {/* Arc meter */}
          <div style={{ position: 'relative', width: '160px', height: '160px', margin: '0 auto 20px' }}>
            <svg viewBox="0 0 160 160" style={{ transform: 'rotate(-90deg)' }}>
              <circle cx="80" cy="80" r="64" fill="none" stroke="var(--bg-elevated)" strokeWidth="12" />
              <motion.circle cx="80" cy="80" r="64" fill="none"
                stroke={result.passed ? 'var(--success)' : 'var(--error)'}
                strokeWidth="12" strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 64}`}
                initial={{ strokeDashoffset: 2 * Math.PI * 64 }}
                animate={{ strokeDashoffset: 2 * Math.PI * 64 * (1 - pct / 100) }}
                transition={{ duration: 1.2, delay: 0.4, ease: 'easeOut' }}
              />
            </svg>
            <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                style={{ fontFamily: 'var(--font-mono)', fontSize: '2rem', fontWeight: 500, color: 'var(--text-primary)', lineHeight: 1 }}
              >
                {pct.toFixed(1)}%
              </motion.span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>score</span>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
            {[
              { label: 'Score', value: `${result.score ?? 0}/${result.total_marks}` },
              { label: 'Status', value: result.passed ? 'PASSED' : 'FAILED' },
              { label: 'Time', value: result.time_taken_seconds ? `${Math.floor(result.time_taken_seconds / 60)}m ${result.time_taken_seconds % 60}s` : '—' },
            ].map(({ label, value }) => (
              <div key={label} style={{ background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', padding: '12px' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>{label}</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--text-primary)', fontWeight: 500 }}>{value}</div>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <Button variant="ghost" onClick={onBack} icon={<ChevronLeft size={16} />}>Back to Exams</Button>
          <StarBorder as="button" color="var(--gold)" speed="5s" thickness={2} onClick={() => window.location.href = '/student/results'} style={{ minWidth: 160 }}>
            View All Results
          </StarBorder>
        </div>
      </motion.div>
    </div>
  )
}

// ─── Exam Taking Page ─────────────────────────────────────────────────────────
export const ExamTakingPage: React.FC = () => {
  const { examId } = useParams<{ examId: string }>()
  const navigate = useNavigate()
  const [attempt, setAttempt] = useState<AttemptStart | null>(null)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [currentQ, setCurrentQ] = useState(0)
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [started, setStarted] = useState(false)
  const [starting, setStarting] = useState(false)

  const { data: exam, loading: loadingExam } = useFetch(
    () => examApi.get(Number(examId)),
    [examId]
  )

  const timer = useCountdown(attempt?.started_at ?? null, attempt?.duration_minutes ?? 60)

  // Auto-submit on timeout
  const handleSubmit = useCallback(async (auto = false) => {
    if (!attempt) return
    if (!auto && !confirm('Submit exam? You cannot change answers after submitting.')) return
    setSubmitting(true)
    try {
      const payload = Object.entries(answers).map(([qid, sel]) => ({
        question_id: Number(qid),
        selected_answer: sel,
      }))
      const res = await attemptApi.submit(attempt.id, payload)
      setResult(res)
      if (auto) toast.error('Time up! Exam auto-submitted.')
      else toast.success('Exam submitted!')
    } catch (err: unknown) {
      toast.error((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Submit failed')
    } finally {
      setSubmitting(false)
    }
  }, [attempt, answers])

  // Watch for timer expiry
  React.useEffect(() => {
    if (timer.isExpired && attempt && !result && !submitting) {
      handleSubmit(true)
    }
  }, [timer.isExpired, attempt, result, submitting, handleSubmit])

  const handleStart = async () => {
    setStarting(true)
    try {
      const att = await attemptApi.start(Number(examId))
      setAttempt(att)
      setStarted(true)
    } catch (err: unknown) {
      toast.error((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Could not start exam')
    } finally {
      setStarting(false)
    }
  }

  if (loadingExam) return <PageLoader />

  // ── Result screen ──────────────────────────────────────────────────────────
  if (result) return <ResultScreen result={result} onBack={() => navigate('/student/my-exams')} />

  // ── Pre-start screen ───────────────────────────────────────────────────────
  if (!started || !attempt) {
    return (
      <div style={{ maxWidth: '560px', margin: '0 auto', padding: '48px 24px' }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-default)',
            borderRadius: 'var(--radius-xl)', padding: '36px', textAlign: 'center',
          }}>
            <div style={{
              width: 72, height: 72, borderRadius: '50%', background: 'var(--gold-dim)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px',
              border: '1px solid rgba(201,168,76,0.3)',
            }}>
              <Clock size={32} color="var(--gold)" />
            </div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.75rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
              {exam?.title}
            </h1>
            {exam?.description && (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '24px' }}>{exam.description}</p>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '28px' }}>
              {[
                { label: 'Duration', value: `${exam?.duration_minutes} minutes` },
                { label: 'Questions', value: `${exam?.question_count}` },
                { label: 'Total Marks', value: `${exam?.total_marks}` },
                { label: 'Pass Mark', value: `${exam?.pass_percentage}%` },
                { label: 'Max Attempts', value: `${exam?.max_attempts}` },
              ].map(({ label, value }) => (
                <div key={label} style={{ background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', padding: '12px' }}>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>{label}</div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.95rem', color: 'var(--text-primary)' }}>{value}</div>
                </div>
              ))}
            </div>

            <div style={{ background: 'var(--warning-dim)', border: '1px solid rgba(251,191,36,0.2)', borderRadius: 'var(--radius-md)', padding: '12px 14px', marginBottom: '24px', textAlign: 'left' }}>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
                <AlertTriangle size={16} style={{ color: 'var(--warning)', flexShrink: 0, marginTop: '2px' }} />
                <p style={{ fontSize: '0.83rem', color: 'var(--warning)', lineHeight: 1.5 }}>
                  Once started, the timer cannot be paused. Ensure you have a stable connection before beginning.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <Button variant="ghost" onClick={() => navigate('/student/my-exams')}>Cancel</Button>
              <StarBorder
                as="button"
                color="var(--gold)"
                speed="4s"
                thickness={2}
                disabled={starting}
                onClick={handleStart}
                style={{ minWidth: 140 }}
              >
                {starting ? 'Starting...' : 'Begin Exam'}
              </StarBorder>
            </div>
          </div>
        </motion.div>
      </div>
    )
  }

  // ── Active exam ────────────────────────────────────────────────────────────
  const questions = attempt.questions
  const q = questions[currentQ]
  const answered = Object.keys(answers).length
  const total = questions.length

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      {/* Timer Bar */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        style={{
          position: 'sticky', top: 0, zIndex: 20, background: 'var(--bg-surface)',
          borderBottom: '1px solid var(--border-subtle)', padding: '12px 0', marginBottom: '24px',
        }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{exam?.title}</span>
            <Badge variant="default">{answered}/{total} answered</Badge>
          </div>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            fontFamily: 'var(--font-mono)', fontSize: '1.25rem', fontWeight: 500,
            color: timer.isDanger ? 'var(--error)' : timer.isWarning ? 'var(--warning)' : 'var(--text-primary)',
          }}>
            <motion.div
              animate={timer.isDanger ? { scale: [1, 1.1, 1] } : {}}
              transition={{ repeat: Infinity, duration: 0.8 }}
            >
              <Clock size={18} style={{ color: timer.isDanger ? 'var(--error)' : timer.isWarning ? 'var(--warning)' : 'var(--gold)' }} />
            </motion.div>
            {timer.display}
          </div>
        </div>
        {/* Progress bar */}
        <div style={{ marginTop: '10px', height: '3px', background: 'var(--bg-elevated)', borderRadius: '2px', overflow: 'hidden' }}>
          <motion.div
            style={{ height: '100%', background: timer.isDanger ? 'var(--error)' : timer.isWarning ? 'var(--warning)' : 'var(--gold)', borderRadius: '2px' }}
            animate={{ width: `${timer.percentage}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </motion.div>

      {/* Question Navigation dots */}
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '20px' }}>
        {questions.map((_, qi) => (
          <motion.button
            key={qi}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setCurrentQ(qi)}
            style={{
              width: 32, height: 32, borderRadius: '50%', border: 'none', cursor: 'pointer',
              fontFamily: 'var(--font-mono)', fontSize: '0.75rem', fontWeight: 500,
              background: qi === currentQ
                ? 'var(--gold)'
                : answers[questions[qi].id]
                  ? 'var(--success-dim)'
                  : 'var(--bg-elevated)',
              color: qi === currentQ
                ? 'var(--bg-void)'
                : answers[questions[qi].id]
                  ? 'var(--success)'
                  : 'var(--text-muted)',
              border: `1px solid ${qi === currentQ ? 'var(--gold)' : answers[questions[qi].id] ? 'rgba(52,211,153,0.3)' : 'var(--border-subtle)'}`,
              transition: 'all 0.15s',
            }}>
            {qi + 1}
          </motion.button>
        ))}
      </div>

      {/* Question card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentQ}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
          style={{
            background: 'var(--bg-card)', border: '1px solid var(--border-default)',
            borderRadius: 'var(--radius-xl)', padding: '28px', marginBottom: '20px',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--gold)', fontFamily: 'var(--font-mono)', fontWeight: 500 }}>
              Question {currentQ + 1} of {total}
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              {q.marks} mark{q.marks !== 1 ? 's' : ''}
            </span>
          </div>

          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--text-primary)', lineHeight: 1.5, marginBottom: '24px' }}>
            {q.text}
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {q.options.map((opt, oi) => {
              const isSelected = answers[q.id] === opt
              return (
                <motion.button
                  key={oi}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.99 }}
                  onClick={() => setAnswers(prev => ({ ...prev, [q.id]: opt }))}
                  style={{
                    display: 'flex', alignItems: 'center', gap: '12px',
                    padding: '14px 18px', borderRadius: 'var(--radius-md)',
                    border: `1px solid ${isSelected ? 'var(--gold)' : 'var(--border-default)'}`,
                    background: isSelected ? 'var(--gold-dim)' : 'var(--bg-elevated)',
                    color: isSelected ? 'var(--gold)' : 'var(--text-primary)',
                    textAlign: 'left', cursor: 'pointer', fontFamily: 'var(--font-body)',
                    fontSize: '0.95rem', transition: 'all 0.15s',
                  }}>
                  <span style={{
                    width: 26, height: 26, borderRadius: '50%', flexShrink: 0,
                    border: `1.5px solid ${isSelected ? 'var(--gold)' : 'var(--border-strong)'}`,
                    background: isSelected ? 'var(--gold)' : 'transparent',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '0.75rem', fontWeight: 600,
                    color: isSelected ? 'var(--bg-void)' : 'var(--text-muted)',
                  }}>
                    {String.fromCharCode(65 + oi)}
                  </span>
                  {opt}
                </motion.button>
              )
            })}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button variant="ghost" icon={<ChevronLeft size={16} />} disabled={currentQ === 0}
          onClick={() => setCurrentQ(q => q - 1)}>
          Previous
        </Button>

        <div style={{ display: 'flex', gap: '10px' }}>
          {currentQ < total - 1 ? (
            <Button variant="primary" onClick={() => setCurrentQ(q => q + 1)}>
              Next <ChevronRight size={16} />
            </Button>
          ) : (
            <StarBorder
              as="button"
              color="var(--gold)"
              speed="4s"
              thickness={2}
              disabled={submitting}
              onClick={() => handleSubmit(false)}
              style={{ minWidth: 180 }}
            >
              <Send size={14} /> {submitting ? 'Submitting...' : `Submit Exam (${answered}/${total})`}
            </StarBorder>
          )}
        </div>
      </div>
    </div>
  )
}
