/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          // Legacy aliases mapped to clean enterprise tokens for backwards compatibility
          dark: '#0f172a',
          panel: '#ffffff',
          card: '#ffffff',
          border: '#e2e8f0',
          accent: '#2563eb',
          cyan: '#2563eb',
          emerald: '#16a34a',
          amber: '#d97706',
          rose: '#dc2626',
        },
        surface: {
          ground: '#f8fafc',
          card: '#ffffff',
          subtle: '#f1f5f9',
          hover: '#f8fafc',
          active: '#eff6ff',
        },
        border: {
          subtle: '#e2e8f0',
          default: '#cbd5e1',
          focus: '#3b82f6',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
        sans: ['Inter', 'Segoe UI', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'xs': '0 1px 2px 0 rgba(15, 23, 42, 0.03)',
        'sm': '0 1px 3px 0 rgba(15, 23, 42, 0.06), 0 1px 2px -1px rgba(15, 23, 42, 0.04)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px 0 rgba(0, 0, 0, 0.02)',
      }
    },
  },
  plugins: [],
}

