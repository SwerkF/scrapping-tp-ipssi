import { QueryClientProvider } from '@tanstack/react-query';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { queryClient } from './store/queryClient.ts';

createRoot(document.getElementById('root')!).render(
    <QueryClientProvider client={queryClient}>
        <App />
    </QueryClientProvider>
);
