import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {SettingsContextProvider} from "@/lib/settingsContext.tsx";

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
     <SettingsContextProvider>
         <App />
     </SettingsContextProvider>
    </QueryClientProvider>
  </StrictMode>,
)