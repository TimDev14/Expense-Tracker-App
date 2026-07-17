import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { ProductProvider } from './context/ProductProvider.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* TODO(Milestone 2): wrap protected screens in the signed-in user provider
        once authentication state and route guards are implemented. */}
    <BrowserRouter>
      <ProductProvider><App /></ProductProvider>
    </BrowserRouter>
  </StrictMode>,
)
