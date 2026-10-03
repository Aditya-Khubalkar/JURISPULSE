import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

// Design-token CSS custom properties (must come first)
import '@/styles/globals.css';
import '@/styles/dark-theme.css';

// Base reset and element defaults
import '@/styles/base.css';

// Primitive layer
import '@/styles/forms.css';
import '@/styles/surfaces.css';
import '@/styles/typography.css';
import '@/styles/motion.css';
import '@/styles/breakpoints.css';
import '@/styles/accessibility.css';

import App from '@/App';


const root = document.getElementById('root');
if (!root) throw new Error('Root element not found');

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>
);
