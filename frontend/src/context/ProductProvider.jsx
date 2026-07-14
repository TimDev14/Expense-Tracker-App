import { useEffect } from "react"
import {useState, useEffect, useMemo} from "react"
import {ProductContext, productContext} from "./ProductContext"

export const ProductProvider = ({children}) => {
    const [loading, setLoading] = useState(false)
    useEffect(() => {
        setLoading(true)
    })
    return(<ProductContext.Provider value={contextValue}>
        {children}
    </ProductContext.Provider>)
}