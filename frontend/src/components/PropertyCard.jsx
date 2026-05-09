import { Link } from "react-router-dom"

function PropertyCard({ property }) {

  return (

    <div className="bg-white rounded-2xl shadow-xl overflow-hidden hover:scale-105 duration-300">

      <img
        src={
          property.image_url
            ? property.image_url
            : "https://via.placeholder.com/600x400?text=No+Image"
        }
        alt={property.title}
        className="w-full h-60 object-cover"
      />

      <div className="p-5">

        <h1 className="text-3xl font-bold text-gray-800">

          {property.title}

        </h1>

        <p className="text-gray-600 mt-3">

          {property.description}

        </p>

        <p className="text-gray-500 mt-2">

          📍 {property.address}

        </p>

        <p className="text-2xl font-bold text-green-600 mt-4">

          ₹ {property.rent_amount}

        </p>

        <Link
          to={`/property/${property.id}`}
          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-5 py-3 rounded-xl inline-block mt-5 hover:opacity-90"
        >

          View Property

        </Link>

      </div>

    </div>
  )
}

export default PropertyCard