import { Link } from "react-router-dom"

function Navbar() {

  const logout = () => {

    localStorage.removeItem("token")

    window.location.href = "/login"
  }

  return (

    <div className="bg-black text-white p-4 flex items-center justify-between">

      <div className="flex gap-8 items-center flex-wrap">

        <Link to="/">
          Properties
        </Link>

        <Link to="/login">
          Login
        </Link>

        <Link to="/register">
          Register
        </Link>

        <Link to="/owner-dashboard">
          Owner Dashboard
        </Link>

        <Link to="/tenant-dashboard">
          Tenant Dashboard
        </Link>

        <Link to="/lease-requests">
          Lease Requests
        </Link>

        <Link to="/maintenance">
          Maintenance
        </Link>

        <Link to="/payments">
          Payments
        </Link>

        <Link to="/create-property">
          Create Property
        </Link>

        <Link to="/admin-dashboard">
          Admin Dashboard
        </Link>

      </div>

      <button
        onClick={logout}
        className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded"
      >

        Logout

      </button>

    </div>
  )
}

export default Navbar