import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useDebounce, useCountdown } from '@/hooks'

// ─── useDebounce ──────────────────────────────────────────────────────────────
describe('useDebounce', () => {
  beforeEach(() => { vi.useFakeTimers() })

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 400))
    expect(result.current).toBe('hello')
  })

  it('does not update before delay', () => {
    const { result, rerender } = renderHook(({ val }) => useDebounce(val, 400), {
      initialProps: { val: 'hello' },
    })
    rerender({ val: 'world' })
    expect(result.current).toBe('hello')
  })

  it('updates after delay', () => {
    const { result, rerender } = renderHook(({ val }) => useDebounce(val, 400), {
      initialProps: { val: 'hello' },
    })
    rerender({ val: 'world' })
    act(() => { vi.advanceTimersByTime(400) })
    expect(result.current).toBe('world')
  })
})

// ─── useCountdown ─────────────────────────────────────────────────────────────
describe('useCountdown', () => {
  beforeEach(() => { vi.useFakeTimers() })

  it('returns correct display format MM:SS', () => {
    const started = new Date(Date.now() - 10_000).toISOString() // 10 secs ago
    const { result } = renderHook(() => useCountdown(started, 1)) // 1 min exam
    // Should show something like 00:50 (50 seconds left)
    expect(result.current.display).toMatch(/^\d{2}:\d{2}$/)
  })

  it('isExpired is false when time remains', () => {
    const started = new Date(Date.now()).toISOString()
    const { result } = renderHook(() => useCountdown(started, 60))
    expect(result.current.isExpired).toBe(false)
  })

  it('isExpired is true when time is up', () => {
    const started = new Date(Date.now() - 61 * 60 * 1000).toISOString() // 61 min ago
    const { result } = renderHook(() => useCountdown(started, 60))
    expect(result.current.isExpired).toBe(true)
    expect(result.current.seconds).toBe(0)
  })

  it('isDanger is true when less than 60 seconds remain', () => {
    const started = new Date(Date.now() - (60 * 60 - 30) * 1000).toISOString() // 30s left
    const { result } = renderHook(() => useCountdown(started, 60))
    expect(result.current.isDanger).toBe(true)
    expect(result.current.isWarning).toBe(true)
  })
})

// ─── Utility helpers ──────────────────────────────────────────────────────────
describe('score formatting helpers', () => {
  const fmtPct = (score: number, total: number) =>
    total > 0 ? Math.round((score / total) * 100) : 0

  it('calculates percentage correctly', () => {
    expect(fmtPct(40, 50)).toBe(80)
    expect(fmtPct(0, 50)).toBe(0)
    expect(fmtPct(50, 50)).toBe(100)
  })

  it('handles zero total gracefully', () => {
    expect(fmtPct(10, 0)).toBe(0)
  })
})
