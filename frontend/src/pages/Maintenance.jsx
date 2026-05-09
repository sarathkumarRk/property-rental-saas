import { useState } from "react"

import API from "../api/axios"

function Maintenance() {

  const [propertyId, setPropertyId] = useState("")

  const [issue, setIssue] = useState("")

  const submitIssue = async () => {

    await API.post(
      `/maintenance/?property_id=${propertyId}&issue=${issue}`
    )

    alert("Maintenance Request Submitted")
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-orange-100 to-red-100 flex items-center justify-center p-10">

      <div className="bg-white shadow-2xl rounded-3xl p-10 w-full max-w-lg">

        <h1 className="text-4xl font-bold text-center text-red-600 mb-8">

          Maintenance Request

        </h1>

        <div className="flex flex-col gap-5">

          <input
            placeholder="Property ID"
            className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-red-500"
            onChange={(e) =>
              setPropertyId(e.target.value)
            }
          />

          <textarea
            placeholder="Describe the Issue"
            rows="5"
            className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-red-500"
            onChange={(e) =>
              setIssue(e.target.value)
            }
          />

          <button
            onClick={submitIssue}
            className="bg-gradient-to-r from-red-500 to-orange-500 text-white p-4 rounded-xl text-lg font-semibold hover:scale-105 duration-300"
          >

            Submit Request

          </button>

        </div>

      </div>

    </div>
  )
}

export default Maintenance