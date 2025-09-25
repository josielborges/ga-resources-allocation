/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      colors: {
        primary: {
          main: '#3f6ad8',
          light: '#7996e3',
          DEFAULT: '#3f6ad8',
        },
        secondary: {
          main: '#495057',
          light: '#6c757d',
          DEFAULT: '#495057',
        },
        background: {
          default: '#f1f4f6',
          paper: '#ffffff',
          sidebar: '#343a40',
        },
        text: {
          primary: '#495057',
          secondary: '#6c757d',
          disabled: '#adb5bd',
          'on-dark': '#dee2e6',
        },
        semantic: {
          success: {
            main: '#3ac47d',
            light: '#e1f5ec',
            DEFAULT: '#3ac47d',
          },
          error: {
            main: '#d92550',
            light: '#fbe9ed',
            DEFAULT: '#d92550',
          },
          warning: {
            main: '#f7b924',
            light: '#fef8e8',
            DEFAULT: '#f7b924',
          },
          info: {
            main: '#16aaff',
            light: '#e7f6ff',
            DEFAULT: '#16aaff',
          },
        },
        divider: '#e9ecef',
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '16px',
      },
      boxShadow: {
        'level1': '0 0.46875rem 2.1875rem rgba(4, 9, 20, 0.03), 0 0.9375rem 1.40625rem rgba(4, 9, 20, 0.03), 0 0.25rem 0.53125rem rgba(4, 9, 20, 0.05), 0 0.125rem 0.1875rem rgba(4, 9, 20, 0.03)',
        'level2': '0px 5px 15px rgba(0, 0, 0, 0.1)',
      },
      fontSize: {
        'metric-large': '2.25rem',
        'metric-small': '1.5rem',
        'card-title': '1.1rem',
      },
      fontWeight: {
        'metric': '700',
        'card-title': '600',
      },
    },
  },
  plugins: [],
}