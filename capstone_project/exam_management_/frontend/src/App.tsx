    import { Toaster } from 'react-hot-toast'
    import { AppRouter } from '@/router'
    import ClickSpark from '@/components/shared/ClickSpark'

    function App() {
      return (
        <ClickSpark
          sparkColor='#c9a84c'
          sparkSize={12}
          sparkRadius={20}
          sparkCount={8}
          duration={500}
          easing='ease-out'
          extraScale={1.2}
        >
          <AppRouter />
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3500,
              style: {
                background: 'var(--bg-card)',
                border: '1px solid var(--border-default)',
                color: 'var(--text-primary)',
                fontFamily: 'var(--font-body)',
                fontSize: '0.875rem',
                boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
              },
              success: {
                iconTheme: { primary: 'var(--success)', secondary: 'var(--bg-card)' },
              },
              error: {
                iconTheme: { primary: 'var(--error)', secondary: 'var(--bg-card)' },
              },
            }}
          />
        </ClickSpark>
      )
    }

    export default App