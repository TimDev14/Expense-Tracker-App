import { useContext } from 'react'
import { ProductContext } from './ProductContext'

export const useProductContext = () => {
    // TODO(Milestone 2): update this hook to match the final session provider
    // API and use it in protected layouts and authenticated pages.
    const context = useContext(ProductContext)
    if(!context){
        throw new Error('useProductContext must be used within a ProductProvider')
    }
    return context
}
