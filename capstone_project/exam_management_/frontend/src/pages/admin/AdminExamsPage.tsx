import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Plus, Search, Edit2, Trash2, Eye, BookOpen, Clock, Target } from 'lucide-react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { examApi } from '@/api/services'
import { useFetch, useDebounce } from '@/hooks'
import { Button, Card, Badge, Modal, Input, EmptyState, PageLoader } from '@/components/shared/UI'
import StarBorder from '@/components/shared/StarBorder'
import type { Exam } from '@/types'
import toast from 'react-hot-toast'

const statusBadge = (s: string) => {
  if (s === 'published') return <Badge variant="success">Published</Badge>
  if (s === 'archived') return <Badge variant="default">Archived</Badge>
  return <Badge variant="warning">Draft</Badge>
}

const questionSchema = z.object({
  text: z.string().min(5, 'Question too short'),
  options: z.array(z.string().min(1)).min(2).max(6),
  correct_answer: z.string().min(1),
  marks: z.coerce.number().min(1),
})

const examSchema = z.object({
  title: z.string().min(3),
  description: z.string().optional(),
  duration_minutes: z.coerce.number().min(5).max(360),
  pass_percentage: z.coerce.number().min(1).max(100),
  max_attempts: z.coerce.number().min(1).max(10),
  questions: z.array(questionSchema).min(1, 'At least one question required'),
})
type ExamForm = z.infer<typeof examSchema>

