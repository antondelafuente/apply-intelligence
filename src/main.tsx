import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ApplyIntelligence from './components/ApplyIntelligence/ApplyIntelligence.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ApplyIntelligence />
  </StrictMode>,
);
