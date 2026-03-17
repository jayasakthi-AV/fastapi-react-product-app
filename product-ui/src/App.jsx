import { useState, useEffect } from "react"

function App() {

  const [products,setProducts] = useState([])
  const [id,setId] = useState("")
  const [name,setName] = useState("")
  const [price,setPrice] = useState("")

  const API = "http://127.0.0.1:8000"

  // fetch products
  const loadProducts = async () =>{
    const res = await fetch(`${API}/products`)
    const data = await res.json()
    setProducts(data)
  }

  useEffect(()=>{
    loadProducts()
  },[])

  // add product
  const addProduct = async () =>{

    await fetch(`${API}/products`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({
        id:parseInt(id),
        name:name,
        price:parseFloat(price)
      })
    })

    loadProducts()
  }

  // delete product
  const deleteProduct = async (pid) =>{

    await fetch(`${API}/products/${pid}`,{
      method:"DELETE"
    })

    loadProducts()
  }

  return (
    <div style={{padding:"40px"}}>

      <h1>Product Manager</h1>

      <h3>Add Product</h3>

      <input placeholder="ID" onChange={(e)=>setId(e.target.value)} />
      <input placeholder="Name" onChange={(e)=>setName(e.target.value)} />
      <input placeholder="Price" onChange={(e)=>setPrice(e.target.value)} />

      <button onClick={addProduct}>Add</button>

      <h3>Products</h3>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>

          {products.map((p)=>(
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.price}</td>
              <td>
                <button onClick={()=>deleteProduct(p.id)}>Delete</button>
              </td>
            </tr>
          ))}

        </tbody>

      </table>

    </div>
  )
}

export default App