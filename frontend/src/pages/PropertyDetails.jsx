import { useEffect, useState } from "react"

import { useParams } from "react-router-dom"

import API from "../api/axios"

function PropertyDetails() {

  const { id } = useParams()

  const [property, setProperty] = useState(null)

  useEffect(() => {

    fetchProperty()

  }, [])

  const fetchProperty = async () => {

    const res = await API.get(
      `/properties/${id}`
    )

    setProperty(res.data)
  }

  const requestLease = async () => {

    await API.post(
      "/leases/request",
      {
        property_id: parseInt(id)
      }
    )

    alert("Lease Requested Successfully")
  }

  if (!property) {

    return (

      <div className="flex items-center justify-center min-h-screen text-3xl font-bold">

        Loading...

      </div>
    )
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-blue-100 to-purple-100 flex items-center justify-center p-10">

      <div className="bg-white rounded-3xl shadow-2xl overflow-hidden max-w-5xl w-full grid md:grid-cols-2">

        <img
          src={
            property.image_url
              ? property.image_url
              : "https://via.placeholder.com/800x600?text=No+Image"
          }
          alt={property.title}
          className="w-full h-full object-cover"
        />

        <div className="p-10 flex flex-col justify-center">

          <h1 className="text-5xl font-bold text-gray-800 mb-5">

            {property.title}

          </h1>

          <p className="text-lg text-gray-600 mb-4">

            {property.description}

          </p>

          <p className="text-xl text-gray-500 mb-3">

            📍 {property.address}

          </p>

          <p className="text-4xl font-bold text-green-600 mb-8">

            ₹ {property.rent_amount}

          </p>

          <button
            onClick={requestLease}
            className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-4 rounded-2xl text-xl font-semibold hover:scale-105 duration-300"
          >

            Request Lease

          </button>

        </div>

      </div>

    </div>
  )
}

export default PropertyDetails