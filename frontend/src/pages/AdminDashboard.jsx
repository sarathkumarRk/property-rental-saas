import { useEffect, useState } from "react"
import API from "../api/axios"

function AdminDashboard() {

  const [data, setData] = useState(null)

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    const res = await API.get(
      "/admin/dashboard"
    )
    setData(res.data)
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center text-4xl font-bold">
        Loading...
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-100 to-slate-200 p-10">

      <h1 className="text-5xl font-bold text-center text-gray-800 mb-12">
        Admin Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8 max-w-7xl mx-auto">

        <div className="bg-white shadow-2xl rounded-3xl p-8">
          <h2 className="text-2xl font-bold text-blue-600 mb-3">
            Total Users
          </h2>
          <p className="text-4xl font-bold text-gray-800">
            {data.total_users}
          </p>
        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8">
          <h2 className="text-2xl font-bold text-green-600 mb-3">
            Total Properties
          </h2>
          <p className="text-4xl font-bold text-gray-800">
            {data.total_properties}
          </p>
        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8">
          <h2 className="text-2xl font-bold text-purple-600 mb-3">
            Active Leases
          </h2>
          <p className="text-4xl font-bold text-gray-800">
            {data.active_leases}
          </p>
        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8">
          <h2 className="text-2xl font-bold text-red-600 mb-3">
            Total Revenue
          </h2>
          <p className="text-4xl font-bold text-gray-800">
            ₹ {data.total_revenue}
          </p>
        </div>

      </div>
    </div>
  )
}

export default AdminDashboard