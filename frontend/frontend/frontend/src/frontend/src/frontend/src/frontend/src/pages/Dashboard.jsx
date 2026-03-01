import React, {useState, useEffect} from 'react'

export default function Dashboard(){
  const [cartoes, setCartoes] = useState([])
  useEffect(()=> {
    const api = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    fetch(api + '/cartoes')
      .then(r=>r.json())
      .then(setCartoes).catch(()=>setCartoes([]))
  },[])
  return (
    <div style={{padding:20}}>
      <h1>Virada Financeira</h1>
      <h3>Do aperto ao controle</h3>
      <section>
        <h4>Cartões</h4>
        <ul>
          {cartoes.map(c=>(
            <li key={c.id}>{c.nome} - Limite: {c.limite_total} - Utilizado: {c.limite_utilizado}</li>
          ))}
        </ul>
      </section>
      <p>Interface escura simples — você pode estender com mais componentes.</p>
    </div>
  )
}
