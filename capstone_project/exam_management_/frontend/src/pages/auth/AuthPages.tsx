import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff, Mail, Lock, User, GraduationCap, ChevronRight, Clock, BookOpen, Award } from 'lucide-react'
import { useAuth } from '@/hooks'
import { useAuthStore } from '@/store/authStore'
import { Input } from '@/components/shared/UI'
import CardSwap, { Card } from '@/components/shared/CardSwap'
import FloatingLines from '@/components/shared/FloatingLines'
import StarBorder from '@/components/shared/StarBorder'
import toast from 'react-hot-toast'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
})

const registerSchema = z.object({
  full_name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  role: z.enum(['student', 'admin']),
})

type LoginForm = z.infer<typeof loginSchema>
type RegisterForm = z.infer<typeof registerSchema>

const AuthBackground = () => (
  <div style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none' }}>
    {/* Dark base */}
    <div style={{ position: 'absolute', inset: 0, background: 'var(--bg-void)' }} />
    {/* FloatingLines — gold + accent gradient matching project theme */}
    <div style={{ position: 'absolute', inset: 0, opacity: 0.85 }}>
      <FloatingLines
        linesGradient={['#080b12', '#1a1200', '#c9a84c', '#e8c97a', '#4f8ef7', '#c9a84c', '#1a1200', '#080b12']}
        enabledWaves={['top', 'middle', 'bottom']}
        lineCount={[6, 10, 8]}
        lineDistance={[8, 6, 5]}
        bendRadius={4.0}
        bendStrength={-0.6}
        animationSpeed={0.6}
        interactive={true}
        parallax={true}
        parallaxStrength={0.15}
        mixBlendMode="screen"
        bottomWavePosition={{ x: 2.0, y: -0.7, rotate: -1 }}
      />
    </div>
    {/* Subtle vignette overlay to keep text readable */}
    <div style={{
      position: 'absolute', inset: 0,
      background: 'radial-gradient(ellipse at center, transparent 30%, rgba(8,11,18,0.7) 100%)',
    }} />
  </div>
)

