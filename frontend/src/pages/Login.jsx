import { useState } from "react"

import { useNavigate } from "react-router-dom"

import API from "../api/axios"

function Login() {

  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: "",
    password: ""
  })

  const handleSubmit = async (e) => {

    e.preventDefault()

    const res = await API.post(
      "/auth/login",
      form
    )

    localStorage.setItem(
      "token",
      res.data.access_token
    )

    alert("Login Successful")

    navigate("/")
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 flex items-center justify-center">

      <form
        onSubmit={handleSubmit}
        className="bg-white p-10 rounded-2xl shadow-2xl flex flex-col gap-5 w-[400px]"
      >

        <h1 className="text-3xl font-bold text-center text-blue-600">

          Login

        </h1>

        <input
          type="email"
          placeholder="Email"
          className="border p-3 rounded-lg outline-none focus:border-blue-500"
          onChange={(e) =>
            setForm({
              ...form,
              email: e.target.value
            })
          }
        />

        <input
          type="password"
          placeholder="Password"
          className="border p-3 rounded-lg outline-none focus:border-blue-500"
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value
            })
          }
        />

        <button
          className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg text-lg font-semibold"
        >

          Login

        </button>

      </form>

    </div>
  )
}

export default Login