// ─── Create Exam Modal ────────────────────────────────────────────────────────
const CreateExamModal: React.FC<{ open: boolean; onClose: () => void; onCreated: () => void }> = ({ open, onClose, onCreated }) => {
  const [submitting, setSubmitting] = useState(false)
  const { register, control, handleSubmit, formState: { errors }, watch, reset } = useForm<ExamForm>({
    resolver: zodResolver(examSchema),
    defaultValues: {
      duration_minutes: 60, pass_percentage: 60, max_attempts: 1,
      questions: [{ text: '', options: ['', '', '', ''], correct_answer: '', marks: 5 }],
    },
  })
  const { fields, append, remove } = useFieldArray({ control, name: 'questions' })

  const onSubmit = async (data: ExamForm) => {
    setSubmitting(true)
    try {
      await examApi.create(data)
      toast.success('Exam created!')
      reset()
      onCreated()
      onClose()
    } catch (err: unknown) {
      toast.error((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to create exam')
    } finally { setSubmitting(false) }
  }

  return (
    <Modal open={open} onClose={onClose} title="Create New Exam" size="lg">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
          <div style={{ gridColumn: '1/-1' }}>
            <Input label="Exam Title" placeholder="e.g. Python Fundamentals" error={errors.title?.message} {...register('title')} />
          </div>
          <div style={{ gridColumn: '1/-1' }}>
            <Input label="Description (optional)" placeholder="Brief description" {...register('description')} />
          </div>
          <Input label="Duration (min)" type="number" error={errors.duration_minutes?.message} {...register('duration_minutes')} />
          <Input label="Pass % threshold" type="number" error={errors.pass_percentage?.message} {...register('pass_percentage')} />
          <Input label="Max attempts" type="number" {...register('max_attempts')} />
        </div>

        <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '16px', marginBottom: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h3 style={{ fontFamily: 'var(--font-display)', color: 'var(--text-primary)' }}>Questions ({fields.length})</h3>
            <Button type="button" variant="ghost" size="sm" icon={<Plus size={14} />}
              onClick={() => append({ text: '', options: ['', '', '', ''], correct_answer: '', marks: 5 })}>
              Add Question
            </Button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxHeight: '360px', overflowY: 'auto', paddingRight: '4px' }}>
            {fields.map((field, qi) => {
              const qErrors = errors.questions?.[qi]
              return (
                <motion.div key={field.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                  style={{ background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', padding: '14px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--gold)', fontFamily: 'var(--font-mono)' }}>Q{qi + 1}</span>
                    {fields.length > 1 && (
                      <button type="button" onClick={() => remove(qi)}
                        style={{ background: 'none', border: 'none', color: 'var(--error)', cursor: 'pointer', padding: '2px' }}>
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                  <Input placeholder="Question text" error={qErrors?.text?.message} style={{ marginBottom: '10px' }} {...register(`questions.${qi}.text`)} />
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', marginBottom: '10px' }}>
                    {[0, 1, 2, 3].map(oi => (
                      <Input key={oi} placeholder={`Option ${oi + 1}`} {...register(`questions.${qi}.options.${oi}`)} />
                    ))}
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '10px' }}>
                    <div>
                      <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Correct answer</label>
                      <select {...register(`questions.${qi}.correct_answer`)}
                        style={{ width: '100%', background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', padding: '8px 10px', fontSize: '0.875rem' }}>
                        <option value="">Select...</option>
                        {watch(`questions.${qi}.options`)?.filter(Boolean).map((opt, i) => (
                          <option key={i} value={opt}>{opt}</option>
                        ))}
                      </select>
                      {qErrors?.correct_answer && <span style={{ fontSize: '0.75rem', color: 'var(--error)' }}>{qErrors.correct_answer.message}</span>}
                    </div>
                    <Input label="Marks" type="number" {...register(`questions.${qi}.marks`)} />
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-subtle)' }}>
          <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="gold" loading={submitting}>Create Exam</Button>
        </div>
      </form>
    </Modal>
  )
}

// ─── Admin Exams Page ─────────────────────────────────────────────────────────
export const AdminExamsPage: React.FC = () => {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [createOpen, setCreateOpen] = useState(false)
  const [page, setPage] = useState(1)
  const debouncedSearch = useDebounce(search)

  const { data, loading, refetch } = useFetch(
    () => examApi.list({ page, page_size: 10, search: debouncedSearch || undefined }),
    [page, debouncedSearch]
  )

  const handlePublish = async (exam: Exam) => {
    try {
      await examApi.update(exam.id, { status: exam.status === 'published' ? 'draft' : 'published' })
      toast.success(`Exam ${exam.status === 'published' ? 'unpublished' : 'published'}`)
      refetch()
    } catch { toast.error('Failed to update exam') }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this exam?')) return
    try {
      await examApi.delete(id)
      toast.success('Exam deleted')
      refetch()
    } catch { toast.error('Failed to delete') }
  }

  return (
    <div style={{ maxWidth: '1100px' }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '28px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '4px' }}>Exams</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{data?.total ?? 0} total exams</p>
        </div>
        <StarBorder as="button" color="var(--gold)" speed="5s" thickness={2} onClick={() => setCreateOpen(true)} style={{ minWidth: 140 }}>
          <Plus size={15} /> Create Exam
        </StarBorder>
      </motion.div>

      {/* Search */}
      <div style={{ marginBottom: '20px' }}>
        <Input placeholder="Search exams..." icon={<Search size={16} />} value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} style={{ maxWidth: '360px' }} />
      </div>

      {/* Exam cards */}
      {loading ? <PageLoader /> : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {data?.items.length === 0 ? (
            <EmptyState icon={<BookOpen size={40} />} title="No exams yet" description="Create your first exam to get started"
              action={<Button variant="gold" icon={<Plus size={14} />} onClick={() => setCreateOpen(true)}>Create Exam</Button>} />
          ) : data?.items.map((exam, i) => (
            <motion.div key={exam.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
              <Card hover>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px', flexWrap: 'wrap' }}>
                      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)' }}>{exam.title}</h3>
                      {statusBadge(exam.status)}
                    </div>
                    {exam.description && <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '10px' }}>{exam.description}</p>}
                    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        <Clock size={13} /> {exam.duration_minutes}m
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        <BookOpen size={13} /> {exam.question_count} Qs
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        <Target size={13} /> Pass: {exam.pass_percentage}%
                      </span>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '8px', flexShrink: 0 }}>
                    <Button variant="ghost" size="sm" icon={<Eye size={14} />}
                      onClick={() => navigate(`/admin/exams/${exam.id}`)}>Results</Button>
                    <Button variant={exam.status === 'published' ? 'outline' : 'primary'} size="sm" icon={<Edit2 size={14} />}
                      onClick={() => handlePublish(exam)}>
                      {exam.status === 'published' ? 'Unpublish' : 'Publish'}
                    </Button>
                    <Button variant="danger" size="sm" icon={<Trash2 size={14} />} onClick={() => handleDelete(exam.id)}>Delete</Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {data && data.total > 10 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '24px' }}>
          <Button variant="ghost" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</Button>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', alignSelf: 'center' }}>
            {page} / {Math.ceil(data.total / 10)}
          </span>
          <Button variant="ghost" size="sm" disabled={page >= Math.ceil(data.total / 10)} onClick={() => setPage(p => p + 1)}>Next</Button>
        </div>
      )}

      <CreateExamModal open={createOpen} onClose={() => setCreateOpen(false)} onCreated={refetch} />
    </div>
  )
}