const PreviewCards = () => (
  <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
    <CardSwap cardDistance={45} verticalDistance={55} delay={3500} pauseOnHover width={300} height={180}>
      <Card style={{ background: 'linear-gradient(135deg, #1a2236 0%, #0d1117 100%)', border: '1px solid rgba(201,168,76,0.3)', borderRadius: '16px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(201,168,76,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Clock size={18} color="#c9a84c" />
          </div>
          <span style={{ fontFamily: 'DM Serif Display, serif', fontSize: '1rem', color: '#f0ede6' }}>Timed Exams</span>
        </div>
        <p style={{ fontSize: '0.82rem', color: '#9aa3b3', lineHeight: 1.5 }}>Auto-submit with live countdown. Never lose your progress.</p>
        <div style={{ display: 'flex', gap: '6px' }}>
          {['30 min', '60 min', '90 min'].map(t => (
            <span key={t} style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: '100px', background: 'rgba(201,168,76,0.1)', color: '#c9a84c', border: '1px solid rgba(201,168,76,0.2)' }}>{t}</span>
          ))}
        </div>
      </Card>

      <Card style={{ background: 'linear-gradient(135deg, #1a2236 0%, #0d1117 100%)', border: '1px solid rgba(79,142,247,0.3)', borderRadius: '16px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(79,142,247,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Award size={18} color="#4f8ef7" />
          </div>
          <span style={{ fontFamily: 'DM Serif Display, serif', fontSize: '1rem', color: '#f0ede6' }}>Smart Scoring</span>
        </div>
        <p style={{ fontSize: '0.82rem', color: '#9aa3b3', lineHeight: 1.5 }}>Instant results with detailed answer review and pass/fail analysis.</p>
        <div style={{ height: '6px', background: '#1a2236', borderRadius: '3px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: '78%', background: 'linear-gradient(90deg, #4f8ef7, #818cf8)', borderRadius: '3px' }} />
        </div>
        <span style={{ fontSize: '0.7rem', color: '#5a6478' }}>Average pass rate: 78%</span>
      </Card>

      <Card style={{ background: 'linear-gradient(135deg, #1a2236 0%, #0d1117 100%)', border: '1px solid rgba(52,211,153,0.3)', borderRadius: '16px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(52,211,153,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <BookOpen size={18} color="#34d399" />
          </div>
          <span style={{ fontFamily: 'DM Serif Display, serif', fontSize: '1rem', color: '#f0ede6' }}>Question Bank</span>
        </div>
        <p style={{ fontSize: '0.82rem', color: '#9aa3b3', lineHeight: 1.5 }}>Create rich multi-choice exams with custom marks per question.</p>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          {[['Questions', '10+'], ['Marks', 'Custom'], ['Attempts', 'Limited']].map(([l, v]) => (
            <div key={l} style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.85rem', color: '#34d399', fontWeight: 500 }}>{v}</div>
              <div style={{ fontSize: '0.65rem', color: '#5a6478' }}>{l}</div>
            </div>
          ))}
        </div>
      </Card>
    </CardSwap>
  </div>
)

const AuthLayout: React.FC<{ children: React.ReactNode; title: string; subtitle: string }> = ({ children, title, subtitle }) => (
  <div style={{ minHeight: '100vh', display: 'flex', position: 'relative' }}>
    <AuthBackground />
    <div style={{ flex: '0 0 auto', width: '100%', maxWidth: '480px', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '32px 24px', position: 'relative', zIndex: 1, borderRight: '1px solid rgba(255,255,255,0.06)' }}>
      <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }} style={{ width: '100%', maxWidth: '400px' }}>
        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.1, type: 'spring', stiffness: 400 }}
          style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '36px' }}>
          <div style={{ width: 44, height: 44, background: 'linear-gradient(135deg, #c9a84c, #e8c97a)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 24px rgba(201,168,76,0.2)' }}>
            <GraduationCap size={24} color="#080b12" />
          </div>
          <span style={{ fontFamily: 'DM Serif Display, serif', fontSize: '1.5rem', color: '#f0ede6' }}>ExamPortal</span>
        </motion.div>
        <div style={{ background: '#1e2a3a', border: '1px solid rgba(255,255,255,0.12)', borderRadius: '24px', padding: '32px', boxShadow: '0 24px 80px rgba(0,0,0,0.5)' }}>
          <div style={{ marginBottom: '24px' }}>
            <h1 style={{ fontFamily: 'DM Serif Display, serif', fontSize: '1.75rem', color: '#f0ede6', marginBottom: '6px' }}>{title}</h1>
            <p style={{ color: '#5a6478', fontSize: '0.9rem' }}>{subtitle}</p>
          </div>
          {children}
        </div>
      </motion.div>
    </div>

    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px', position: 'relative', zIndex: 1, gap: '20px' }} className="auth-right-panel">

      {/* Heading */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.6 }} style={{ textAlign: 'center' }}>
        <h2 style={{ fontFamily: 'DM Serif Display, serif', fontSize: '2rem', color: '#f0ede6', marginBottom: '8px' }}>
          Everything you need to <span style={{ color: '#c9a84c', fontStyle: 'italic' }}>excel</span>
        </h2>
        <p style={{ color: '#5a6478', fontSize: '0.9rem', maxWidth: '340px', margin: '0 auto' }}>
          A complete exam platform with timed attempts, instant scoring, and detailed analytics.
        </p>
      </motion.div>

      {/* Stats above cards — no overlap */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}
        style={{ display: 'flex', gap: '40px' }}>
        {[['Exams', '50+'], ['Students', '200+'], ['Questions', '500+']].map(([label, value]) => (
          <div key={label} style={{ textAlign: 'center' }}>
            <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '1.4rem', fontWeight: 500, color: '#c9a84c' }}>{value}</div>
            <div style={{ fontSize: '0.7rem', color: '#5a6478', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: '2px' }}>{label}</div>
          </div>
        ))}
      </motion.div>

      {/* CardSwap below stats */}
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.6, duration: 0.6 }}
        style={{ width: '100%', maxWidth: '460px', height: '260px', flexShrink: 0 }}>
        <PreviewCards />
      </motion.div>

    </div>
    <style>{`@media (max-width: 768px) { .auth-right-panel { display: none !important; } }`}</style>
  </div>
)

