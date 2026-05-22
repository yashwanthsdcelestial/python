import React from 'react'
import { motion } from 'framer-motion'
import { Users, BookOpen, TrendingUp, Award, CheckCircle, BarChart2 } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { useAuth, useFetch } from '@/hooks'
import { adminApi } from '@/api/services'
import { StatCard, PageLoader, Card } from '@/components/shared/UI'

const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: { value: number }[]; label?: string }) => {
  if (active && payload?.length) {
    return (
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '10px 14px' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '4px' }}>{label}</p>
        <p style={{ color: 'var(--gold)', fontFamily: 'var(--font-mono)', fontWeight: 500 }}>{payload[0].value}</p>
      </div>
    )
  }
  return null
}

export const AdminDashboard: React.FC = () => {
  const { user } = useAuth()
  const { data: stats, loading } = useFetch(adminApi.stats)

  if (loading) return <PageLoader />

  const chartData = stats ? [
    { name: 'Total Users', value: stats.total_users, color: 'var(--accent)' },
    { name: 'Students', value: stats.total_students, color: 'var(--gold)' },
    { name: 'Total Exams', value: stats.total_exams, color: '#a78bfa' },
    { name: 'Published', value: stats.published_exams, color: 'var(--success)' },
    { name: 'Attempts', value: stats.total_attempts, color: '#fb923c' },
    { name: 'Passed', value: stats.passed_attempts, color: 'var(--success)' },
  ] : []

  const passRate = stats && stats.total_attempts > 0
    ? Math.round((stats.passed_attempts / stats.total_attempts) * 100)
    : 0

  return (
    <div style={{ maxWidth: '1200px' }}>
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '6px' }}>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--text-primary)' }}>
            Dashboard
          </h1>
          <span style={{ color: 'var(--gold)', fontFamily: 'var(--font-display)', fontStyle: 'italic', fontSize: '1.2rem' }}>Overview</span>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Welcome back, <span style={{ color: 'var(--text-secondary)' }}>{user?.full_name}</span>
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px', marginBottom: '28px' }}>
        <StatCard label="Total Users" value={stats?.total_users ?? 0} icon={<Users size={20} />} color="var(--accent)" delay={0} />
        <StatCard label="Students" value={stats?.total_students ?? 0} icon={<Users size={20} />} color="var(--gold)" delay={0.05} />
        <StatCard label="Total Exams" value={stats?.total_exams ?? 0} icon={<BookOpen size={20} />} color="#a78bfa" delay={0.1} />
        <StatCard label="Published" value={stats?.published_exams ?? 0} icon={<CheckCircle size={20} />} color="var(--success)" delay={0.15} />
        <StatCard label="Attempts" value={stats?.total_attempts ?? 0} icon={<TrendingUp size={20} />} color="#fb923c" delay={0.2} />
        <StatCard label="Pass Rate" value={`${passRate}%`} icon={<Award size={20} />} color="var(--success)" delay={0.25} />
      </div>

      {/* Chart + Pass Rate */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '20px', alignItems: 'start' }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
              <BarChart2 size={18} style={{ color: 'var(--gold)' }} />
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--text-primary)' }}>System Overview</h2>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={chartData} barSize={36}>
                <XAxis dataKey="name" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} fillOpacity={0.85} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </motion.div>

        {/* Pass Rate Gauge */}
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.4 }}>
          <Card style={{ textAlign: 'center', minWidth: '180px' }}>
            <div style={{ position: 'relative', width: '120px', height: '120px', margin: '0 auto 16px' }}>
              <svg viewBox="0 0 120 120" style={{ transform: 'rotate(-90deg)' }}>
                <circle cx="60" cy="60" r="50" fill="none" stroke="var(--bg-elevated)" strokeWidth="10" />
                <motion.circle cx="60" cy="60" r="50" fill="none"
                  stroke={passRate >= 70 ? 'var(--success)' : passRate >= 50 ? 'var(--warning)' : 'var(--error)'}
                  strokeWidth="10" strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 50}`}
                  initial={{ strokeDashoffset: 2 * Math.PI * 50 }}
                  animate={{ strokeDashoffset: 2 * Math.PI * 50 * (1 - passRate / 100) }}
                  transition={{ duration: 1.2, delay: 0.5, ease: 'easeOut' }}
                />
              </svg>
              <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 500, color: 'var(--text-primary)' }}>{passRate}%</span>
              </div>
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Pass Rate</div>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
