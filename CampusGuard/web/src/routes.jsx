import { Navigate, Route, Routes } from "react-router-dom";
import StudentPage from "./features/student/StudentPage";
import DashboardPage from "./features/dashboard/DashboardPage";
import InsightsPage from "./features/insights/InsightsPage";
export default function AppRoutes(){return <Routes><Route path="/" element={<StudentPage/>}/><Route path="/dashboard" element={<DashboardPage/>}/><Route path="/insights" element={<InsightsPage/>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes>}
