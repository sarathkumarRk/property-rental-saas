import { useEffect, useState } from "react"

import API from "../api/axios"

import PropertyCard from "../components/PropertyCard"

function Properties() {

  const [properties, setProperties] = useState([])

  useEffect(() => {

    fetchProperties()

  }, [])

  const fetchProperties = async () => {

    const res = await API.get(
      "/properties/"
    )

    setProperties(res.data)
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-slate-100 to-blue-100 p-10">

      <h1 className="text-4xl font-bold text-center text-purple-700 mb-10">

        Available Properties

      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

        {properties.map((property) => (

          <PropertyCard
            key={property.id}
            property={property}
          />

        ))}

      </div>

    </div>
  )
}

export default Properties