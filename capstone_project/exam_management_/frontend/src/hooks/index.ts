import { useState, useEffect, useCallback, useRef } from 'react'
import { useAuthStore } from '@/store/authStore'

// ─── useAuth ─────────────────────────────────────────────────────────────────
export const useAuth = () => {
  const store = useAuthStore()
  return {
    user: store.user,
    isAuthenticated: store.isAuthenticated,
    isLoading: store.isLoading,
    isAdmin: store.user?.role === 'admin',
    isStudent: store.user?.role === 'student',
    login: store.login,
    register: store.register,
    logout: store.logout,
    fetchMe: store.fetchMe,
  }
}

// ─── useFetch ─────────────────────────────────────────────────────────────────
export function useFetch<T>(fn: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fn()
      setData(result)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Something went wrong'
      setError(msg)
    } finally {
      setLoading(false)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(() => { fetchData() }, [fetchData])

  return { data, loading, error, refetch: fetchData }
}

// ─── useDebounce ─────────────────────────────────────────────────────────────
export function useDebounce<T>(value: T, delay = 400): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  return debounced
}

// ─── useCountdown ─────────────────────────────────────────────────────────────
export function useCountdown(targetDate: string | null, durationMinutes: number) {
  const calcRemaining = useCallback(() => {
    if (!targetDate) return durationMinutes * 60
    const started = new Date(targetDate).getTime()
    const deadline = started + durationMinutes * 60 * 1000
    const remaining = Math.floor((deadline - Date.now()) / 1000)
    return Math.max(0, remaining)
  }, [targetDate, durationMinutes])

  const [seconds, setSeconds] = useState(calcRemaining)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    setSeconds(calcRemaining())
    intervalRef.current = setInterval(() => {
      setSeconds((s) => {
        if (s <= 1) { clearInterval(intervalRef.current!); return 0 }
        return s - 1
      })
    }, 1000)
    return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
  }, [calcRemaining])

  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  const isExpired = seconds === 0
  const isWarning = seconds < 300 // < 5 minutes
  const isDanger = seconds < 60

  return {
    seconds,
    display: `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`,
    isExpired,
    isWarning,
    isDanger,
    percentage: targetDate
      ? Math.round((seconds / (durationMinutes * 60)) * 100)
      : 100,
  }
}

// ─── useLocalStorage ──────────────────────────────────────────────────────────
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}
