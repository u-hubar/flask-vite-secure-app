import vue from '@vitejs/plugin-vue'
import { hostname } from "vite";

export default {
  plugins: [vue()],
  server: {
    hmr: {
      protocol: 'wss',
      host: hostname,
      port: 443,
      path: 'wsdev/',
    },
  },
}
