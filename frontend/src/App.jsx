import { Routes, Route } from "react-router-dom"

import Navbar from "./components/Navbar"

import Login from "./pages/Login"
import Register from "./pages/Register"

import Properties from "./pages/Properties"
import PropertyDetails from "./pages/PropertyDetails"

import OwnerDashboard from "./pages/OwnerDashboard"
import TenantDashboard from "./pages/TenantDashboard"
import AdminDashboard from "./pages/AdminDashboard"

import Maintenance from "./pages/Maintenance"
import Payments from "./pages/Payments"

import CreateProperty from "./pages/CreateProperty"
import LeaseRequests from "./pages/LeaseRequests"

function App() {

  return (

    <div>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<Properties />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/property/:id"
          element={<PropertyDetails />}
        />

        <Route
          path="/owner-dashboard"
          element={<OwnerDashboard />}
        />

        <Route
          path="/tenant-dashboard"
          element={<TenantDashboard />}
        />

        <Route
          path="/admin-dashboard"
          element={<AdminDashboard />}
        />

        <Route
          path="/maintenance"
          element={<Maintenance />}
        />

        <Route
          path="/payments"
          element={<Payments />}
        />

        <Route
          path="/create-property"
          element={<CreateProperty />}
        />

        <Route
          path="/lease-requests"
          element={<LeaseRequests />}
        />

      </Routes>

    </div>
  )
}

export default App
