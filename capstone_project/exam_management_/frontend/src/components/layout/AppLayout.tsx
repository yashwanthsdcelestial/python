import React, { useState } from 'react'
import { NavLink, useNavigate, Outlet } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, BookOpen, ClipboardList, Users, LogOut,
  Menu, X, Award, ChevronRight, GraduationCap,
} from 'lucide-react'
import { useAuth } from '@/hooks'
import toast from 'react-hot-toast'

const adminLinks = [
  { to: '/admin', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
  { to: '/admin/exams', icon: <BookOpen size={18} />, label: 'Exams' },
  { to: '/admin/users', icon: <Users size={18} />, label: 'Users' },
]

const studentLinks = [
  { to: '/student', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
  { to: '/student/exams', icon: <BookOpen size={18} />, label: 'Browse Exams' },
  { to: '/student/my-exams', icon: <ClipboardList size={18} />, label: 'My Exams' },
  { to: '/student/results', icon: <Award size={18} />, label: 'Results' },
]

export const AppLayout: React.FC = () => {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const links = isAdmin ? adminLinks : studentLinks

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const SidebarContent = () => (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Logo */}
      <div style={{ padding: '28px 24px 20px', borderBottom: '1px solid var(--border-subtle)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: 36, height: 36, background: 'linear-gradient(135deg, var(--gold), var(--gold-light))',
            borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <GraduationCap size={20} color="var(--bg-void)" />
          </div>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)', lineHeight: 1 }}>ExamPortal</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', marginTop: '2px' }}>
              {isAdmin ? 'Admin Console' : 'Student Portal'}
            </div>
          </div>
        </div>
      </div>

      {/* Nav Links */}
      <nav style={{ flex: 1, padding: '16px 12px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} end={link.to.split('/').length === 2}
            onClick={() => setSidebarOpen(false)}
            style={({ isActive }) => ({
              display: 'flex', alignItems: 'center', gap: '10px',
              padding: '10px 12px', borderRadius: 'var(--radius-md)',
              color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
              background: isActive ? 'var(--bg-hover)' : 'transparent',
              borderLeft: isActive ? '2px solid var(--gold)' : '2px solid transparent',
              fontSize: '0.9rem', fontWeight: isActive ? 500 : 400,
              textDecoration: 'none', transition: 'all 0.15s',
            })}>
            {link.icon}
            <span>{link.label}</span>
            <ChevronRight size={14} style={{ marginLeft: 'auto', opacity: 0.4 }} />
          </NavLink>
        ))}
      </nav>

      {/* User section */}
      <div style={{ padding: '16px', borderTop: '1px solid var(--border-subtle)' }}>
        <div style={{
          background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)',
          padding: '12px', marginBottom: '8px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: 34, height: 34, borderRadius: '50%',
              background: 'linear-gradient(135deg, var(--accent), var(--gold))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '0.875rem', fontWeight: 600, color: 'white', flexShrink: 0,
            }}>
              {user?.full_name?.charAt(0).toUpperCase()}
            </div>
            <div style={{ overflow: 'hidden', flex: 1 }}>
              <div style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-primary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {user?.full_name}
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                {user?.role}
              </div>
            </div>
          </div>
        </div>
        <button onClick={handleLogout} style={{
          width: '100%', display: 'flex', alignItems: 'center', gap: '8px',
          padding: '9px 12px', borderRadius: 'var(--radius-md)',
          background: 'none', border: 'none', color: 'var(--text-muted)',
          fontSize: '0.875rem', cursor: 'pointer', transition: 'all 0.15s',
        }}
          onMouseEnter={e => { e.currentTarget.style.color = 'var(--error)'; e.currentTarget.style.background = 'var(--error-dim)' }}
          onMouseLeave={e => { e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.background = 'none' }}>
          <LogOut size={16} />
          Sign Out
        </button>
      </div>
    </div>
  )

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Desktop Sidebar */}
      <aside style={{
        width: '240px', flexShrink: 0, background: 'var(--bg-surface)',
        borderRight: '1px solid var(--border-subtle)',
        position: 'sticky', top: 0, height: '100vh',
        display: 'none',
      }} className="desktop-sidebar">
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div key="overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', zIndex: 50, backdropFilter: 'blur(4px)' }} />
            <motion.aside key="mobile-sidebar"
              initial={{ x: '-100%' }} animate={{ x: 0 }} exit={{ x: '-100%' }}
              transition={{ type: 'spring', stiffness: 400, damping: 35 }}
              style={{
                position: 'fixed', left: 0, top: 0, bottom: 0, width: '260px',
                background: 'var(--bg-surface)', borderRight: '1px solid var(--border-default)',
                zIndex: 51,
              }}>
              <button onClick={() => setSidebarOpen(false)}
                style={{ position: 'absolute', top: '16px', right: '16px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={20} />
              </button>
              <SidebarContent />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        {/* Mobile Header */}
        <header style={{
          padding: '16px 20px', background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-subtle)',
          display: 'flex', alignItems: 'center', gap: '16px', position: 'sticky', top: 0, zIndex: 10,
        }} className="mobile-header">
          <button onClick={() => setSidebarOpen(true)}
            style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', display: 'flex' }}>
            <Menu size={22} />
          </button>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--gold)' }}>ExamPortal</div>
        </header>

        <main style={{ flex: 1, padding: '28px', overflowY: 'auto' }}>
          <Outlet />
        </main>
      </div>

      <style>{`
        @media (min-width: 768px) {
          .desktop-sidebar { display: block !important; }
          .mobile-header { display: none !important; }
        }
      `}</style>
    </div>
  )
}
