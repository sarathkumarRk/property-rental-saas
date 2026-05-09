import { useEffect, useState } from "react"

import API from "../api/axios"

function OwnerDashboard() {

  const [data, setData] = useState(null)

  useEffect(() => {

    fetchDashboard()

  }, [])

  const fetchDashboard = async () => {

    const res = await API.get(
      "/dashboard/owner"
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

    <div className="min-h-screen bg-gradient-to-r from-indigo-100 to-purple-200 p-10">

      <h1 className="text-5xl font-bold text-center text-purple-700 mb-12">

        Owner Dashboard

      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-indigo-600 mb-3">

            Total Properties

          </h2>

          <p className="text-5xl font-bold text-gray-800">

            {data.total_properties}

          </p>

        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-green-600 mb-3">

            Active Leases

          </h2>

          <p className="text-5xl font-bold text-gray-800">

            {data.active_leases}

          </p>

        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-pink-600 mb-3">

            Monthly Revenue

          </h2>

          <p className="text-5xl font-bold text-gray-800">

            ₹ {data.monthly_revenue}

          </p>

        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-red-600 mb-3">

            Open Maintenance

          </h2>

          <p className="text-5xl font-bold text-gray-800">

            {data.open_maintenance}

          </p>

        </div>

      </div>

    </div>
  )
}

export default OwnerDashboard