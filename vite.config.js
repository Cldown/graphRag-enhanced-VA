import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/datas': {
        target: 'http://localhost:8088', // Flask 后端地址
        changeOrigin: true,
        secure: false
      }
    }
  }
})