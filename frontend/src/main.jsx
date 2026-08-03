// Application entry point. Mounts the React app into the <div id="root"> in
// index.html. StrictMode surfaces unsafe patterns during development and has no
// effect in the production build.
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
