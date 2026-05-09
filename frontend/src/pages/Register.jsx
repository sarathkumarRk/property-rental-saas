import { useState } from "react"

import { useNavigate } from "react-router-dom"

import API from "../api/axios"

function Register() {

  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: "",
    password: "",
    role: "tenant"
  })

  const handleSubmit = async (e) => {

    e.preventDefault()

    await API.post(
      "/auth/register",
      form
    )

    alert("Registered Successfully")

    navigate("/login")
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center">

      <form
        onSubmit={handleSubmit}
        className="bg-white p-10 rounded-2xl shadow-2xl flex flex-col gap-5 w-[400px]"
      >

        <h1 className="text-3xl font-bold text-center text-purple-600">

          Register

        </h1>

        <input
          type="email"
          placeholder="Email"
          className="border p-3 rounded-lg outline-none focus:border-purple-500"
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
          className="border p-3 rounded-lg outline-none focus:border-purple-500"
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value
            })
          }
        />

        <select
          className="border p-3 rounded-lg outline-none focus:border-purple-500"
          onChange={(e) =>
            setForm({
              ...form,
              role: e.target.value
            })
          }
        >

          <option value="tenant">
            Tenant
          </option>

          <option value="owner">
            Owner
          </option>

        </select>

        <button
          className="bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-lg text-lg font-semibold"
        >

          Register

        </button>

      </form>

    </div>
  )
}

export default Register