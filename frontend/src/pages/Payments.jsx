import { useEffect, useState } from "react"

import API from "../api/axios"

import { loadStripe } from "@stripe/stripe-js"

const stripePromise = loadStripe(
  "pk_test_51TN4QWEJ9XVT4TIpMvwUzKUfMrPOoyXyPkNfSBzXCcWia1BSNsRa2bO22nSnZYoCvGk3keiQDrkj2J5zSF0ktXv700jI0To4ay"
)

function Payments() {

  const [payments, setPayments] = useState([])

  const [leaseId, setLeaseId] = useState("")

  useEffect(() => {

    fetchPayments()

  }, [])

  const fetchPayments = async () => {

    const res = await API.get(
      "/payments/"
    )

    setPayments(res.data)
  }

  const payRent = async () => {

    const stripe = await stripePromise

    const res = await API.post(
      `/payments/${leaseId}`
    )

    const clientSecret = res.data.client_secret

    await stripe.confirmCardPayment(
      clientSecret,
      {
        payment_method: {
          card: {
            token: "tok_visa"
          }
        }
      }
    )

    alert("Payment Successful")

    fetchPayments()
  }

  return (

    <div className="min-h-screen bg-gradient-to-r from-green-100 to-emerald-200 p-10">

      <h1 className="text-5xl font-bold text-center text-green-700 mb-10">

        Payments

      </h1>

      <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-xl mx-auto mb-10">

        <h2 className="text-2xl font-bold mb-5">

          Pay Rent

        </h2>

        <input
          placeholder="Lease ID"
          className="border-2 border-gray-300 p-4 rounded-xl w-full mb-5"
          onChange={(e) =>
            setLeaseId(e.target.value)
          }
        />

        <button
          onClick={payRent}
          className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-4 rounded-xl w-full text-lg font-bold"
        >

          Pay Now

        </button>

      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {payments.map((payment) => (

          <div
            key={payment.id}
            className="bg-white shadow-xl rounded-2xl p-6"
          >

            <p className="text-xl font-bold">

              Amount: ₹ {payment.amount}

            </p>

            <p className="mt-2">

              Status:
              <span className="font-bold text-green-600 ml-2">

                {payment.payment_status}

              </span>

            </p>

            <p className="mt-2 text-gray-500">

              {payment.payment_date}

            </p>

          </div>

        ))}

      </div>

    </div>
  )
}

export default Payments