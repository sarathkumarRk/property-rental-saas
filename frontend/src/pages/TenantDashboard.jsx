import { useEffect, useState } from "react"

import API from "../api/axios"

function TenantDashboard() {

  const [data, setData] = useState(null)

  useEffect(() => {

    fetchDashboard()

  }, [])

  const fetchDashboard = async () => {

    const res = await API.get(
      "/dashboard/tenant"
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

    <div className="min-h-screen bg-gradient-to-r from-cyan-100 to-blue-200 p-10">

      <h1 className="text-5xl font-bold text-center text-blue-700 mb-12">

        Tenant Dashboard

      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-blue-600 mb-3">

            Active Lease

          </h2>

          <p className="text-4xl font-bold text-gray-800">

            {data.active_lease}

          </p>

        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-green-600 mb-3">

            Payments

          </h2>

          <p className="text-4xl font-bold text-gray-800">

            {data.payment_count}

          </p>

        </div>

        <div className="bg-white shadow-2xl rounded-3xl p-8 hover:scale-105 duration-300">

          <h2 className="text-2xl font-bold text-red-600 mb-3">

            Maintenance Requests

          </h2>

          <p className="text-4xl font-bold text-gray-800">

            {data.maintenance_count}

          </p>

        </div>

      </div>

    </div>
  )
}

export default TenantDashboard