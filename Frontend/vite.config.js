import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './'),
      '@components': resolve(__dirname, './components'),
      '@hooks': resolve(__dirname, './hooks'),
      '@services': resolve(__dirname, './services'),
      '@utils': resolve(__dirname, './utils'),
      '@assets': resolve(__dirname, './assets')
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    lib: {
      entry: resolve(__dirname, 'index.js'),
      name: 'HeadlessCMSModules',
      formats: ['es', 'umd']
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
      }
    }
  },
  server: {
    port: 3001,
    open: true
  },
  preview: {
    port: 3001
  }
})