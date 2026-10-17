import { Navigate, Route, Routes } from "react-router-dom";
import StudentPage from "./features/student/StudentPage";
import DashboardPage from "./features/dashboard/DashboardPage";
import InsightsPage from "./features/insights/InsightsPage";
import AdminPage from "./features/admin/AdminPage";
import LoginPage from "./features/auth/LoginPage";
import ProtectedRoute from "./features/auth/ProtectedRoute";
export default function AppRoutes(){return <Routes><Route path="/" element={<StudentPage/>}/><Route path="/login" element={<LoginPage/>}/><Route path="/dashboard" element={<ProtectedRoute roles={["admin","responder"]}><DashboardPage/></ProtectedRoute>}/><Route path="/insights" element={<ProtectedRoute roles={["admin","responder"]}><InsightsPage/></ProtectedRoute>}/><Route path="/admin" element={<ProtectedRoute roles={["admin"]}><AdminPage/></ProtectedRoute>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes>}
