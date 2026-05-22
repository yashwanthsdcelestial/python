import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Loader2 } from 'lucide-react'
import { clsx } from 'clsx'
import StarBorder from './StarBorder'

// ─── Button ───────────────────────────────────────────────────────────────────
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'gold' | 'ghost' | 'danger' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
}

const BUTTON_VARIANT_STYLES: Record<string, React.CSSProperties> = {
  primary: {
    background: 'var(--accent)',
    color: '#fff',
    border: 'none',
    boxShadow: '0 0 20px rgba(79,142,247,0.25)',
  },
  gold: {
    background: 'linear-gradient(135deg, var(--gold), var(--gold-light))',
    color: 'var(--bg-void)',
    border: 'none',
    boxShadow: '0 0 20px rgba(201,168,76,0.3)',
  },
  ghost: {
    background: 'transparent',
    color: 'var(--text-secondary)',
    border: '1px solid var(--border-subtle)',
  },
  danger: {
    background: 'rgba(248,113,113,0.1)',
    color: 'var(--error)',
    border: '1px solid rgba(248,113,113,0.2)',
  },
  outline: {
    background: 'transparent',
    color: 'var(--text-primary)',
    border: '1px solid var(--border-default)',
  },
}

const BUTTON_SIZE_STYLES: Record<string, React.CSSProperties> = {
  sm: { padding: '6px 12px', fontSize: '0.8125rem' },
  md: { padding: '10px 16px', fontSize: '0.875rem' },
  lg: { padding: '12px 24px', fontSize: '1rem' },
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary', size = 'md', loading, icon, children, className, disabled, style, ...props
}) => {
  return (
    <button
      className={clsx(className)}
      disabled={disabled || loading}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '6px',
        fontWeight: 500,
        borderRadius: 'var(--radius-md)',
        cursor: (disabled || loading) ? 'not-allowed' : 'pointer',
        opacity: (disabled || loading) ? 0.5 : 1,
        transition: 'filter 0.15s, opacity 0.15s, transform 0.1s',
        fontFamily: 'var(--font-body)',
        whiteSpace: 'nowrap',
        userSelect: 'none',
        ...BUTTON_VARIANT_STYLES[variant],
        ...BUTTON_SIZE_STYLES[size],
        ...style,
      }}
      onMouseEnter={(e) => {
        if (!disabled && !loading) e.currentTarget.style.filter = 'brightness(1.12)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.filter = 'brightness(1)'
        e.currentTarget.style.transform = 'scale(1)'
      }}
      onMouseDown={(e) => { e.currentTarget.style.transform = 'scale(0.97)' }}
      onMouseUp={(e) => { e.currentTarget.style.transform = 'scale(1)' }}
      {...props}
    >
      {loading ? <Loader2 size={16} style={{ animation: 'spin 1s linear infinite' }} /> : icon}
      {children}
    </button>
  )
}

// ─── Input ────────────────────────────────────────────────────────────────────
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  icon?: React.ReactNode
  rightIcon?: React.ReactNode
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, icon, rightIcon, className, style, ...props }, ref) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
      {label && (
        <label style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
          {label}
        </label>
      )}
      <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
        {icon && (
          <span style={{
            position: 'absolute',
            left: '12px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--gold)',
            pointerEvents: 'none',
            display: 'flex',
            alignItems: 'center',
            opacity: 0.75,
            zIndex: 1,
          }}>
            {icon}
          </span>
        )}
        <input
          ref={ref}
          className={clsx('theme-input', className)}
          style={{
            width: '100%',
            background: 'var(--bg-elevated)',
            border: `1px solid ${error ? 'var(--error)' : 'var(--border-default)'}`,
            borderRadius: 'var(--radius-md)',
            color: 'var(--text-primary)',
            padding: `10px ${rightIcon ? '40px' : '14px'} 10px ${icon ? '40px' : '14px'}`,
            fontSize: '0.9375rem',
            outline: 'none',
            transition: 'border-color 0.2s, box-shadow 0.2s',
            fontFamily: 'var(--font-body)',
            ...style,
          }}
          onFocus={(e) => {
            e.target.style.borderColor = 'var(--gold)'
            e.target.style.boxShadow = '0 0 0 3px rgba(201,168,76,0.12)'
            props.onFocus?.(e)
          }}
          onBlur={(e) => {
            e.target.style.borderColor = error ? 'var(--error)' : 'var(--border-default)'
            e.target.style.boxShadow = 'none'
            props.onBlur?.(e)
          }}
          {...props}
        />
        {rightIcon && (
          <span style={{
            position: 'absolute',
            right: '12px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
          }}>
            {rightIcon}
          </span>
        )}
      </div>
      {error && (
        <motion.span
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ fontSize: '0.8125rem', color: 'var(--error)' }}
        >
          {error}
        </motion.span>
      )}
    </div>
  )
)
Input.displayName = 'Input'

// ─── Card ─────────────────────────────────────────────────────────────────────
interface CardProps {
  children: React.ReactNode
  className?: string
  hover?: boolean
  gold?: boolean
  style?: React.CSSProperties
  onClick?: () => void
}

