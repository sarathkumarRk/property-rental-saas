import { useEffect, useState } from "react"
import API from "../api/axios"

function LeaseRequests() {

  const [requests, setRequests] = useState([])

  useEffect(() => {
    fetchRequests()
  }, [])

  const fetchRequests = async () => {

    const res = await API.get(
      "/leases/requests"
    )

    setRequests(res.data)
  }

  const approveRequest = async (requestId) => {

    await API.post(
      "/leases/approve",
      {
        request_id: requestId,
        start_date: "2026-05-01",
        end_date: "2027-05-01"
      }
    )

    alert("Lease Approved")

    fetchRequests()
  }

  const rejectRequest = async (requestId) => {

    await API.put(
      `/leases/reject/${requestId}`
    )

    alert("Lease Rejected")

    fetchRequests()
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-yellow-100 to-orange-100 p-10">

      <h1 className="text-5xl font-bold text-center text-orange-600 mb-10">

        Lease Requests

      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {requests.map((req) => (

          <div
            key={req.id}
            className="bg-white shadow-2xl rounded-3xl p-6"
          >

            <h2 className="text-2xl font-bold mb-2">

              {req.property_title}

            </h2>

            <p className="mb-1">
              Tenant: {req.tenant_email}
            </p>

            <p className="mb-3">
              Status:
              <span className="font-bold ml-2">
                {req.status}
              </span>
            </p>

            {req.status === "pending" && (

              <div className="flex gap-4 mt-4">

                <button
                  onClick={() =>
                    approveRequest(req.id)
                  }
                  className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
                >

                  Approve

                </button>

                <button
                  onClick={() =>
                    rejectRequest(req.id)
                  }
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
                >

                  Reject

                </button>

              </div>
            )}

          </div>
        ))}

      </div>

    </div>
  )
}

export default LeaseRequests