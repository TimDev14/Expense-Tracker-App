import {BASE_URL} from "../.env"

try{
    let response = await fetch(BASE_URL)
    if(!response.ok){
        throw new Error("Network Error")
    }
    let data = await response.json()
    return data

}catch(error){
    console.error(error)
}