export const LoginPage: React.FC = () => {
  const { login, isLoading } = useAuth()
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) })

  const onSubmit = async (data: LoginForm) => {
    try {
      await login(data.email, data.password)
      toast.success('Welcome back!')
      const { user } = useAuthStore.getState()
      navigate(user?.role === 'admin' ? '/admin' : '/student', { replace: true })
    } catch (err: unknown) {
      toast.error((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <AuthLayout title="Welcome back" subtitle="Sign in to your exam portal account">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
        <Input label="Email address" type="email" placeholder="you@example.com" icon={<Mail size={16} />} error={errors.email?.message} {...register('email')} />
        <Input label="Password" type={showPassword ? 'text' : 'password'} placeholder="Your password" icon={<Lock size={16} />} error={errors.password?.message}
          rightIcon={<span onClick={() => setShowPassword(p => !p)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</span>}
          {...register('password')} />
        <div style={{ background: '#111827', borderRadius: '10px', padding: '12px', fontSize: '0.8rem', color: '#5a6478' }}>
          <div style={{ marginBottom: '4px', color: '#c9a84c', fontWeight: 500 }}>Demo credentials</div>
          <div>Admin: <span style={{ fontFamily: 'JetBrains Mono, monospace', color: '#9aa3b3' }}>admin@examportal.com / Admin@1234</span></div>
          <div>Student: <span style={{ fontFamily: 'JetBrains Mono, monospace', color: '#9aa3b3' }}>student1@example.com / Student@1234</span></div>
        </div>
        <StarBorder
          as="button"
          type="submit"
          color="#c9a84c"
          speed="4s"
          thickness={2}
          disabled={isLoading}
          style={{ marginTop: '4px' }}
        >
          {isLoading ? 'Signing in...' : <><span>Sign In</span><ChevronRight size={16} /></>}
        </StarBorder>
      </form>
      <p style={{ textAlign: 'center', marginTop: '20px', color: '#5a6478', fontSize: '0.875rem' }}>
        No account?{' '}<Link to="/register" style={{ color: '#c9a84c', fontWeight: 500 }}>Create one</Link>
      </p>
    </AuthLayout>
  )
}

export const RegisterPage: React.FC = () => {
  const { register: registerUser, isLoading } = useAuth()
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const { register, handleSubmit, formState: { errors }, watch } = useForm<RegisterForm>({ resolver: zodResolver(registerSchema), defaultValues: { role: 'student' } })
  const role = watch('role')

  const onSubmit = async (data: RegisterForm) => {
    try {
      await registerUser(data)
      toast.success('Account created! Welcome.')
      const { user } = useAuthStore.getState()
      navigate(user?.role === 'admin' ? '/admin' : '/student', { replace: true })
    } catch (err: unknown) {
      toast.error((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <AuthLayout title="Create account" subtitle="Join ExamPortal to get started">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <Input label="Full name" placeholder="Your full name" icon={<User size={16} />} error={errors.full_name?.message} {...register('full_name')} />
        <Input label="Email address" type="email" placeholder="you@example.com" icon={<Mail size={16} />} error={errors.email?.message} {...register('email')} />
        <Input label="Password" type={showPassword ? 'text' : 'password'} placeholder="Min. 8 characters" icon={<Lock size={16} />} error={errors.password?.message}
          rightIcon={<span onClick={() => setShowPassword(p => !p)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</span>}
          {...register('password')} />
        <div>
          <label style={{ fontSize: '0.8125rem', color: '#9aa3b3', fontWeight: 500, display: 'block', marginBottom: '8px' }}>Role</label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            {(['student', 'admin'] as const).map((r) => (
              <label key={r} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 14px', border: `1px solid ${role === r ? '#c9a84c' : 'rgba(255,255,255,0.12)'}`, borderRadius: '10px', cursor: 'pointer', background: role === r ? 'rgba(201,168,76,0.15)' : '#111827', transition: 'all 0.15s' }}>
                <input type="radio" value={r} {...register('role')} style={{ accentColor: '#c9a84c' }} />
                <span style={{ fontSize: '0.875rem', color: role === r ? '#c9a84c' : '#9aa3b3', textTransform: 'capitalize' }}>{r}</span>
              </label>
            ))}
          </div>
        </div>
        <StarBorder
          as="button"
          type="submit"
          color="#c9a84c"
          speed="4s"
          thickness={2}
          disabled={isLoading}
          style={{ marginTop: '4px' }}
        >
          {isLoading ? 'Creating...' : <><span>Create Account</span><ChevronRight size={16} /></>}
        </StarBorder>
      </form>
      <p style={{ textAlign: 'center', marginTop: '20px', color: '#5a6478', fontSize: '0.875rem' }}>
        Have an account?{' '}<Link to="/login" style={{ color: '#c9a84c', fontWeight: 500 }}>Sign in</Link>
      </p>
    </AuthLayout>
  )
}