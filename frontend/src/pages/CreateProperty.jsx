import { useState } from "react"

import API from "../api/axios"

function CreateProperty() {

  const [form, setForm] = useState({
    title: "",
    description: "",
    address: "",
    rent_amount: ""
  })

  const [image, setImage] = useState(null)

  const handleSubmit = async (e) => {

    e.preventDefault()

    // Step 1: Create property
    const res = await API.post(
      "/properties/",
      {
        ...form,
        rent_amount: Number(form.rent_amount)
      }
    )

    const propertyId = res.data.id

    // Step 2: Upload image (if selected)
    if (image) {

      const formData = new FormData()

      formData.append(
        "file",
        image
      )

      await API.post(
        `/properties/${propertyId}/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      )
    }

    alert("Property Created Successfully")
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-green-100 to-emerald-200 flex items-center justify-center p-10">

      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-2xl rounded-3xl p-10 flex flex-col gap-5 w-full max-w-xl"
      >

        <h1 className="text-4xl font-bold text-center text-green-700 mb-5">

          Create Property

        </h1>

        <input
          placeholder="Property Title"
          className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-green-500"
          onChange={(e) =>
            setForm({
              ...form,
              title: e.target.value
            })
          }
        />

        <textarea
          placeholder="Property Description"
          rows="4"
          className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-green-500"
          onChange={(e) =>
            setForm({
              ...form,
              description: e.target.value
            })
          }
        />

        <input
          placeholder="Property Address"
          className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-green-500"
          onChange={(e) =>
            setForm({
              ...form,
              address: e.target.value
            })
          }
        />

        <input
          placeholder="Monthly Rent"
          type="number"
          className="border-2 border-gray-300 p-4 rounded-xl outline-none focus:border-green-500"
          onChange={(e) =>
            setForm({
              ...form,
              rent_amount: e.target.value
            })
          }
        />

        <input
          type="file"
          accept="image/*"
          className="border-2 border-gray-300 p-3 rounded-xl"
          onChange={(e) =>
            setImage(e.target.files[0])
          }
        />

        <button
          className="bg-gradient-to-r from-green-500 to-emerald-600 text-white p-4 rounded-xl text-lg font-semibold hover:scale-105 duration-300"
        >

          Create Property

        </button>

      </form>

    </div>
  )
}

export default CreateProperty