export const Card: React.FC<CardProps> = ({ children, hover, gold, style, onClick, className }) => (
  <motion.div
    whileHover={hover ? { y: -2, boxShadow: gold ? 'var(--shadow-gold)' : '0 8px 32px rgba(0,0,0,0.5)' } : undefined}
    onClick={onClick}
    style={{
      background: 'var(--bg-card)',
      border: `1px solid ${gold ? 'rgba(201,168,76,0.2)' : 'var(--border-subtle)'}`,
      borderRadius: 'var(--radius-lg)',
      padding: '24px',
      boxShadow: 'var(--shadow-card)',
      cursor: onClick ? 'pointer' : 'default',
      ...style,
    }}
    className={className}
  >
    {children}
  </motion.div>
)

// ─── Badge ────────────────────────────────────────────────────────────────────
type BadgeVariant = 'default' | 'success' | 'error' | 'warning' | 'gold' | 'blue'

export const Badge: React.FC<{ variant?: BadgeVariant; children: React.ReactNode }> = ({ variant = 'default', children }) => {
  const styles: Record<BadgeVariant, React.CSSProperties> = {
    default: { background: 'var(--bg-elevated)', color: 'var(--text-secondary)', border: '1px solid var(--border-subtle)' },
    success: { background: 'var(--success-dim)', color: 'var(--success)', border: '1px solid rgba(52,211,153,0.25)' },
    error:   { background: 'var(--error-dim)', color: 'var(--error)', border: '1px solid rgba(248,113,113,0.25)' },
    warning: { background: 'var(--warning-dim)', color: 'var(--warning)', border: '1px solid rgba(251,191,36,0.25)' },
    gold:    { background: 'var(--gold-dim)', color: 'var(--gold)', border: '1px solid rgba(201,168,76,0.3)' },
    blue:    { background: 'var(--accent-dim)', color: 'var(--accent)', border: '1px solid rgba(79,142,247,0.3)' },
  }
  return (
    <span style={{ ...styles[variant], padding: '2px 10px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: '4px', whiteSpace: 'nowrap' }}>
      {children}
    </span>
  )
}

// ─── Spinner ──────────────────────────────────────────────────────────────────
export const Spinner: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = 'var(--accent)' }) => (
  <Loader2 size={size} style={{ color, animation: 'spin 1s linear infinite' }} />
)

// ─── PageLoader ───────────────────────────────────────────────────────────────
export const PageLoader: React.FC = () => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', flexDirection: 'column', gap: '16px' }}>
    <motion.div animate={{ rotate: 360 }} transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
      style={{ width: 40, height: 40, border: '2px solid var(--border-default)', borderTopColor: 'var(--gold)', borderRadius: '50%' }} />
    <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontFamily: 'var(--font-mono)' }}>Loading...</span>
  </div>
)

// ─── Modal ────────────────────────────────────────────────────────────────────
interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}

export const Modal: React.FC<ModalProps> = ({ open, onClose, title, children, size = 'md' }) => {
  const widths = { sm: '400px', md: '560px', lg: '720px' }

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div key="backdrop" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={onClose}
            style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)', zIndex: 100 }} />
          <div key="modal-wrapper"
            style={{
              position: 'fixed',
              top: 0, left: 0, right: 0, bottom: 0,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              zIndex: 101,
              pointerEvents: 'none',
            }}>
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
              style={{
                width: `min(${widths[size]}, 95vw)`, maxHeight: '90vh', overflowY: 'auto',
                background: 'var(--bg-card)', border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-xl)', padding: '28px',
                boxShadow: '0 24px 80px rgba(0,0,0,0.7)',
                pointerEvents: 'all',
              }}>
              {title && (
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                  <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.4rem', color: 'var(--text-primary)' }}>{title}</h2>
                  <button onClick={onClose}
                    style={{ background: 'none', border: 'none', color: 'var(--text-muted)', padding: '4px', cursor: 'pointer', borderRadius: '4px' }}>
                    <X size={18} />
                  </button>
                </div>
              )}
              {children}
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  )
}

// ─── EmptyState ───────────────────────────────────────────────────────────────
export const EmptyState: React.FC<{ icon: React.ReactNode; title: string; description?: string; action?: React.ReactNode }> = ({ icon, title, description, action }) => (
  <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
    style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '64px 24px', gap: '12px', textAlign: 'center' }}>
    <div style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>{icon}</div>
    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--text-secondary)' }}>{title}</h3>
    {description && <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', maxWidth: '300px' }}>{description}</p>}
    {action && <div style={{ marginTop: '12px' }}>{action}</div>}
  </motion.div>
)

// ─── StatCard ─────────────────────────────────────────────────────────────────
export const StatCard: React.FC<{ label: string; value: string | number; icon: React.ReactNode; color?: string; delay?: number }> = ({ label, value, icon, color = 'var(--accent)', delay = 0 }) => (
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }}
    style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
    <StarBorder
      as="div"
      color={color}
      speed="5s"
      thickness={2}
      className="stat-card-star"
      style={{ display: 'block', borderRadius: 'var(--radius-lg)', width: '100%' }}
    >
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: 'calc(var(--radius-lg) - 2px)',
        padding: '20px',
        position: 'relative',
        overflow: 'hidden',
        border: '1px solid var(--border-subtle)',
      }}>
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '2px', background: color, opacity: 0.5 }} />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.875rem', fontWeight: 500, color: 'var(--text-primary)' }}>{value}</div>
          </div>
          <div style={{ color, background: `${color}15`, padding: '10px', borderRadius: 'var(--radius-md)' }}>{icon}</div>
        </div>
      </div>
    </StarBorder>
  </motion.div>
)