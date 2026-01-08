import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import viteTsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), viteTsconfigPaths()],
  server: {
    // This ensures Vite listens on all IPs (needed for Docker)
    host: '0.0.0.0', 
    port: 3000,
    open: false, 
  },
});